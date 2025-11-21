import numpy as np
import pandas as pd
import tensorflow as tf
import tensorflow_federated as tff
from glob import glob
import os

# Create directory for saving the model if it doesn't exist
os.makedirs("models_tff", exist_ok=True)


# ======================
# 1. Load merged hospital CSVs
# ======================
def load_merged_clients():
    """Loads and preprocesses client data, simulating the two-headed model input."""
    # Make sure this path matches where your docker container sees the data
    files = glob("data/processed/merged_hospitals/client_merged_*.csv")
    clients = {}

    print(f"Debug: Looking for files in data/processed/merged_hospitals/...")
    if not files:
        print("WARNING: No client files found! Make sure the path is correct.")

    for f in files:
        # Read CSV
        df = pd.read_csv(f)
        
        # Ensure we only get the columns we expect
        # (HeartRate, Temp, PM25, NO2, CO_Level, Label)
        df = df[["HeartRate", "Temp", "PM25", "NO2", "CO_Level", "Label"]]
        clients[f] = df

    return clients


# ======================
# 2. Convert DataFrame → TFF dataset
# ======================
def df_to_tff_dataset(df: pd.DataFrame, batch_size=8):
    """Converts a DataFrame into a TFF-compatible TensorFlow Dataset."""
    
    # 5 Features: Health (Heart, Temp) + Environment (PM2.5, NO2, CO)
    features = df[["HeartRate", "Temp", "PM25", "NO2", "CO_Level"]].values.astype(np.float32)
    
    # 1 Label: Risk Score
    labels = df["Label"].values.astype(np.int32)

    # Create dataset
    ds = tf.data.Dataset.from_tensor_slices((features, labels))
    
    # Shuffle, Batch, and Repeat (Repeat is needed for multi-epoch simulation)
    return ds.shuffle(len(df)).batch(batch_size).repeat()


# ======================
# 3. Build Keras model architecture
# ======================
def create_keras_model():
    """Defines the Neural Network structure."""
    return tf.keras.Sequential([
        # Input Layer: 5 inputs
        tf.keras.layers.Input(shape=(5,)),
        
        # Hidden Layers
        tf.keras.layers.Dense(32, activation="relu"),
        tf.keras.layers.Dense(16, activation="relu"),
        
        # Output Layer: 3 categories (Low, Medium, High Risk)
        tf.keras.layers.Dense(3, activation="softmax")
    ])


# ======================
# 4. Wrap model for TFF
# ======================
def model_fn():
    """Wraps the Keras model so TFF can use it."""
    keras_model = create_keras_model()

    return tff.learning.models.from_keras_model(
        keras_model,
        # This Input Spec tells TFF what shape of data to expect
        # (Batch_Size=None, Features=5) and (Batch_Size=None, Label=1)
        input_spec=(
            tf.TensorSpec(shape=(None, 5), dtype=tf.float32),
            tf.TensorSpec(shape=(None,), dtype=tf.int32)
        ),
        loss=tf.keras.losses.SparseCategoricalCrossentropy(),
        metrics=[tf.keras.metrics.SparseCategoricalAccuracy()]
    )


# ======================
# 5. MAIN TRAINING LOOP
# ======================
def main():
    print("--- Starting TFF Server ---")
    
    # A. Load Data
    clients = load_merged_clients()
    client_ids = list(clients.keys())
    
    if len(client_ids) == 0:
        print("Error: No data found. Exiting.")
        return

    print(f"Found {len(client_ids)} merged clients")

    # B. Convert to TFF Datasets
    tff_client_data = {
        k: df_to_tff_dataset(v) for k, v in clients.items()
    }

    # C. Build the Federated Averaging Algorithm
    # FIX: We use Standard Keras Optimizers here to avoid the AttributeError
    print("Building TFF FedAvg process...")

    iterative_process = tff.learning.algorithms.build_weighted_fed_avg(
        model_fn=model_fn,
        client_optimizer_fn=lambda: tf.keras.optimizers.Adam(learning_rate=0.001),
        server_optimizer_fn=lambda: tf.keras.optimizers.Adam(learning_rate=1.0)
    )

    # D. Initialize the Server State
    print("Initializing server state...")
    state = iterative_process.initialize()
    
    # E. Run Training Rounds
    NUM_ROUNDS = 10  # You can increase this later
    print(f"Starting training for {NUM_ROUNDS} rounds...")

    for round_num in range(1, NUM_ROUNDS + 1):
        # In this simulation, we use ALL clients in every round
        federated_data = [tff_client_data[c] for c in client_ids]

        # Run one round of training
        result = iterative_process.next(state, federated_data)
        
        # Update state (weights)
        state = result.state
        metrics = result.metrics

        # Print accuracy/loss
        # Structure depends on TFF version, usually: metrics['client_work']['eval']['current_round_metrics']
        print(f"Round {round_num}: Loss={metrics['client_work']['loss']:.4f}, Accuracy={metrics['client_work']['sparse_categorical_accuracy']:.4f}")

    # F. Save the Final Model
    print("\nTraining complete. Saving model...")
    
    # We must create a fresh Keras model to hold the final weights
    final_keras_model = create_keras_model()
    
    # Extract weights from the TFF state and assign to Keras model
    final_weights = iterative_process.get_model_weights(state)
    final_weights.assign_weights_to(final_keras_model)

    # Compile it so it's ready to use for predictions
    final_keras_model.compile(
        optimizer=tf.keras.optimizers.Adam(0.001),
        loss=tf.keras.losses.SparseCategoricalCrossentropy(),
        metrics=[tf.keras.metrics.SparseCategoricalAccuracy()]
    )

    # Save to .keras format (Standard for Keras 3) or .h5
    save_path = "models_tff/tff_global_model.keras"
    final_keras_model.save(save_path)
    print(f"SUCCESS: Global model saved to {save_path}")


if __name__ == "__main__":
    main()