import numpy as np
import tensorflow as tf
from pathlib import Path
from sklearn.metrics import classification_report, confusion_matrix
from .central_baseline import (
    load_merged_dataset,
    make_train_test_split,
    FEATURE_COLUMNS,
    TARGET_COLUMN,
)

MODEL_PATH = Path("models_tff/manual_fedavg_global_model.keras")


def main():
    print("Loading merged dataset (same as baseline)...")
    df_all = load_merged_dataset()
    print(f"Total rows after cleanup: {len(df_all)}")

    print("Label distribution:")
    print(df_all[TARGET_COLUMN].value_counts())
    print(df_all[TARGET_COLUMN].value_counts(normalize=True))

    X_train, X_test, y_train, y_test = make_train_test_split(df_all)

    print(f"\nTest size: {len(X_test)}")

    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Federated model file not found: {MODEL_PATH}")

    print(f"\nLoading manual FedAvg global model from: {MODEL_PATH}")
    model = tf.keras.models.load_model(MODEL_PATH)

    print("\nEvaluating federated model on 20% held-out test set...")
    test_loss, test_acc = model.evaluate(X_test, y_test, verbose=0)
    print(f"Federated test loss: {test_loss:.4f}, Federated test accuracy: {test_acc:.4f}")

    y_pred_probs = model.predict(X_test)
    y_pred = np.argmax(y_pred_probs, axis=1)

    print("\nFederated model classification report:")
    print(classification_report(y_test, y_pred, digits=4))

    print("Federated model confusion matrix:")
    print(confusion_matrix(y_test, y_pred))


if __name__ == "__main__":
    main()
