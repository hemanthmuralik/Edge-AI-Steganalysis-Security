# Example usage (Linux / macOS)
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Create an encrypted stego image from text
python stego_encrypt.py --in examples/original.png --out examples/stego.png --text "edge-device-key-123"

# Show visual diff
python difference_map.py --orig examples/original.png --stego examples/stego.png --out examples/diff.png

# Extract and decrypt to file
python stego_decrypt.py --in examples/stego.png --out extracted.bin
