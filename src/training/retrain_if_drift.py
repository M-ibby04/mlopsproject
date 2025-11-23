import json
import os

from src.evaluation.central_baseline import main as train_central
from src.federated.manual_fedavg import main as train_fedavg


DRIFT_SUMMARY_PATH = "data/processed/eval/data_drift_summary.json"


def should_retrain(threshold_label: str = "HIGH") -> bool:
    if not os.path.exists(DRIFT_SUMMARY_PATH):
        print("[Retrain] No drift summary found; skipping.")
        return False

    with open(DRIFT_SUMMARY_PATH, "r") as f:
        summary = json.load(f)

    label = summary.get("label", "LOW")
    print(f"[Retrain] Drift label = {label}")

    order = {"LOW": 0, "MEDIUM": 1, "HIGH": 2}
    return order.get(label, 0) >= order.get(threshold_label, 2)


def main():
    if not should_retrain("HIGH"):
        print("[Retrain] Drift not high enough; no retraining.")
        return

    print("[Retrain] Drift is HIGH → retraining models...")

    # Retrain central baseline
    train_central()

    # Retrain federated global model
    train_fedavg()

    print("[Retrain] Done retraining models.")


if __name__ == "__main__":
    main()
