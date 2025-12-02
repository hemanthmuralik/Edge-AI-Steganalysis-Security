import tensorflow as tf
from tensorflow.keras import layers, models, regularizers
import numpy as np

# 1. Define the TLU (Truncated Linear Unit) - The "Secret Sauce" of Ye-Net
def tlu(x, threshold=3.0):
    # Instead of killing negative values like ReLU, we clamp them.
    # This preserves the "negative" noise residuals which are crucial for detection.
    return tf.maximum(tf.minimum(x, threshold), -threshold)

# 2. Define the SRM Filters (The "Forensic Lens")
def get_srm_weights():
    # 30 Basic SRM filters used in research (simplified 3x for brevity)
    # In a real deployment, you load the full 30 kernels.
    # Here we initialize random high-pass filters for demonstration.
    return np.random.randn(5, 5, 3, 30).astype(np.float32)

class YeNetPreprocessing(layers.Layer):
    def __init__(self, **kwargs):
        super(YeNetPreprocessing, self).__init__(**kwargs)

    def build(self, input_shape):
        self.kernel = self.add_weight(
            name='srm_kernel',
            shape=(5, 5, 3, 30),
            initializer=lambda shape, dtype: get_srm_weights(),
            trainable=False # Keep fixed!
        )
        super(YeNetPreprocessing, self).build(input_shape)

    def call(self, inputs):
        return tf.nn.conv2d(inputs, self.kernel, strides=[1, 1, 1, 1], padding='SAME')

# 3. Build the Architecture
def build_yenet(input_shape=(128, 128, 3)):
    inputs = layers.Input(shape=input_shape)
    
    # Layer 1: Preprocessing (SRM) + TLU
    x = YeNetPreprocessing()(inputs)
    x = layers.Activation(tlu)(x) # <--- USING TLU HERE
    
    # Layer 2: Separable Convs (Edge Optimization)
    x = layers.SeparableConv2D(30, (3, 3), padding='same')(x)
    x = layers.Activation(tlu)(x)
    x = layers.AveragePooling2D(pool_size=(2, 2))(x)
    
    # Layer 3
    x = layers.SeparableConv2D(30, (3, 3), padding='same')(x)
    x = layers.Activation(tlu)(x)
    x = layers.AveragePooling2D(pool_size=(2, 2))(x)
    
    # Classifier
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dense(64, activation=tlu)(x)
    outputs = layers.Dense(1, activation='sigmoid')(x)
    
    model = models.Model(inputs=inputs, outputs=outputs)
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model
