import numpy as np
import pandas as pd
from pathlib import Path

# Paths
PROCESSED_CITY_DIR = Path("data/processed/city")
PROCESSED_HOSPITAL_DIR = Path("data/processed/hospital")
MERGED_DIR = Path("data/processed/merged_hospitals")
MERGED_DIR.mkdir(parents=True, exist_ok=True)

# City ↔ Hospital mapping
HOSPITAL_TO_CITY = {
    "S2": "lahore",
    "S3": "karachi",
    "S4": "islamabad",
    "S5": "peshawar",
    "S9": "quetta",
}


def load_hospital(subject_id: str) -> pd.DataFrame:
    """Load already-cleaned hospital data."""
    path = PROCESSED_HOSPITAL_DIR / f"client_hospital_{subject_id}.csv"
    if not path.exists():
        raise FileNotFoundError(f"{path} not found. Run clean_wesad.py first.")
    return pd.read_csv(path, parse_dates=["Timestamp"])


def load_city(city_name: str) -> pd.DataFrame:
    """Load cleaned pollution files."""
    path = PROCESSED_CITY_DIR / f"client_city_{city_name}.csv"
    if not path.exists():
        raise FileNotFoundError(f"{path} not found. Run clean_city.py first.")
    df = pd.read_csv(path, parse_dates=["Timestamp"])
    return df[["Timestamp", "PM25", "NO2", "CO_Level"]]


def make_risk_labels_per_subject(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Fill missing
    for col in ["PM25", "NO2", "CO_Level"]:
        med = df[col].median()
        if pd.isna(med):
            med = 0.0
        df[col] = df[col].fillna(med)

    # --- FIX: add controlled synthetic variance ---
    df["PM25"] = df["PM25"] * 1.0 + np.random.normal(0, 5, len(df))
    df["NO2"] = df["NO2"] * 1.0 + np.random.normal(0, 3, len(df))
    df["CO_Level"] = df["CO_Level"] * 1.0 + np.random.normal(0, 1, len(df))

    # Composite index
    pollution_index = 0.5 * df["PM25"] + 0.3 * df["NO2"] + 0.2 * df["CO_Level"]

    # Per-subject quantiles
    q1 = pollution_index.quantile(1 / 3)
    q2 = pollution_index.quantile(2 / 3)

    df["Label"] = np.select(
        [pollution_index <= q1, pollution_index <= q2], [0, 1], default=2
    ).astype(int)

    return df


def merge_subject_with_city(subject_id: str, city_name: str):
    print(f"\n=== Merging hospital {subject_id} with city {city_name} ===")

    # Load hospital vitals
    df_h = load_hospital(subject_id)

    # Remove fake pollution columns if present
    df_h = df_h.drop(columns=["PM25", "NO2", "CO_Level"], errors="ignore")

    # Keep original WESAD stress label
    if "Label" in df_h.columns:
        df_h = df_h.rename(columns={"Label": "StressLabel"})

    # Load pollution
    df_c = load_city(city_name)

    # Sort before merge_asof
    df_h = df_h.sort_values("Timestamp")
    df_c = df_c.sort_values("Timestamp")

    # Time-aware 1-minute pollution match
    merged = pd.merge_asof(
        df_h,
        df_c,
        on="Timestamp",
        direction="nearest",
        tolerance=pd.Timedelta("30min"),
    )

    # Create balanced risk labels
    merged = make_risk_labels_per_subject(merged)

    # Final output columns
    cols = ["Timestamp", "HeartRate", "Temp", "PM25", "NO2", "CO_Level", "Label"]
    if "StressLabel" in merged.columns:
        cols.append("StressLabel")

    merged = merged[cols]

    # Save
    out_path = MERGED_DIR / f"client_merged_{subject_id}.csv"
    merged.to_csv(out_path, index=False)
    print(f"Saved {out_path}, shape={merged.shape} ✓")


def merge_all():
    for subject_id, city_name in HOSPITAL_TO_CITY.items():
        merge_subject_with_city(subject_id, city_name)


if __name__ == "__main__":
    merge_all()
