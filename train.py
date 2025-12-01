import tensorflow as tf
from tensorflow.keras import layers, models, regularizers
import numpy as np

# --- 1. Define the Preprocessing Layer (The "SRM" Filter) ---
# This filter removes image content and keeps only the noise residuals.
# It makes the model converge much faster and accurate.
def get_srm_filter_weights():
    # A standard 5x5 High-Pass Filter used in Steganalysis (KV Kernel)
    # It calculates the difference between a pixel and its neighbors.
    filter_weights = np.array([
        [-1,  2, -2,  2, -1],
        [ 2, -6,  8, -6,  2],
        [-2,  8, -12, 8, -2],
        [ 2, -6,  8, -6,  2],
        [-1,  2, -2,  2, -1]
    ], dtype=np.float32) / 12.0
    
    # Reshape to (Height, Width, Input_Channels, Output_Channels)
    # Assuming RGB input (3 channels), we apply the same filter to each.
    return np.repeat(filter_weights[:, :, np.newaxis, np.newaxis], 3, axis=2)

class HPFLayer(layers.Layer):
    def __init__(self, **kwargs):
        super(HPFLayer, self).__init__(**kwargs)
    
    def build(self, input_shape):
        self.kernel = self.add_weight(
            name='hpf_kernel',
            shape=(5, 5, 3, 1), # 5x5 kernel, 3 input channels (RGB), 1 output
            initializer=lambda shape, dtype: get_srm_filter_weights(),
            trainable=False # IMPORTANT: We freeze this! Don't learn it.
        )
        super(HPFLayer, self).build(input_shape)

    def call(self, inputs):
        # Apply the filter to extract residuals
        return tf.nn.depthwise_conv2d(inputs, self.kernel, strides=[1, 1, 1, 1], padding='SAME')

# --- 2. Build the Efficient "Edge" Model ---
def create_improved_model(input_shape=(128, 128, 3)):
    model = models.Sequential()
    
    # Block 1: The Steganalysis Front-End
    model.add(layers.Input(shape=input_shape))
    model.add(HPFLayer()) # <--- CUSTOM LAYER ADDED HERE
    
    # Block 2: Feature Extraction (Using SeparableConv2D for Speed/Edge)
    # Separable Convs use ~9x fewer parameters than standard Convs.
    model.add(layers.SeparableConv2D(16, (3, 3), padding='same'))
    model.add(layers.BatchNormalization())
    model.add(layers.Activation('relu'))
    model.add(layers.MaxPooling2D((2, 2)))
    
    model.add(layers.SeparableConv2D(32, (3, 3), padding='same'))
    model.add(layers.BatchNormalization())
    model.add(layers.Activation('relu'))
    model.add(layers.MaxPooling2D((2, 2)))
    
    model.add(layers.SeparableConv2D(64, (3, 3), padding='same'))
    model.add(layers.BatchNormalization())
    model.add(layers.Activation('relu'))
    model.add(layers.MaxPooling2D((2, 2)))
    
    # Block 3: Classification
    model.add(layers.GlobalAveragePooling2D()) # Better than Flatten()
    model.add(layers.Dense(64, activation='relu', kernel_regularizer=regularizers.l2(0.001)))
    model.add(layers.Dropout(0.5))
    model.add(layers.Dense(1, activation='sigmoid')) # Binary: Cover vs Stego

    model.compile(optimizer='adam',
                  loss='binary_crossentropy',
                  metrics=['accuracy'])
    
    return model

# Usage inside your training loop:
# model = create_improved_model()
# model.summary()
