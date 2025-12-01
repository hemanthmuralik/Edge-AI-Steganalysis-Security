import tensorflow as tf
import os

def export_to_tflite(model_path='steganalysis_model.h5', output_path='model_quantized.tflite'):
    print(f"Loading model from {model_path}...")
    model = tf.keras.models.load_model(model_path, custom_objects={'HPFLayer': HPFLayer}) # Note: You need the HPFLayer class defined here or imported

    print("Converting to TFLite with Quantization...")
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    
    # OPTIMIZATION: Quantize weights from Float32 -> Int8
    # This reduces model size by 4x and speeds up inference on CPU/Edge TPU
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    
    tflite_model = converter.convert()

    # Save the file
    with open(output_path, 'wb') as f:
        f.write(tflite_model)
    
    print(f"Success! Saved quantized model to {output_path}")
    print(f"Original Size: {os.path.getsize(model_path) / 1024:.2f} KB")
    print(f"Edge Size: {os.path.getsize(output_path) / 1024:.2f} KB")

# To use this, you need to paste the HPFLayer class definition (from Step 1) 
# into this file as well so Keras knows how to load it.
if __name__ == "__main__":
    # Ensure you have trained and saved 'steganalysis_model.h5' first
    export_to_tflite()
