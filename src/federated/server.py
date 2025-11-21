import os

import tensorflow as tf
import tensorflow_federated as tff

from .client import build_federated_data
from .model import model_fn, create_keras_model


def main():
    # 1. Build federated datasets (one per client/node)
    federated_data = build_federated_data()
    if len(federated_data) == 0:
        raise RuntimeError("No client datasets found. Check your data/processed folders.")

    print(f"[TFF] Total clients: {len(federated_data)}")

    # 2. Get input_spec from one client to configure TFF model
    input_spec = federated_data[0].element_spec

    # 3. Build TFF FedAvg training process with TFF optimizers
    client_optimizer = tff.learning.optimizers.build_adam(learning_rate=0.002)
    server_optimizer = tff.learning.optimizers.build_sgdm(learning_rate=1.0)

    iterative_process = tff.learning.algorithms.build_weighted_fed_avg(
        model_fn=lambda: model_fn(input_spec),
        client_optimizer_fn=client_optimizer,
        server_optimizer_fn=server_optimizer,
    )

    state = iterative_process.initialize()

    # 4. Run more FL rounds so the model can actually learn
    NUM_ROUNDS = 120
    for round_num in range(1, NUM_ROUNDS + 1):
        result = iterative_process.next(state, federated_data)
        state = result.state
        print(f"[TFF] Round {round_num} metrics: {result.metrics}")

    # 5. Extract final global model weights and save Keras model
    keras_model = create_keras_model()
    final_weights = iterative_process.get_model_weights(state)
    final_weights.assign_weights_to(keras_model)

    os.makedirs("models_tff", exist_ok=True)
    out_path = "models_tff/tff_global_model"
    keras_model.save(out_path)
    print(f"[TFF] Saved global TFF model -> {out_path}")


if __name__ == "__main__":
    main()
