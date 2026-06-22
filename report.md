# Deepfake Detection System - Project Report

## Project Overview
This project is an advanced Deepfake Detection System integrating multiple CNN models (EfficientNet) and Frequency Domain Analysis (Fast Fourier Transform) to distinguish between real photographs and AI-generated or manipulated images/videos. The application provides a polished, forensic-style dark theme UI built using Streamlit.

## Architecture

### 1. CNN Ensemble Engine (`utils/ensemble.py`)
The system employs an ensemble of 3 independent CNN models loaded from HuggingFace to classify media:
- **GAN Face Detector** (`dima806/deepfake_vs_real_image_detection`)
- **AI Image Detector** (`haywoodsloan/ai-image-detector-deploy`)
- **SDXL Detector** (`Organika/sdxl-detector`)

*Mechanism:* Each CNN classifier casts a single vote (Real/Fake). The predictions are aggregated to minimize false positives, increasing overall detection accuracy compared to singlemodel systems.

### 2. Spectral Analysis Module (`utils/frequency_analysis.py`)
This module provides a secondary detection mechanism based on the 2D Fast Fourier Transform (FFT).
- **Core Concept:** Real photographs contain natural noise across all frequency bands, whereas AI-generated images exhibit unnaturally uniform frequency distributions. 
- **Mechanism:** It computes the FFT of the grayscale image, checking the variance and high-frequency energy ratio to spot AI spectral signatures. If suspicious patterns are detected, this score contributes an additional weighted "soft vote" to the CNN ensemble.

### 3. Media Processing (`utils/preprocessor.py`, `utils/video_utils.py`)
- **Images:** Uploaded images are strictly validated to catch corruptions, converted to RGB, and resized (using `LANCZOS` resampling) to the `224x224` format expected by the EfficientNet pipelines.
- **Videos:** The system extracts up to 8 evenly spaced frames from an uploaded `.mp4`, `.avi`, or `.mov` file using `OpenCV`. It then processes each frame individually through the ensemble engine and frequency analyzer. The final video verdict is based on a majority vote of those key frames.

### 4. User Interface (`app.py`, `styles/theme.py`)
- **Framework:** `streamlit`
- **Design:** The platform features a customized "Dark Forensic UI" injecting bespoke CSS classes for a professional, analytical aesthetic.
- **Explainability:** Displays confidence metrics, an explicit breakdown of per-model votes, and granular metrics regarding frequency analysis. The detailed diagnostics are aimed at providing interpretable machine learning rather than a "black-box" decision.

## Dependencies & Setup

The system requires Python 3.9+ and the following core dependencies:
- `streamlit>=1.32.0`
- `transformers>=4.38.0`
- `torch>=2.0.0`
- `torchvision>=0.15.0`
- `Pillow>=10.0.0`
- `opencv-python>=4.8.0`
- `numpy>=1.24.0`
- `pandas>=2.0.0`

### Running the application
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Known Limitations
1. **Compression:** Significant media compression (like WhatsApp or standard social media processing) can degrade accuracy, particularly impairing the frequency domain analysis.
2. **Evolving Baselines:** Rapidly advancing Generative AI architectures could outsmart current CNN training data boundaries.
3. **Face Restrictions:** The pipeline performs optimally on clear, front-facing subjects without significant occlusion.
