#!/bin/bash
set -e

echo "=== STEP 1: Preprocess city data ==="
python src/preprocessing/clean_city.py

echo "=== STEP 2: Train central baseline model ==="
python src/evaluation/central_baseline.py

echo "=== STEP 3: Train manual FedAvg model ==="
python src/federated/manual_fedavg.py

echo "=== STEP 4: Evaluate global model ==="
python -m src.federated.eval_global_model

echo "=== STEP 5: Run data drift detection ==="
python src/evaluation/data_drift.py

echo "=== STEP 6: Conditional retraining if drift is HIGH ==="
python src/training/retrain_if_drift.py

echo "=== PIPELINE COMPLETED SUCCESSFULLY ==="
