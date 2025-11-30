# AI-Powered Steganalysis (Easy)

This repo contains a **simple, easy-to-run** AI steganalysis project (detects LSB stego images).
It is designed as the *easiest* path from your C steganography tool to an AI-relevant project.

## What is included
- `dataset_gen.py` — generates a dataset of clean/stego image pairs using CIFAR-10,
  and writes images into `data/clean` and `data/stego`.
- `train.py` — trains a small CNN classifier (Keras/TensorFlow) to detect stego images.
- `detect.py` — runs the trained model on a single image and prints confidence.
- `utils.py` — helper functions: simple LSB embed/extract and preprocessing.
- `requirements.txt` — Python dependencies.
- `LICENSE` — MIT license.
- `example_usage.sh` — example commands to generate dataset, train and run detection.

## Quickstart (example)
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# generate dataset (creates ./data with clean and stego dirs)
python dataset_gen.py --outdir ./data --num 2000

# train (saves model to model.h5)
python train.py --data ./data --epochs 10 --batch_size 64

# test on an image
python detect.py --model model.h5 --image ./data/clean/0000.png
```

## Notes
- The dataset generator uses CIFAR-10 (small images, fast to run). You can replace it with your own images (BMP/PNG) or use the C tool to create stego images — just put them into the folders `data/clean` and `data/stego` with matching sizes.
- This is intentionally minimal and educational. To make it research-grade, consider:
  - Larger datasets, transfer learning, or custom preprocessing (high-pass filters used in steganalysis).
  - Using your original BMP-based C stego generator to produce the stego dataset for more realistic results.
  - Adding model evaluation, cross-validation, and a training notebook.

If you want, I can also:
- Add a tiny Flask UI for inference.
- Convert the trained model to TFLite for edge deployment (Raspberry Pi / ESP32).
- Create a README badge, diagram PNG, or a polished GitHub-ready README.
