# file: stego_encrypt.py
import cv2
import numpy as np
import os
import random

def to_bin(data):
    """Convert string to binary."""
    if isinstance(data, str):
        return ''.join([format(ord(i), "08b") for i in data])
    elif isinstance(data, bytes):
        return ''.join([format(i, "08b") for i in data])
    elif isinstance(data, np.ndarray):
        return [format(i, "08b") for i in data]
    elif isinstance(data, int) or isinstance(data, np.uint8):
        return format(data, "08b")
    else:
        raise TypeError("Input type not supported")

def encrypt_image_random(image_path, secret_message, output_path):
    """
    Embeds data into random pixels rather than sequential ones.
    This mimics more advanced steganography and prevents the model
    from just memorizing the top-left corner of images.
    """
    img = cv2.imread(image_path)
    if img is None:
        print(f"Error: Could not read {image_path}")
        return

    # Add a delimiter so we know when the message ends
    secret_message += "#####" 
    data_bin = to_bin(secret_message)
    data_len = len(data_bin)
    
    height, width, channels = img.shape
    total_pixels = height * width
    
    if data_len > total_pixels * 3:
        raise ValueError("Insufficient pixels to hold data")

    # --- THE UPGRADE: Randomize Coordinates ---
    # Create a list of all (x, y) coordinates
    coords = [(x, y) for x in range(height) for y in range(width)]
    # Shuffle them securely based on a seed (optional: use a key)
    random.seed(42) 
    random.shuffle(coords)

    data_index = 0
    
    # Iterate through random pixels
    for x, y in coords:
        if data_index < data_len:
            # Modify the Blue channel (channel 0)
            pixel = img[x, y]
            # specific LSB modification
            pixel[0] = int(to_bin(pixel[0])[:-1] + data_bin[data_index], 2)
            data_index += 1
        else:
            break
            
    cv2.imwrite(output_path, img)
    print(f"Data embedded into {output_path} using Randomized LSB.")

# Example usage
# encrypt_image_random("examples/cover.jpg", "Secret Agent Data", "examples/stego.png")
