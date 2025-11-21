import os
import numpy as np
import pandas as pd
import tensorflow as tf

from .client import FEATURE_COLS
from .model import NUM_CLASSES

MODEL_PATH = "models_tff/tff_global_model"
TEST_CSV_PATH = "data/processed/test/test_all_clients.csv"


def load_test_dataset(csv_path: str):
    if not os.path.exists(csv_path):
        raise FileNotFoundError(
            f"Test CSV not found at {csv_path}. "
            f"Create a held-out test file with the same columns as the training data."
        )

    df = pd.read_csv(csv_path)

    if "Label" not in df.columns:
        raise ValueError("Test CSV must contain a 'Label' column.")

    missing_feats = [c for c in FEATURE_COLS if c not in df.columns]
    if missing_feats:
        raise ValueError(f"Test CSV is missing feature columns: {missing_feats}")

    X = df[FEATURE_COLS].astype("float32").to_numpy()
    y = df["Label"].astype("int32").to_numpy()

    ds = tf.data.Dataset.from_tensor_slices((X, y)).batch(32)
    return ds, y


def main():
    print("[EVAL] Loading saved global model...")
    model = tf.keras.models.load_model(MODEL_PATH)

    # Compile for evaluation
    model.compile(
        optimizer="adam",
        loss=tf.keras.losses.SparseCategoricalCrossentropy(),
        metrics=[tf.keras.metrics.SparseCategoricalAccuracy()],
    )

    print(f"[EVAL] Loading test data from: {TEST_CSV_PATH}")
    test_ds, y_true = load_test_dataset(TEST_CSV_PATH)

    print("[EVAL] Running evaluation on test set...")
    results = model.evaluate(test_ds, verbose=0, return_dict=True)
    print(f"[EVAL] Test results: {results}")


    print("[EVAL] Generating predictions for confusion matrix...")
    y_pred_probs = model.predict(test_ds, verbose=0)
    y_pred = np.argmax(y_pred_probs, axis=1)

    # Confusion matrix
    conf_mat = tf.math.confusion_matrix(
        y_true, y_pred, num_classes=NUM_CLASSES
    ).numpy()

    print("\n[EVAL] Confusion matrix (rows = true labels, cols = predicted labels):")
    print(conf_mat)

    # Normalized version
    row_sums = conf_mat.sum(axis=1, keepdims=True) + 1e-8
    conf_mat_norm = conf_mat / row_sums

    print("\n[EVAL] Normalized confusion matrix:")
    np.set_printoptions(precision=3, suppress=True)
    print(conf_mat_norm)


if __name__ == "__main__":
    main()
