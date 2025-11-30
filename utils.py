# Utility functions for simple LSB embed/extract and preprocessing
import numpy as np
from PIL import Image

def embed_lsb(image: np.ndarray, payload: bytes) -> np.ndarray:
    """Embed payload bytes into image using LSB on the red channel.
    image: HxWx3 uint8
    payload: bytes to embed (will be truncated if too long)
    Returns a new image array with embedded payload.
    """
    arr = image.copy().astype(np.uint8)
    h,w,_ = arr.shape
    max_bits = h*w  # using one bit per pixel (red channel)
    payload_bits = []
    for b in payload:
        for i in range(8):
            payload_bits.append((b >> (7-i)) & 1)
    # add delimiter 16 zeros to mark end
    payload_bits += [0]*16
    if len(payload_bits) > max_bits:
        payload_bits = payload_bits[:max_bits]
    flat = arr[:,:,0].flatten()  # red channel
    for i,bit in enumerate(payload_bits):
        flat[i] = (flat[i] & ~1) | bit
    arr[:,:,0] = flat.reshape(h,w)
    return arr

def extract_lsb(image: np.ndarray, max_bytes=1024) -> bytes:
    arr = image.astype(np.uint8)
    flat = arr[:,:,0].flatten()
    bits = [int(x&1) for x in flat[:max_bytes*8]]
    # convert to bytes until delimiter of 16 zeros
    out_bytes = []
    cur = 0
    for i,bit in enumerate(bits):
        cur = (cur<<1) | bit
        if (i+1) % 8 == 0:
            out_bytes.append(cur & 0xFF)
            cur = 0
            if len(out_bytes) >= 2 and out_bytes[-2:] == [0,0]:
                break
    return bytes(out_bytes)

def load_image(path, size=None):
    img = Image.open(path).convert('RGB')
    if size is not None:
        img = img.resize(size, Image.BILINEAR)
    return np.array(img)

def save_image(arr, path):
    Image.fromarray(arr.astype('uint8')).save(path)
