import numpy as np
import pandas as pd
from pathlib import Path

# Paths based on your current structure
PROCESSED_CITY_DIR = Path("data/processed/city")
PROCESSED_HOSPITAL_DIR = Path("data/processed/hospital")
MERGED_DIR = Path("data/processed/merged_hospitals")
MERGED_DIR.mkdir(parents=True, exist_ok=True)

# Map each WESAD subject (hospital) to some city
# adjust mapping if you want different cities per subject
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
    df = pd.read_csv(path, parse_dates=["Timestamp"])
    return df


def load_city(city_name: str) -> pd.DataFrame:
    """Load already-cleaned city data (pollution only)."""
    path = PROCESSED_CITY_DIR / f"client_city_{city_name}.csv"
    if not path.exists():
        raise FileNotFoundError(f"{path} not found. Run clean_city.py first.")
    df = pd.read_csv(path, parse_dates=["Timestamp"])
    # keep only timestamp + pollution
    return df[["Timestamp", "PM25", "NO2", "CO_Level"]]


def make_risk_label_from_pollution(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create a 3-class health risk label from pollution.
    We DO NOT drop rows – we fill missing pollution values instead.
    """
    df = df.copy()

    # If some of the early minutes have NaNs in pollution, fill them.
    # You can choose median, mean, or even 0. I'll use median here.
    for col in ["PM25", "NO2", "CO_Level"]:
        col_median = df[col].median(skipna=True)
        # fall back to 0 if whole column is NaN for some reason
        if pd.isna(col_median):
            col_median = 0.0
        df[col] = df[col].fillna(col_median)

    pollution_index = (
        0.5 * df["PM25"] +
        0.3 * df["NO2"] +
        0.2 * df["CO_Level"]
    )

    conds = [
        pollution_index < 0.33,
        pollution_index < 0.66,
    ]
    choices = [0, 1]  # 0 = low, 1 = medium, 2 = high
    risk_label = np.select(conds, choices, default=2).astype(int)

    df["Label"] = risk_label
    return df



def merge_subject_with_city(subject_id: str, city_name: str):
    print(f"\n=== Merging hospital {subject_id} with city {city_name} ===")

    # 1) Load hospital data
    df_h = load_hospital(subject_id)

    # If hospital already has fake pollution columns from clean_wesad, drop them.
    df_h = df_h.drop(columns=["PM25", "NO2", "CO_Level"], errors="ignore")

    # Keep original WESAD stress label (if present) but under a different name
    if "Label" in df_h.columns:
        df_h = df_h.rename(columns={"Label": "StressLabel"})

    # 2) Load city pollution data
    df_c = load_city(city_name)

    # 3) Sort both by Timestamp for merge_asof
    df_h = df_h.sort_values("Timestamp")
    df_c = df_c.sort_values("Timestamp")

    # 4) Time-based join: match each hospital row to nearest city pollution timestamp
    # within a tolerance window (e.g., 30 minutes)
    merged = pd.merge_asof(
        df_h,
        df_c,
        on="Timestamp",
        direction="nearest",
        tolerance=pd.Timedelta("30min"),  # adjust if needed
    )

    # 5) Sanity check we really have pollution columns now
    required_cols = ["PM25", "NO2", "CO_Level"]
    missing = [c for c in required_cols if c not in merged.columns]
    if missing:
        raise ValueError(
            f"Pollution columns missing after merge for subject {subject_id}. "
            f"Missing: {missing}. Got columns: {list(merged.columns)}"
        )

    # 6) Build health-risk label from pollution and store in 'Label'
    merged = make_risk_label_from_pollution(merged)

    # 7) Final column order: Timestamp, vitals, pollution, Label, StressLabel (optional)
    cols = ["Timestamp", "HeartRate", "Temp", "PM25", "NO2", "CO_Level", "Label"]
    if "StressLabel" in merged.columns:
        cols.append("StressLabel")

    merged = merged[cols]

    # 8) Save
    out_path = MERGED_DIR / f"client_merged_{subject_id}.csv"
    merged.to_csv(out_path, index=False)
    print(f"Saved {out_path}, shape={merged.shape}")


def merge_all():
    for subject_id, city_name in HOSPITAL_TO_CITY.items():
        merge_subject_with_city(subject_id, city_name)


if __name__ == "__main__":
    merge_all()
