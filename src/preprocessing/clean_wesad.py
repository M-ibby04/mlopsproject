import pickle
from pathlib import Path

import numpy as np
import pandas as pd

# ==== PATHS ====
RAW_HOSPITAL_DIR = Path("data/raw/hospitals")  # matches your tree: data/raw/hospitals/ S2, S3, ...
PROCESSED_HOSPITAL_DIR = Path("data/processed/hospital")
PROCESSED_HOSPITAL_DIR.mkdir(parents=True, exist_ok=True)

# ==== WHICH SUBJECTS BECOME HOSPITAL NODES ====
# You can change this list later if you want different subjects.
SUBJECTS = ["S2", "S3", "S4", "S5", "S9"]

# ==== WESAD SIGNAL PROPERTIES ====
SAMPLE_RATE = 700          # 700 Hz according to WESAD
WINDOW_SECONDS = 60        # 1 minute windows
WINDOW_SIZE = SAMPLE_RATE * WINDOW_SECONDS  # 42,000 samples per minute

# We'll align timestamps roughly to your city start date for consistency
START_TIME = pd.Timestamp("2021-08-24 00:00:00")


def load_subject_pickle(subject_id: str):
    """
    Load S?.pkl for a given subject ID.
    """
    pkl_path = RAW_HOSPITAL_DIR / subject_id / f"{subject_id}.pkl"
    if not pkl_path.exists():
        raise FileNotFoundError(f"{pkl_path} not found. Check your folder structure and subject list.")
    with open(pkl_path, "rb") as f:
        data = pickle.load(f, encoding="latin1")
    return data


def extract_chest_signals(data):
    """
    Extract ECG, Temp and labels from WESAD dict.
    Chest keys in WESAD are typically: 'ACC','ECG','EMG','EDA','Temp','Resp'.

    We are robust to 'Temp' vs 'TEMP' naming.
    """
    chest = data["signal"]["chest"]

    # ECG
    if "ECG" not in chest:
        raise KeyError(f"ECG channel not found in chest signals. Found keys: {list(chest.keys())}")
    ecg = np.squeeze(chest["ECG"])

    # Temperature (Temp or TEMP)
    temp_key = "Temp"
    if temp_key not in chest:
        if "TEMP" in chest:
            temp_key = "TEMP"
        else:
            raise KeyError(f"Temp/TEMP channel not found in chest signals. Found keys: {list(chest.keys())}")
    temp = np.squeeze(chest[temp_key])

    # Labels
    labels = np.squeeze(data["label"])

    return ecg, temp, labels


def compute_window_modes(label_windows: np.ndarray) -> np.ndarray:
    """
    Compute mode label for each window using numpy (no scipy dependency).
    label_windows shape: (n_windows, window_size)
    """
    n_windows = label_windows.shape[0]
    modes = np.zeros(n_windows, dtype=int)

    for i in range(n_windows):
        window = label_windows[i]
        # bincount only works with non-negative ints
        window = window.astype(int)
        counts = np.bincount(window)
        modes[i] = counts.argmax()
    return modes


def downsample_to_minutes(ecg, temp, labels) -> pd.DataFrame:
    """
    Downsample ECG, temp, labels from 700 Hz to 1-minute windows
    using mean for signals and mode for labels.
    """
    # Ensure equal length
    n = min(len(ecg), len(temp), len(labels))
    ecg = ecg[:n]
    temp = temp[:n]
    labels = labels[:n]

    if n < WINDOW_SIZE:
        raise ValueError(f"Not enough samples ({n}) for one 60s window at 700Hz ({WINDOW_SIZE}).")

    n_windows = n // WINDOW_SIZE

    ecg_reshaped = ecg[: n_windows * WINDOW_SIZE].reshape(n_windows, WINDOW_SIZE)
    temp_reshaped = temp[: n_windows * WINDOW_SIZE].reshape(n_windows, WINDOW_SIZE)
    labels_reshaped = labels[: n_windows * WINDOW_SIZE].reshape(n_windows, WINDOW_SIZE)

    ecg_mean = ecg_reshaped.mean(axis=1)
    temp_mean = temp_reshaped.mean(axis=1)
    label_mode = compute_window_modes(labels_reshaped)

    df = pd.DataFrame(
        {
            "HeartRate": ecg_mean,
            "Temp": temp_mean,
            "Label": label_mode,
        }
    )

    # Construct 1-minute timestamps
    timestamps = pd.date_range(start=START_TIME, periods=len(df), freq="1min")
    df["Timestamp"] = timestamps

    return df


def normalize_health(df: pd.DataFrame) -> pd.DataFrame:
    """
    Min-max normalize HeartRate and Temp to [0,1] per subject.
    """
    df = df.copy()
    for col in ["HeartRate", "Temp"]:
        col_min = df[col].min()
        col_max = df[col].max()
        if pd.isna(col_min) or pd.isna(col_max) or col_max == col_min:
            df[col] = 0.0
        else:
            df[col] = (df[col] - col_min) / (col_max - col_min)
    return df


def add_air_padding(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add zero pollution columns so schema matches city nodes.
    """
    df = df.copy()
    df["PM25"] = 0.0
    df["NO2"] = 0.0
    df["CO_Level"] = 0.0
    return df


def reorder_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Ensure column order matches:
    [Timestamp, HeartRate, Temp, PM25, NO2, CO_Level, Label]
    """
    return df[["Timestamp", "HeartRate", "Temp", "PM25", "NO2", "CO_Level", "Label"]]


def process_subject(subject_id: str):
    print(f"\n=== Processing subject: {subject_id} ===")
    data = load_subject_pickle(subject_id)
    ecg, temp, labels = extract_chest_signals(data)
    df_minute = downsample_to_minutes(ecg, temp, labels)
    df_norm = normalize_health(df_minute)
    df_padded = add_air_padding(df_norm)
    df_final = reorder_columns(df_padded)

    out_path = PROCESSED_HOSPITAL_DIR / f"client_hospital_{subject_id}.csv"
    df_final.to_csv(out_path, index=False)
    print(f"Saved {out_path}, shape={df_final.shape}")


def process_all_subjects():
    for sid in SUBJECTS:
        process_subject(sid)


if __name__ == "__main__":
    process_all_subjects()
