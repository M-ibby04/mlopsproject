import pandas as pd
import numpy as np
import json
import os
from scipy.stats import ks_2samp
from pathlib import Path
from datetime import datetime

FEATURE_COLS = ["HeartRate", "Temp", "PM25", "NO2", "CO_Level"]
LABEL_COL = "Label"

TRAIN_PATH = Path("data/processed/merged_hospitals")
NEW_DATA_PATH = Path("data/processed/test/test_all_clients.csv")


def load_training_distribution():
    files = list(TRAIN_PATH.glob("client_merged_*.csv"))
    if not files:
        raise FileNotFoundError(f"No training CSVs found in {TRAIN_PATH}")

    dfs = [pd.read_csv(f)[FEATURE_COLS + [LABEL_COL]] for f in files]
    train_df = pd.concat(dfs, ignore_index=True)
    return train_df


def psi(expected, actual, buckets=10):
    def scale(series):
        return pd.qcut(series.rank(method="first"), buckets, duplicates="drop")

    expected_pct = scale(expected).value_counts(normalize=True)
    actual_pct = scale(actual).value_counts(normalize=True)

    psi_val = np.sum(
        (expected_pct - actual_pct)
        * np.log((expected_pct + 1e-8) / (actual_pct + 1e-8))
    )
    return psi_val


def detect_drift(train_df, new_df):
    report = {}

    for col in FEATURE_COLS:
        ks_statistic, ks_p_value = ks_2samp(train_df[col], new_df[col])
        psi_value = psi(train_df[col], new_df[col])

        drift_label = (
            "HIGH" if psi_value > 0.25 else "MEDIUM" if psi_value > 0.10 else "LOW"
        )

        report[col] = {
            "ks_statistic": float(ks_statistic),
            "ks_p_value": float(ks_p_value),
            "psi": float(psi_value),
            "drift_level": drift_label,
        }

    # Label distribution drift (classification)
    label_train = train_df[LABEL_COL].value_counts(normalize=True)
    label_new = new_df[LABEL_COL].value_counts(normalize=True)

    label_psi = np.sum(
        (label_train - label_new).fillna(0)
        * np.log((label_train + 1e-8) / (label_new + 1e-8))
    )

    label_drift = (
        "HIGH" if label_psi > 0.25 else "MEDIUM" if label_psi > 0.10 else "LOW"
    )

    report["Label"] = {
        "psi": float(label_psi),
        "drift_level": label_drift,
    }

    return report


def main():
    print("\n[DRIFT] Loading datasets...")
    train_df = load_training_distribution()
    new_df = pd.read_csv(NEW_DATA_PATH)

    new_df = new_df[FEATURE_COLS + [LABEL_COL]].dropna()

    print("[DRIFT] Computing drift scores...\n")
    report = detect_drift(train_df, new_df)

    # Print report
    for col, info in report.items():
        print(
            f"{col}: drift={info['drift_level']} | "
            f"KS_p={info.get('ks_p_value', 'N/A')} | "
            f"PSI={info['psi']:.4f}"
        )

    # ---- Save summary to JSON ----
    latest_label_drift = report["Label"]["drift_level"]
    latest_label_psi = report["Label"]["psi"]

    summary = {
        "label": latest_label_drift,
        "label_psi": latest_label_psi,
        "timestamp": datetime.utcnow().isoformat(),
    }

    os.makedirs("data/processed/eval", exist_ok=True)
    out_path = "data/processed/eval/data_drift_summary.json"

    with open(out_path, "w") as f:
        json.dump(summary, f, indent=2)

    print(f"\n[DataDrift] Summary saved to {out_path}")


if __name__ == "__main__":
    main()
