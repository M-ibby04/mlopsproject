import pathlib

import numpy as np
import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
import tensorflow as tf

# Paths
MERGED_DIR = pathlib.Path("data/processed/merged_hospitals")
MODEL_PATH = pathlib.Path("models_tff/manual_fedavg_global_model.keras")

FEATURE_COLS = ["HeartRate", "Temp", "PM25", "NO2", "CO_Level"]
LABEL_COL = "Label"
TEST_SIZE = 0.2
RANDOM_STATE = 42


def load_merged_dataset() -> pd.DataFrame:
    """Load and concatenate all merged_hospitals clients into a single DataFrame."""
    csv_files = sorted(MERGED_DIR.glob("client_merged_*.csv"))
    if not csv_files:
        raise FileNotFoundError(f"No merged client CSVs found in {MERGED_DIR}")

    dfs = []
    for f in csv_files:
        df = pd.read_csv(f)
        print(f"Loaded {f.name}: {len(df)} rows")
        dfs.append(df)

    df_all = pd.concat(dfs, ignore_index=True)
    print(f"\nTotal merged rows: {len(df_all)}")
    print("Label distribution:")
    print(df_all[LABEL_COL].value_counts())
    print(df_all[LABEL_COL].value_counts(normalize=True).rename("proportion"))
    return df_all


def make_train_test(df: pd.DataFrame):
    """Split into 80/20 train/test, but we only use test for evaluating this model."""
    X = df[FEATURE_COLS].values.astype("float32")
    y = df[LABEL_COL].values.astype("int64")

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=y,
    )

    print(f"\nTrain size: {len(X_train)}, Test size: {len(X_test)}")
    return X_train, X_test, y_train, y_test


def load_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Model not found at {MODEL_PATH}")

    print(f"\nLoading manual FedAvg model from: {MODEL_PATH}")
    model = tf.keras.models.load_model(MODEL_PATH)

    # Compile for evaluation
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )
    return model


def main():
    # 1) Load data
    df_all = load_merged_dataset()

    # 2) Train/test split (we only use test set for evaluation)
    _, X_test, _, y_test = make_train_test(df_all)

    # 3) Load manual FedAvg global model
    model = load_model()

    # 4) Evaluate
    print("\nEvaluating manual FedAvg model on 20% held-out test set...")
    test_loss, test_acc = model.evaluate(X_test, y_test, verbose=0)
    print(f"Test loss: {test_loss:.4f}, Test accuracy: {test_acc:.4f}")

    # 5) Detailed metrics
    y_pred_probs = model.predict(X_test, verbose=0)
    y_pred = np.argmax(y_pred_probs, axis=1)

    print("\nClassification report:")
    print(classification_report(y_test, y_pred, digits=4))

    print("Confusion matrix:")
    print(confusion_matrix(y_test, y_pred))

    # === Save predictions for notebook EDA ===

    OUT_DIR = pathlib.Path("data/processed/eval")
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    preds_path = OUT_DIR / "manual_fedavg_test_predictions.csv"

    # Rebuild a DataFrame with features, true label, and predicted label
    df_test = pd.DataFrame(X_test, columns=["HeartRate", "Temp", "PM25", "NO2", "CO_Level"])
    df_test["Label"] = y_test
    df_test["PredLabel"] = y_pred

    df_test.to_csv(preds_path, index=False)
    print(f"\nSaved test predictions for EDA to: {preds_path}")



if __name__ == "__main__":
    main()
