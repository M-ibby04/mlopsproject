import tensorflow as tf
import tensorflow_federated as tff

NUM_FEATURES = 5
NUM_CLASSES = 8

# Change to a standard Python list (no tf.constant yet!)
# The TFF wrapper is fine with global Python lists/ints/strings.
RAW_CLASS_WEIGHTS = [1.0, 3.0, 3.0, 4.0, 4.0, 6.0, 6.0, 6.0] 


def create_keras_model() -> tf.keras.Model:
    """Stronger MLP with dropout for federated learning."""
    return tf.keras.Sequential([
        tf.keras.layers.Input(shape=(NUM_FEATURES,)),
        tf.keras.layers.BatchNormalization(),

        tf.keras.layers.Dense(256, activation="relu"),
        tf.keras.layers.Dropout(0.3),

        tf.keras.layers.Dense(128, activation="relu"),
        tf.keras.layers.Dropout(0.3),

        tf.keras.layers.Dense(64, activation="relu"),
        tf.keras.layers.Dropout(0.3),

        tf.keras.layers.Dense(NUM_CLASSES, activation="softmax"),
    ])


class WeightedSparseCategoricalCrossentropy(tf.keras.losses.Loss):
    """Class-weighted sparse categorical crossentropy loss."""

    def __init__(self, class_weights, from_logits=False, name="weighted_sparse_cce"):
        super().__init__(name=name, reduction=tf.keras.losses.Reduction.NONE)
        
        # --- FIX IS HERE ---
        # Convert to Tensor inside the init method, which TFF correctly wraps.
        self.class_weights = tf.constant(class_weights, dtype=tf.float32)
        
        self.from_logits = from_logits
        self.base_loss = tf.keras.losses.SparseCategoricalCrossentropy(
            from_logits=from_logits,
            reduction=tf.keras.losses.Reduction.NONE,
        )

    def call(self, y_true, y_pred):
        y_true = tf.cast(y_true, tf.int32)
        
        # shape: [batch]
        # This will now correctly use the Tensor created in __init__
        weights = tf.gather(self.class_weights, y_true) 
        unweighted = self.base_loss(y_true, y_pred)  # [batch]
        return unweighted * tf.cast(weights, unweighted.dtype)


def model_fn(input_spec):
    """Wrap the Keras model into a TFF model."""
    keras_model = create_keras_model()

    # Pass the Python list here
    loss_obj = WeightedSparseCategoricalCrossentropy(RAW_CLASS_WEIGHTS) 

    return tff.learning.models.from_keras_model(
        keras_model=keras_model,
        input_spec=input_spec,
        loss=loss_obj,
        metrics=[tf.keras.metrics.SparseCategoricalAccuracy()],
    )