# Secure-Edge-Steganography (AES-256 + LSB)

This upgraded project demonstrates a secure steganography workflow suitable for Edge/Embedded profiles:
- **AES-256-GCM** encryption of payloads before embedding (confidentiality + integrity).
- **LSB-based** embedding into PNG images (simple, educational).
- **Difference map** visualization showing where bits changed (for README/proof).

## Contents
- `stego_encrypt.py` — encrypt a file/text and embed into an image.
- `stego_decrypt.py` — extract bytes from an image and decrypt.
- `difference_map.py` — produce a visual difference map between original and stego images.
- `utils/aes_utils.py` — AES-256-GCM helper functions.
- `utils/lsb_utils.py` — LSB embedding/extraction helpers (red channel).
- `examples/` — contains a generated example original image, the produced stego image, and diff image.
- `requirements.txt`, `example_usage.sh`, `LICENSE`.

## Quickstart
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Embed a secret text into an image (you will be prompted for a passphrase)
python stego_encrypt.py --in examples/original.png --out examples/stego.png --text "my secret command key"

# Visualize difference map
python difference_map.py --orig examples/original.png --stego examples/stego.png --out examples/diff.png

# Extract and decrypt (use the same passphrase)
python stego_decrypt.py --in examples/stego.png --out extracted.bin
```

## Notes & Limitations
- Embedding capacity depends on image size: we use one bit per pixel (red channel). For a 256x256 image capacity is 65536 bits -> 8192 bytes.
- AES-256-GCM provides both confidentiality and integrity (tag verified on decrypt).
- This project is educational: for production use consider stronger cover strategies, better embedding, and steganography-aware preprocessing.

## License
MIT.
