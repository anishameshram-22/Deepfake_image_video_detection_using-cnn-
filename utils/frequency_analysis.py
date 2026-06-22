# Upgrade Phase 1 — Frequency Domain Analysis

import numpy as np
from PIL import Image

__all__ = ["analyze_frequency_domain", "get_frequency_interpretation", "freq_score_to_color"]

def analyze_frequency_domain(pil_image):
    """
    Analyses image frequency domain using 2D FFT to detect AI generation artefacts. 
    AI-generated images exhibit unnaturally uniform frequency distributions compared 
    to real photographs.
    """
    ai_suspicion_score = 0.0
    
    # Step 1 — Convert image to grayscale
    gray = pil_image.convert("L")
    
    # Step 2 — Convert to numpy float32 array
    gray_arr = np.array(gray, dtype=np.float32)
    
    # Step 3 — Apply numpy 2D FFT
    fft = np.fft.fft2(gray_arr)
    
    # Step 4 — Shift the zero-frequency component to center
    fft_shifted = np.fft.fftshift(fft)
    
    # Step 5 — Compute log magnitude
    magnitude = np.log(np.abs(fft_shifted) + 1)
    
    # Step 6 — Calculate freq_variance
    freq_variance = float(np.var(magnitude))
    
    # Step 7 — Calculate freq_mean
    freq_mean = float(np.mean(magnitude))
    
    # Step 8 — Get image shape
    h, w = magnitude.shape
    
    # Step 9 — Compute center
    center_h = h // 2
    center_w = w // 2
    
    # Step 10 — Compute margin
    margin = min(h, w) // 6
    
    # Step 11 — Extract low frequency region
    low_freq = magnitude[center_h-margin:center_h+margin, center_w-margin:center_w+margin]
    
    # Step 12 — Compute high_freq_energy
    high_freq_energy = np.sum(magnitude) - np.sum(low_freq)
    
    # Step 13 — Compute total_energy
    total_energy = np.sum(magnitude)
    
    # Step 14 — Compute high_freq_ratio
    high_freq_ratio = float(high_freq_energy / total_energy) if total_energy > 0 else 0.0
    
    # Scoring logic
    if freq_variance < 8.0:
        ai_suspicion_score += 0.40
    elif freq_variance < 12.0:
        ai_suspicion_score += 0.20
        
    if high_freq_ratio < 0.55:
        ai_suspicion_score += 0.35
    elif high_freq_ratio < 0.65:
        ai_suspicion_score += 0.15
        
    # Cap score at maximum 1.0 using min()
    ai_suspicion_score = min(ai_suspicion_score, 1.0)
    
    # Verdict string logic
    if ai_suspicion_score >= 0.6:
        freq_verdict = "Suspicious — AI-like frequency pattern detected"
    elif ai_suspicion_score >= 0.3:
        freq_verdict = "Uncertain — ambiguous frequency pattern"
    else:
        freq_verdict = "Natural — real photo-like frequency pattern"
        
    return {
        "ai_suspicion_score": round(float(ai_suspicion_score), 3),
        "ai_suspicion_pct": round(float(ai_suspicion_score) * 100.0, 1),
        "freq_variance": round(float(freq_variance), 3),
        "high_freq_ratio": round(float(high_freq_ratio), 3),
        "freq_mean": round(float(freq_mean), 3),
        "freq_verdict": freq_verdict
    }

def get_frequency_interpretation(freq_result):
    """
    Returns a plain English string explanation based on frequency analysis results.
    """
    score = freq_result["ai_suspicion_score"]
    variance = freq_result["freq_variance"]
    ratio = freq_result["high_freq_ratio"]
    
    if score >= 0.6:
        return f"The frequency spectrum shows patterns typical of AI-generated images. Real photographs contain natural noise across all frequency bands. This image shows unusually uniform frequency distribution (variance: {variance}) and suppressed high-frequency content (ratio: {ratio}), both characteristic of GAN or diffusion model outputs."
    elif score >= 0.3:
        return f"The frequency analysis is inconclusive. Some AI-like spectral patterns were found (variance: {variance}, high-freq ratio: {ratio}), but not strongly enough to confirm manipulation. Image compression or photo processing could cause similar patterns."
    else:
        return f"The frequency spectrum looks natural. Real photographs typically show this distribution of frequency content (variance: {variance}, high-freq ratio: {ratio}). No strong AI generation fingerprint detected at the spectral level."

def freq_score_to_color(ai_suspicion_score):
    """
    Returns a hex color code based on the AI suspicion score.
    """
    if ai_suspicion_score >= 0.6:
        return "#FF4B4B"
    elif ai_suspicion_score >= 0.3:
        return "#FFA500"
    else:
        return "#00CC44"
