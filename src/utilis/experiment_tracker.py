import os
import csv
from datetime import datetime

LOG_DIR = "logs"
LOG_PATH = os.path.join(LOG_DIR, "experiments.csv")


def log_experiment(model_name: str, metrics: dict, params: dict):
    """
    Append one experiment run to logs/experiments.csv
    """

    # Ensure directory exists
    os.makedirs(LOG_DIR, exist_ok=True)

    # Build flat row
    row = {
        "timestamp": datetime.utcnow().isoformat(),
        "model_name": model_name,
    }

    # Prefix keys to keep tables clean
    for k, v in params.items():
        row[f"param_{k}"] = v

    for k, v in metrics.items():
        row[f"metric_{k}"] = v

    # Detect if CSV already exists
    file_exists = os.path.exists(LOG_PATH)

    with open(LOG_PATH, mode="a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=row.keys())

        # Write header only once
        if not file_exists:
            writer.writeheader()

        writer.writerow(row)

    print(f"[ExperimentTracker] Logged run for {model_name} → {LOG_PATH}")
