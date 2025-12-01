# Edge-AI Steganalysis Security Framework

[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-orange.svg)](https://tensorflow.org)
[![Edge AI](https://img.shields.io/badge/Edge_AI-TFLite-green)](https://www.tensorflow.org/lite)
[![Security](https://img.shields.io/badge/Security-Steganalysis-red)](https://en.wikipedia.org/wiki/Steganalysis)

A lightweight, high-performance Deep Learning framework designed to detect **covert data (steganography)** in digital images. This system is optimized for **Edge Devices** (Raspberry Pi, IoT, Mobile) using specific architectural optimizations like Separable Convolutions and Int8 Quantization.

## 🚀 Key Features

### 1. Edge-Native Architecture
Unlike standard heavy CNNs, this model uses **Depthwise Separable Convolutions**, reducing parameter count by **~85%**. It includes an automated pipeline (`export_edge.py`) to convert and quantize the model into **TensorFlow Lite (Int8)** format, ensuring real-time inference on low-power hardware.

### 2. Forensic High-Pass Filtering (HPF)
Standard AI models get distracted by image content (colors, shapes). This model implements a fixed **SRM (Spatial Rich Model) High-Pass Filter** layer at the input.
* **Action:** It suppresses the image content and isolates the **noise residuals**.
* **Result:** The model "sees" the hidden steganographic noise regardless of whether the image is a cat, a landscape, or a document.

### 3. Advanced Randomized Attacks
The data generation engine (`stego_encrypt.py`) creates realistic training data using **Randomized LSB Embedding**.
* **Old Method:** Hiding data sequentially (pixels 1, 2, 3...). *Easy to detect.*
* **New Method:** Cryptographically shuffling pixel coordinates based on a seed. *Hard to detect.*

## 🧠 System Architecture

The pipeline consists of three stages:

1.  **Preprocessing (The "Forensic Lens"):**
    * Input: RGB Image ($128 \times 128 \times 3$)
    * Layer: Fixed 5x5 High-Pass Kernel (Kv Filter)
    * Output: Noise Residual Map

2.  **Feature Extraction (The "Edge Brain"):**
    * 3 Blocks of **SeparableConv2D** + Batch Normalization + ReLU.
    * Global Average Pooling (replaces heavy Dense layers).

3.  **Deployment (The "Edge Export"):**
    * Trained `.h5` models are converted to `.tflite`.
    * Weights are quantized to `int8` for 4x size reduction.

## 📂 Repository Structure

```bash
├── stego_encrypt.py   # Generates dataset using Randomized LSB injection
├── train.py           # Defines and trains the Edge-Optimized CNN with HPF
├── export_edge.py     # Converts trained model to TFLite (Quantized)
├── stego_decrypt.py   # Decodes hidden messages from images
├── difference_map.py  # Visualization tool for pixel anomalies
└── examples/          # Sample Cover and Stego images
⚡ Quick Start1. Generate DataCreate a steganographic image with hidden data scattered randomly.Bashpython stego_encrypt.py --cover assets/clean.jpg --message "Secret Payload" --output assets/stego.png
2. Train the ModelTrain the forensic CNN. The High-Pass Filter is initialized automatically.Bashpython train.py
3. Export for EdgeConvert the trained model to a lightweight TFLite file for mobile/IoT deployment.Bashpython export_edge.py
# Output: stego_security_edge.tflite (~50KB size)
📊 Performance (Projected)MetricStandard CNNOur Edge ModelModel Size~2.5 MB~0.4 MBInference Speed45ms12msLSB Detection Acc78%94%🛠️ Tech StackDeep Learning: TensorFlow 2.x, KerasEdge Deployment: TensorFlow Lite (TFLite)Image Processing: OpenCV, NumPyVisualization: Matplotlib📜 LicenseThis project is licensed under the MIT License.
