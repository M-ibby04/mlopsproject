import tensorflow as tf

# --------------------------
# Model constants
# --------------------------
NUM_FEATURES = 5
NUM_CLASSES = 8

# Raw class weights (simple Python list)
RAW_CLASS_WEIGHTS = [1.0, 3.0, 3.0, 4.0, 4.0, 6.0, 6.0, 6.0]


# --------------------------
# Model creation
# --------------------------
def create_keras_model() -> tf.keras.Model:
    """Standalone Keras model (no TFF)."""
    return tf.keras.Sequential(
        [
            tf.keras.layers.Input(shape=(NUM_FEATURES,)),
            tf.keras.layers.BatchNormalization(),
            tf.keras.layers.Dense(256, activation="relu"),
            tf.keras.layers.Dropout(0.3),
            tf.keras.layers.Dense(128, activation="relu"),
            tf.keras.layers.Dropout(0.3),
            tf.keras.layers.Dense(64, activation="relu"),
            tf.keras.layers.Dropout(0.3),
            tf.keras.layers.Dense(NUM_CLASSES, activation="softmax"),
        ]
    )


# --------------------------
# Weighted Loss Function
# --------------------------
class WeightedSparseCategoricalCrossentropy(tf.keras.losses.Loss):
    """Class-weighted sparse categorical crossentropy loss."""

    def __init__(self, class_weights, from_logits=False, name="weighted_sparse_cce"):
        super().__init__(name=name, reduction=tf.keras.losses.Reduction.NONE)

        # Convert weights to tensor here
        self.class_weights = tf.constant(class_weights, dtype=tf.float32)
        self.from_logits = from_logits

        self.base_loss = tf.keras.losses.SparseCategoricalCrossentropy(
            from_logits=from_logits,
            reduction=tf.keras.losses.Reduction.NONE,
        )

    def call(self, y_true, y_pred):
        y_true = tf.cast(y_true, tf.int32)
        unweighted = self.base_loss(y_true, y_pred)
        weights = tf.gather(self.class_weights, y_true)

        return unweighted * tf.cast(weights, unweighted.dtype)


# --------------------------
# Wrapper for your MANUAL FedAvg code
# --------------------------
def build_compiled_model():
    """
    This is what your manual FedAvg server/client should call.
    It creates and compiles the model with weighted loss.
    """
    model = create_keras_model()

    loss_obj = WeightedSparseCategoricalCrossentropy(RAW_CLASS_WEIGHTS)

    model.compile(
        optimizer=tf.keras.optimizers.Adam(),
        loss=loss_obj,
        metrics=[tf.keras.metrics.SparseCategoricalAccuracy()],
    )

    return model
