# src/federated/manual_fedavg.py

import os
from pathlib import Path

import numpy as np
import pandas as pd
import tensorflow as tf


# ---------- CONFIG ----------

MERGED_DIR = Path("data/processed/merged_hospitals")
MODEL_OUT = Path("models_tff/manual_fedavg_global_model.keras")

FEATURE_COLS = ["HeartRate", "Temp", "PM25", "NO2", "CO_Level"]
LABEL_COL = "Label"

NUM_CLASSES = 3

NUM_ROUNDS = 10          # federated rounds
LOCAL_EPOCHS = 5         # epochs per client per round
BATCH_SIZE = 16
LEARNING_RATE = 1e-3
SEED = 42

tf.keras.utils.set_random_seed(SEED)
np.random.seed(SEED)


# ---------- UTILS ----------

def build_base_model() -> tf.keras.Model:
    """Simple MLP used by all clients + global model."""
    inputs = tf.keras.Input(shape=(len(FEATURE_COLS),), name="features")
    x = tf.keras.layers.Dense(32, activation="relu")(inputs)
    x = tf.keras.layers.Dense(32, activation="relu")(x)
    outputs = tf.keras.layers.Dense(NUM_CLASSES, activation="softmax")(x)

    model = tf.keras.Model(inputs=inputs, outputs=outputs)
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=LEARNING_RATE),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )
    return model


def oversample_balance(df: pd.DataFrame,
                       label_col: str = LABEL_COL) -> pd.DataFrame:
    """
    Balance a client's dataframe by oversampling minority classes
    up to the size of the majority class.

    If a label is completely missing for this client, we *don't*
    create synthetic rows – we just log it.
    """
    counts = df[label_col].value_counts().sort_index()
    print(f"    Label counts BEFORE balance: {counts.to_dict()}")

    if len(counts) == 0:
        return df

    max_count = counts.max()
    dfs = []

    for label, cnt in counts.items():
        class_df = df[df[label_col] == label]
        if cnt == 0:
            # shouldn't really happen, but just in case
            continue

        if cnt < max_count:
            # how many full repeats we can do
            reps = max_count // cnt
            rem = max_count % cnt

            expanded = pd.concat([class_df] * reps, ignore_index=True)
            if rem > 0:
                expanded = pd.concat(
                    [expanded,
                     class_df.sample(rem, replace=True, random_state=SEED)],
                    ignore_index=True
                )
        else:
            expanded = class_df.copy()

        dfs.append(expanded)

    balanced = pd.concat(dfs, ignore_index=True)
    # shuffle
    balanced = balanced.sample(frac=1.0, random_state=SEED).reset_index(drop=True)

    counts_after = balanced[label_col].value_counts().sort_index()
    print(f"    Label counts AFTER balance:  {counts_after.to_dict()}")

    return balanced


def load_client_dataset(csv_path: Path):
    """Load a single client CSV and return (X, y) numpy arrays."""
    df = pd.read_csv(csv_path)

    # Keep only the needed columns and drop NaNs
    df = df[FEATURE_COLS + [LABEL_COL]].dropna().reset_index(drop=True)

    print(f"\nLoading client {csv_path.name}: {len(df)} raw rows")
    # Balance labels within this client
    df_bal = oversample_balance(df, label_col=LABEL_COL)

    X = df_bal[FEATURE_COLS].astype("float32").values
    y = df_bal[LABEL_COL].astype("int32").values
    return X, y


def weighted_average_weights(client_weights, client_sizes):
    """FedAvg: size-weighted average of model weights from all clients."""
    total_examples = np.sum(client_sizes)
    new_weights = []

    # zip over each layer's weights
    for layer_idx in range(len(client_weights[0])):
        layer_stack = np.stack(
            [cw[layer_idx] * (n / total_examples)
             for cw, n in zip(client_weights, client_sizes)],
            axis=0,
        )
        new_layer = np.sum(layer_stack, axis=0)
        new_weights.append(new_layer)

    return new_weights


# ---------- MAIN TRAINING LOOP ----------

def main():
    # 1) Load all client datasets
    client_files = sorted(MERGED_DIR.glob("client_merged_*.csv"))
    if not client_files:
        raise FileNotFoundError(
            f"No client_merged_*.csv files found in {MERGED_DIR.resolve()}"
        )

    client_datasets = {}
    for csv in client_files:
        X, y = load_client_dataset(csv)
        client_datasets[csv.stem] = (X, y)
        print(f"  -> Balanced client {csv.stem}: {X.shape[0]} examples")

    # 2) Initialize global model
    global_model = build_base_model()
    global_weights = global_model.get_weights()

    # 3) Federated training rounds
    for round_idx in range(1, NUM_ROUNDS + 1):
        print(f"\n=== Federated Round {round_idx}/{NUM_ROUNDS} ===")

        client_weights = []
        client_sizes = []
        round_losses = []
        round_accs = []

        for client_name, (X_client, y_client) in client_datasets.items():
            # fresh local model with current global weights
            local_model = build_base_model()
            local_model.set_weights(global_weights)

            history = local_model.fit(
                X_client,
                y_client,
                epochs=LOCAL_EPOCHS,
                batch_size=BATCH_SIZE,
                verbose=0,
            )

            loss, acc = local_model.evaluate(X_client, y_client, verbose=0)
            round_losses.append(loss)
            round_accs.append(acc)

            print(
                f"  Client {client_name}: "
                f"examples={len(X_client)}, "
                f"local_loss={loss:.4f}, local_acc={acc:.4f}"
            )

            client_weights.append(local_model.get_weights())
            client_sizes.append(len(X_client))

        # FedAvg aggregation
        global_weights = weighted_average_weights(client_weights, client_sizes)
        global_model.set_weights(global_weights)

        # quick aggregated eval on concatenated client data (just for tracking)
        all_X = np.concatenate([X for (X, _) in client_datasets.values()], axis=0)
        all_y = np.concatenate([y for (_, y) in client_datasets.values()], axis=0)
        agg_loss, agg_acc = global_model.evaluate(all_X, all_y, verbose=0)
        print(
            f"Round {round_idx} aggregated eval: "
            f"loss={agg_loss:.4f}, acc={agg_acc:.4f}"
        )

    # 4) Save final global model
    MODEL_OUT.parent.mkdir(parents=True, exist_ok=True)
    global_model.save(MODEL_OUT)
    print(f"\nSaved manual FedAvg global model to: {MODEL_OUT}")


if __name__ == "__main__":
    main()
