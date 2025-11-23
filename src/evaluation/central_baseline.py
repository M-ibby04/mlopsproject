import glob
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
import tensorflow as tf

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.utilis.experiment_tracker import log_experiment


# ==== CONFIG ====
# You can switch this between "Label" (pollution risk) and "StressLabel" (original WESAD)
TARGET_COLUMN = "Label"  # or "StressLabel"

FEATURE_COLUMNS = ["HeartRate", "Temp", "PM25", "NO2", "CO_Level"]

MERGED_DIR = Path("data/processed/merged_hospitals")
MODEL_OUT = Path("models_tff/baseline_central_model.keras")
MODEL_OUT.parent.mkdir(parents=True, exist_ok=True)


def load_merged_dataset() -> pd.DataFrame:
    """Load and concatenate all client_merged_*.csv files."""
    files = glob.glob(str(MERGED_DIR / "client_merged_*.csv"))
    if not files:
        raise FileNotFoundError(f"No merged files found in {MERGED_DIR}")

    dfs = [pd.read_csv(f) for f in files]
    df_all = pd.concat(dfs, ignore_index=True)

    # Drop any rows missing target or features (should be none after your cleaning)
    cols_to_check = FEATURE_COLUMNS + [TARGET_COLUMN]
    df_all = df_all.dropna(subset=cols_to_check).reset_index(drop=True)
    return df_all


def make_train_test_split(df: pd.DataFrame):
    """Create an 80/20 stratified split."""
    X = df[FEATURE_COLUMNS].to_numpy().astype("float32")
    y = df[TARGET_COLUMN].to_numpy().astype("int32")

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        shuffle=True,
        stratify=y,
    )

    return X_train, X_test, y_train, y_test


def build_baseline_model(num_features: int, num_classes: int) -> tf.keras.Model:
    """Simple dense network as a centralized baseline."""
    inputs = tf.keras.Input(shape=(num_features,), name="features")

    x = tf.keras.layers.Dense(32, activation="relu")(inputs)
    x = tf.keras.layers.Dense(32, activation="relu")(x)
    outputs = tf.keras.layers.Dense(num_classes, activation="softmax")(x)

    model = tf.keras.Model(inputs=inputs, outputs=outputs, name="central_baseline")

    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )
    return model


def main():
    print("Loading merged dataset...")
    df_all = load_merged_dataset()
    print(f"Total rows after cleanup: {len(df_all)}")

    print("Label distribution:")
    print(df_all[TARGET_COLUMN].value_counts())
    print(df_all[TARGET_COLUMN].value_counts(normalize=True))

    X_train, X_test, y_train, y_test = make_train_test_split(df_all)

    num_features = X_train.shape[1]
    num_classes = int(df_all[TARGET_COLUMN].nunique())

    print(f"\nTraining size: {len(X_train)}, Test size: {len(X_test)}")
    print(f"Num features: {num_features}, Num classes: {num_classes}")

    model = build_baseline_model(num_features, num_classes)

    print("\nFitting centralized baseline model...")
    history = model.fit(
        X_train,
        y_train,
        validation_split=0.1,
        epochs=30,
        batch_size=32,
        verbose=2,
    )

    print("\nEvaluating on 20% held-out test set...")
    test_loss, test_acc = model.evaluate(X_test, y_test, verbose=0)
    print(f"Test loss: {test_loss:.4f}, Test accuracy: {test_acc:.4f}")

    # Detailed metrics
    y_pred_probs = model.predict(X_test)
    y_pred = np.argmax(y_pred_probs, axis=1)

    print("\nClassification report:")
    print(classification_report(y_test, y_pred, digits=4))

    print("Confusion matrix:")
    print(confusion_matrix(y_test, y_pred))
    # ---- Experiment tracking ----
    val_loss = float(history.history["val_loss"][-1])
    val_accuracy = float(history.history["val_accuracy"][-1])

    metrics = {
        "val_loss": val_loss,
        "val_accuracy": val_accuracy,
        "test_loss": float(test_loss),
        "test_accuracy": float(test_acc),
    }

    params = {
        "epochs": 30,
        "batch_size": 32,
        "learning_rate": 1e-3,
        "num_features": num_features,
    }

    log_experiment("central_baseline", metrics, params)

    # Save the model so you can compare later
    model.save(MODEL_OUT)
    print(f"\nSaved centralized baseline model to: {MODEL_OUT}")


if __name__ == "__main__":
    main()
