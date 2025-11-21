import os
from typing import Dict, List

import pandas as pd
import tensorflow as tf

# Columns we use as features
FEATURE_COLS = ["HeartRate", "Temp", "PM25", "NO2", "CO_Level"]
TARGET_COL = "Label"

# Training hyperparameters
TARGET_SAMPLES_PER_CLASS = 500   # aim per label per client (with replacement if needed)
BATCH_SIZE = 32
LOCAL_EPOCHS = 5                 # more local training per round


def load_all_client_dfs() -> Dict[str, pd.DataFrame]:
    """
    Load processed CSVs for all city and hospital nodes.
    Returns: dict mapping client_id -> pandas DataFrame
    """
    clients: Dict[str, pd.DataFrame] = {}

    city_dir = "data/processed/city"
    hosp_dir = "data/processed/hospital"

    # City nodes
    if os.path.isdir(city_dir):
        for fname in os.listdir(city_dir):
            if fname.endswith(".csv"):
                cid = fname.replace(".csv", "")  # e.g., client_city_lahore
                df = pd.read_csv(os.path.join(city_dir, fname))
                clients[cid] = df

    # Hospital nodes
    if os.path.isdir(hosp_dir):
        for fname in os.listdir(hosp_dir):
            if fname.endswith(".csv"):
                cid = fname.replace(".csv", "")  # e.g., client_hospital_S2
                df = pd.read_csv(os.path.join(hosp_dir, fname))
                clients[cid] = df

    return clients


def balance_labels(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create a roughly balanced dataset per client by oversampling minority classes
    and capping majority classes at TARGET_SAMPLES_PER_CLASS.
    """
    if TARGET_COL not in df.columns:
        raise ValueError(f"Expected label column '{TARGET_COL}' in dataframe.")

    def _sample_group(group: pd.DataFrame) -> pd.DataFrame:
        n_available = len(group)
        if n_available == 0:
            return group
        # If class is rare, oversample with replacement; if big, downsample
        n_samples = min(TARGET_SAMPLES_PER_CLASS, n_available)
        replace = n_available < TARGET_SAMPLES_PER_CLASS
        return group.sample(
            n=n_samples if not replace else TARGET_SAMPLES_PER_CLASS,
            replace=replace,
            random_state=42,
        )

    balanced = (
        df.groupby(TARGET_COL, group_keys=False)
          .apply(_sample_group)
          .reset_index(drop=True)
    )

    return balanced


def df_to_tf_dataset(df: pd.DataFrame) -> tf.data.Dataset:
    """
    Convert a single node's DataFrame into a tf.data.Dataset
    of (features, label) batches, with label balancing and
    multiple local epochs.
    """
    # Balance labels per client to avoid majority-class collapse
    df_balanced = balance_labels(df)

    # Features: float32
    X = df_balanced[FEATURE_COLS].astype("float32").to_numpy()
    # Labels: int32
    y = df_balanced[TARGET_COL].astype("int32").to_numpy()

    ds = tf.data.Dataset.from_tensor_slices((X, y))
    ds = (
        ds.shuffle(buffer_size=min(len(df_balanced), 1000))
          .repeat(LOCAL_EPOCHS)
          .batch(BATCH_SIZE)
          .prefetch(tf.data.AUTOTUNE)
    )
    return ds


def build_federated_data() -> List[tf.data.Dataset]:
    """
    Build a list of client datasets for TFF training.
    Each entry == data for one client/node.
    """
    client_dfs = load_all_client_dfs()
    federated_data: List[tf.data.Dataset] = []

    for cid, df in client_dfs.items():
        balanced_df = balance_labels(df)
        ds = df_to_tf_dataset(df)
        federated_data.append(ds)

        print(
            f"[TFF] Prepared dataset for client '{cid}', "
            f"original_samples={len(df)}, balanced_samples={len(balanced_df)}"
        )

    return federated_data
