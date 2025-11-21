import numpy as np
import pandas as pd
from pathlib import Path

PROCESSED_CITY_DIR = Path("data/processed/city")
PROCESSED_HOSPITAL_DIR = Path("data/processed/hospital")

# Subject → (city, window_mode)
# window_mode:
#   "low"      → mostly label 0
#   "mid"      → mostly label 1
#   "high"     → mostly label 2
#   "balanced" → mix of 0/1/2 ≈ 1/3 each
SUBJECT_CONFIG = {
    "S2": ("lahore", "high"),
    "S3": ("karachi", "balanced"),   # IMPORTANT CHANGE
    "S4": ("islamabad", "low"),
    "S5": ("peshawar", "balanced"),
    "S9": ("quetta", "balanced"),
}


def load_city_with_risk(city_name: str) -> pd.DataFrame:
    """Load processed city data, fill pollution, compute per-minute risk label."""
    path = PROCESSED_CITY_DIR / f"client_city_{city_name}.csv"
    if not path.exists():
        raise FileNotFoundError(f"City file not found: {path}")

    df = pd.read_csv(path, parse_dates=["Timestamp"])
    df = df.sort_values("Timestamp").reset_index(drop=True)

    # Fill NaNs in pollution columns so we can compute a pollution index everywhere
    for col in ["PM25", "NO2", "CO_Level"]:
        med = df[col].median(skipna=True)
        if pd.isna(med):
            med = 0.0
        df[col] = df[col].fillna(med)

    # Same pollution index logic as in merge_city_hospital
    pollution_index = (
        0.5 * df["PM25"] +
        0.3 * df["NO2"] +
        0.2 * df["CO_Level"]
    )

    conds = [
        pollution_index < 0.33,
        pollution_index < 0.66,
    ]
    choices = [0, 1]
    risk_label = np.select(conds, choices, default=2).astype(int)

    df["RiskLabel"] = risk_label
    return df


def select_window(city_df: pd.DataFrame, window_len: int, mode: str) -> pd.Series:
    """
    Select a contiguous window of length `window_len` minutes from city_df["Timestamp"]
    according to the desired mode:
      - "low"      → maximize fraction of label 0
      - "mid"      → maximize fraction of label 1
      - "high"     → maximize fraction of label 2
      - "balanced" → make fractions of (0,1,2) as close as possible to (1/3,1/3,1/3)
    """
    labels = city_df["RiskLabel"].to_numpy()
    n = len(labels)

    if window_len >= n:
        # hospital is longer than city data → just take full series
        start_pos = 0
        end_pos = n
        print(
            f"Warning: window_len={window_len} >= city_len={n}, "
            f"using entire city range."
        )
        return city_df["Timestamp"].iloc[start_pos:end_pos].reset_index(drop=True)

    # Step size to reduce computation but keep overlap
    step = max(1, window_len // 2)

    best_score = None
    best_start = 0

    target_balanced = np.array([1/3, 1/3, 1/3])

    for start in range(0, n - window_len, step):
        end = start + window_len
        window = labels[start:end]
        counts = np.bincount(window, minlength=3)
        frac = counts / window_len  # fractions for labels 0,1,2

        if mode == "low":
            score = frac[0]  # maximize fraction of label 0
        elif mode == "mid":
            score = frac[1]  # maximize fraction of label 1
        elif mode == "high":
            score = frac[2]  # maximize fraction of label 2
        elif mode == "balanced":
            # we want frac close to (1/3,1/3,1/3) → minimize L1 distance
            score = -np.abs(frac - target_balanced).sum()
        else:
            raise ValueError(f"Unknown mode '{mode}'")

        if (best_score is None) or (score > best_score):
            best_score = score
            best_start = start

    best_end = best_start + window_len
    ts_slice = city_df["Timestamp"].iloc[best_start:best_end].reset_index(drop=True)
    return ts_slice


def align_subject(subject_id: str, city_name: str, mode: str):
    """
    Align a hospital subject to a chosen pollution window from the mapped city.
    """
    hosp_path = PROCESSED_HOSPITAL_DIR / f"client_hospital_{subject_id}.csv"
    if not hosp_path.exists():
        raise FileNotFoundError(f"Hospital file not found: {hosp_path}")

    df_h = pd.read_csv(hosp_path, parse_dates=["Timestamp"])
    n_rows = len(df_h)
    if n_rows == 0:
        raise ValueError(f"Hospital dataframe for {subject_id} is empty.")

    city_df = load_city_with_risk(city_name)
    ts_window = select_window(city_df, n_rows, mode)

    df_h["Timestamp"] = ts_window
    df_h.to_csv(hosp_path, index=False)

    print(
        f"Aligned {subject_id} → {city_name} ({mode} window): "
        f"{ts_window.iloc[0]} → {ts_window.iloc[-1]} (rows={n_rows})"
    )


def align_all_subjects():
    for subject_id, (city_name, mode) in SUBJECT_CONFIG.items():
        print(f"\n=== Aligning {subject_id} with {city_name} ({mode}) ===")
        align_subject(subject_id, city_name, mode)


if __name__ == "__main__":
    align_all_subjects()
