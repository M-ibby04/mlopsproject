import os
import pandas as pd
import numpy as np
import pickle

np.random.seed(42)

# Ensure dirs exist
os.makedirs("data/raw/city", exist_ok=True)
os.makedirs("data/raw/hospitals", exist_ok=True)


def create_dummy_city(name):
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
    path = f"data/raw/city/{name}_complete_data_dummy.csv"
    df.to_csv(path, index=False)
    print(f"Created: {path}")


def create_dummy_hospital(name):
    df = pd.DataFrame(
        {
            "HeartRate": np.random.randint(60, 120, 100),
            "Temp": np.random.uniform(36, 40, 100),
            "PM25": np.random.uniform(10, 200, 100),
            "NO2": np.random.uniform(5, 80, 100),
            "CO_Level": np.random.uniform(0.1, 5.0, 100),
            "Label": np.random.randint(0, 3, 100),
        }
    )
    path = f"data/raw/hospitals/{name}_dummy.pkl"
    with open(path, "wb") as f:
        pickle.dump(df, f)
    print(f"Created: {path}")


if __name__ == "__main__":
    # Dummy cities
    for c in ["lahore", "karachi", "islamabad", "peshawar", "quetta"]:
        create_dummy_city(c)

    # Dummy hospitals
    for h in ["S2", "S3", "S4", "S5", "S9"]:
        create_dummy_hospital(h)
