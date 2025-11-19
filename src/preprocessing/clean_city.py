import pandas as pd
import numpy as np
from pathlib import Path

RAW_CITY_DIR = Path("data/raw/city")
PROCESSED_CITY_DIR = Path("data/processed/city")
PROCESSED_CITY_DIR.mkdir(parents=True, exist_ok=True)

# Map node names to filenames (adjust names if your files differ)
CITY_FILES = {
    "lahore": "lahore_complete_data.xlsx",
    "karachi": "karachi_complete_data.xlsx",
    "islamabad": "islamabad_complete_data.xlsx",
    "peshawar": "peshawar_complete_data.csv",
    "quetta": "quetta_complete_data.csv",
}

# we’ll normalize these as our pollution features
POLLUTION_COLS = ["components.co", "components.no2", "components.pm2_5"]

START_TIME = None  # we’ll keep real timestamps from the CSV


def load_city_df(filename: str) -> pd.DataFrame:
    path = RAW_CITY_DIR / filename

    if not path.exists():
        raise FileNotFoundError(f"{path} does not exist")

    # Handle both CSV and Excel
    suffix = path.suffix.lower()
    if suffix in [".xlsx", ".xls"]:
        df = pd.read_excel(path)
    else:
        df = pd.read_csv(path, encoding="latin1")

    if "datetime" not in df.columns:
        raise ValueError(f"'datetime' column not found in {filename}. Found columns: {list(df.columns)}")

    # tolerate formats like "1/9/2021 0:00", "01/09/2021 00:00:00", etc.
    df["Timestamp"] = pd.to_datetime(
        df["datetime"],
        dayfirst=True,      # interpret 1/9/2021 as 1 September, not 9 January
        errors="coerce"     # bad rows become NaT instead of crashing
    )

    # drop rows we couldn't parse
    df = df.dropna(subset=["Timestamp"])
    df = df.set_index("Timestamp").sort_index()
    return df




def fix_missing_and_resample(df: pd.DataFrame) -> pd.DataFrame:
    # Replace -200 with NaN
    df = df.replace(-200, np.nan)

    # Let pandas guess better dtypes first (object -> numeric where possible)
    df = df.infer_objects(copy=False)

    # Work only on numeric columns for interpolation + resample
    numeric_cols = df.select_dtypes(include=["number"]).columns
    df_numeric = df[numeric_cols].copy()

    # Interpolate numeric data
    df_numeric = df_numeric.interpolate(method="linear")

    # Resample numeric data to 1-minute averages
    df_numeric = df_numeric.resample("1min").mean()

    return df_numeric



def normalize_columns(df: pd.DataFrame, cols) -> pd.DataFrame:
    df = df.copy()
    for col in cols:
        if col not in df.columns:
            # if a pollution column is missing, create it as zeros
            df[col] = 0.0
            continue
        col_min = df[col].min()
        col_max = df[col].max()
        if pd.isna(col_min) or pd.isna(col_max) or col_max == col_min:
            df[col] = 0.0
        else:
            df[col] = (df[col] - col_min) / (col_max - col_min)
    return df


def build_city_node(df: pd.DataFrame, node_name: str) -> pd.DataFrame:
    # Normalize only the pollution columns we care about
    df = normalize_columns(df, POLLUTION_COLS)

    df_node = pd.DataFrame(index=df.index)
    df_node["Timestamp"] = df_node.index

    # City has no health data
    df_node["HeartRate"] = 0.0
    df_node["Temp"] = 0.0

    # Map raw pollution columns -> unified schema
    df_node["PM25"] = df["components.pm2_5"] if "components.pm2_5" in df.columns else 0.0
    df_node["NO2"] = df["components.no2"] if "components.no2" in df.columns else 0.0
    df_node["CO_Level"] = df["components.co"] if "components.co" in df.columns else 0.0

    # City has no label → 0
    df_node["Label"] = 0

    # Column order must match hospital nodes
    df_node = df_node[["Timestamp", "HeartRate", "Temp", "PM25", "NO2", "CO_Level", "Label"]]
    return df_node



def process_all_cities():
    for city, filename in CITY_FILES.items():
        print(f"Processing city: {city} from {filename}")
        df_raw = load_city_df(filename)
        df_clean = fix_missing_and_resample(df_raw)
        df_node = build_city_node(df_clean, city)

        out_path = PROCESSED_CITY_DIR / f"client_city_{city}.csv"
        df_node.to_csv(out_path, index=False)
        print(f"Saved {out_path}, shape={df_node.shape}")

if __name__ == "__main__":
    process_all_cities()

