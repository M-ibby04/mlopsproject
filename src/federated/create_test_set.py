import os
import pandas as pd
import glob
from collections import Counter

# --- Configuration ---
# NOTE: Ensure the 'Label' column is present in all client CSVs
FEATURE_COLS = ["HeartRate", "Temp", "PM25", "NO2", "CO_Level"]
TARGET_COL = "Label"
ALL_COLS = FEATURE_COLS + [TARGET_COL] 

CITY_DIR = "data/processed/city"
HOSP_DIR = "data/processed/hospital"
OUT_DIR = "data/processed/test"
OUT_PATH = os.path.join(OUT_DIR, "test_all_clients.csv")

SAMPLES_PER_CLASS = 100  # target per class


def collect_optimal_test_rows():
    os.makedirs(OUT_DIR, exist_ok=True)
    
    # 1. Collect all file paths efficiently
    all_files = []
    for directory in [CITY_DIR, HOSP_DIR]:
        # Use glob to find all CSVs recursively within the directories
        all_files.extend(glob.glob(os.path.join(directory, "*.csv")))

    # 2. Load and concatenate all data
    # Use list comprehension for efficient loading
    dfs = [pd.read_csv(f) for f in all_files]
    
    if not dfs:
        print("[TEST] No CSV files found to combine.")
        return

    combined = pd.concat(dfs, ignore_index=True)

    # 3. Feature Selection and Validation
    # Ensure all required columns are present before balancing
    missing = set(ALL_COLS) - set(combined.columns)
    if missing:
        print(f"ERROR: Missing required columns in combined data: {missing}")
        return
        
    # Select only the required columns for the test set
    combined = combined[ALL_COLS]

    # 4. Balanced Test Set Sampling
    def sample_group(group):
        # Sample up to SAMPLES_PER_CLASS, or less if the group is smaller
        n_samples = min(len(group), SAMPLES_PER_CLASS)
        return group.sample(n=n_samples, random_state=42)
        
    balanced = (
        combined.groupby(TARGET_COL)
        .apply(sample_group)
        .reset_index(drop=True)
    )

    # 5. Final Shuffle and Save
    balanced = balanced.sample(frac=1, random_state=42).reset_index(drop=True)

    balanced.to_csv(OUT_PATH, index=False)

    print(f"\n[TEST] Saved BALANCED test set → {OUT_PATH}")
    print("Label Distribution in Final Test Set:")
    print(balanced[TARGET_COL].value_counts())

if __name__ == "__main__":
    collect_optimal_test_rows()