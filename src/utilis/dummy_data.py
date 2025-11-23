import os
import pandas as pd
import numpy as np
import pickle

np.random.seed(42)

# Ensure dirs exist
os.makedirs("data/raw/city", exist_ok=True)
os.makedirs("data/raw/hospitals/S2", exist_ok=True)
os.makedirs("data/raw/hospitals/S3", exist_ok=True)
os.makedirs("data/raw/hospitals/S4", exist_ok=True)
os.makedirs("data/raw/hospitals/S5", exist_ok=True)
os.makedirs("data/raw/hospitals/S9", exist_ok=True)


# -------------------------
# CITY DUMMY DATA
# -------------------------


def create_dummy_city_excel(name):
    df = pd.DataFrame(
        {
            "datetime": pd.date_range("2024-01-01", periods=100, freq="H"),
            "pm25": np.random.uniform(10, 150, 100),
            "pm10": np.random.uniform(20, 200, 100),
            "nh3": np.random.uniform(1, 10, 100),
            "co": np.random.uniform(0.1, 3.0, 100),
            "temperature": np.random.uniform(10, 40, 100),
            "humidity": np.random.uniform(20, 90, 100),
        }
    )

    path = f"data/raw/city/{name}_complete_data.xlsx"
    df.to_excel(path, index=False)
    print(f"Created Excel: {path}")


def create_dummy_city_csv(name):
    df = pd.DataFrame(
        {
            "datetime": pd.date_range("2024-01-01", periods=100, freq="H"),
            "pm25": np.random.uniform(10, 150, 100),
            "pm10": np.random.uniform(20, 200, 100),
            "nh3": np.random.uniform(1, 10, 100),
            "co": np.random.uniform(0.1, 3.0, 100),
            "temperature": np.random.uniform(10, 40, 100),
            "humidity": np.random.uniform(20, 90, 100),
        }
    )

    path = f"data/raw/city/{name}_complete_data.csv"
    df.to_csv(path, index=False)
    print(f"Created CSV: {path}")


# -------------------------
# HOSPITAL DUMMY DATA
# -------------------------


def create_dummy_hospital(name):
    df = pd.DataFrame(
        {
            "HeartRate": np.random.randint(60, 120, 200),
            "Temp": np.random.uniform(36, 40, 200),
            "PM25": np.random.uniform(10, 200, 200),
            "NO2": np.random.uniform(5, 80, 200),
            "CO_Level": np.random.uniform(0.1, 5.0, 200),
            "Label": np.random.randint(0, 3, 200),
        }
    )

    path = f"data/raw/hospitals/{name}/{name}.pkl"
    with open(path, "wb") as f:
        pickle.dump(df, f)
    print(f"Created PKL: {path}")


# -------------------------
# EXECUTE GENERATION
# -------------------------

if __name__ == "__main__":

    # Excel cities
    for city in ["lahore", "karachi", "islamabad"]:
        create_dummy_city_excel(city)

    # CSV cities
    for city in ["peshawar", "quetta"]:
        create_dummy_city_csv(city)

    # Hospitals
    for hospital in ["S2", "S3", "S4", "S5", "S9"]:
        create_dummy_hospital(hospital)

    print("\nALL DUMMY DATA GENERATED SUCCESSFULLY!")
