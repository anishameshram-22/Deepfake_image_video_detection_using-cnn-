# Upgrade Phase 4 — Dark Forensic UI

import streamlit as st
from PIL import Image
import tempfile
import os
import numpy as np
import pandas as pd

from styles.theme import inject_css
from utils.ensemble import load_all_models, ensemble_predict, get_ensemble_explanation
from utils.frequency_analysis import (
    analyze_frequency_domain,
    get_frequency_interpretation,
    freq_score_to_color
)
from utils.preprocessor import load_and_validate_image, get_image_info
from utils.video_utils import extract_frames, save_uploaded_video, get_video_metadata

# ─────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────
st.set_page_config(
    page_title="Deepfake Detector — Ensemble CNN",
    page_icon="🔍",
    layout="centered"
)

inject_css()
st.markdown('<div class="scan-line"></div>', unsafe_allow_html=True)

# ─────────────────────────────────────────
# SIDEBAR (always visible)
# ─────────────────────────────────────────
st.sidebar.markdown("## ⬡ DETECTION SYSTEM")
st.sidebar.markdown('<div class="section-header">Active Models</div>', unsafe_allow_html=True)
st.sidebar.markdown(
    """
    **3 CNN Models Used:**
    - 🔬 GAN Face Detector
    - 🤖 AI Image Detector  
    - 🖼️ SDXL Detector

    **Plus: FFT Frequency Analysis**
    Detects invisible AI spectral fingerprints that survive compression.

    **Voting System:**
    Each CNN gets 1 vote. Frequency analysis adds up to 0.5 votes if suspicious. Most votes wins.
    """
)
st.sidebar.divider()
st.sidebar.markdown("**⚠️ Known Limitations:**")
st.sidebar.markdown(
    """
    - Heavily compressed images reduce accuracy
    - Very new AI models may not be detected
    - Works best on clear, front-facing faces
    - This is a prototype — not forensic-grade
    """
)
st.sidebar.divider()
st.sidebar.caption("AIML Diploma Project 2025–26 | Based on FaceForensics++ research")

# ─────────────────────────────────────────
# MAIN PAGE HEADER
# ─────────────────────────────────────────
st.markdown("# DEEPFAKE DETECTION SYSTEM")
st.markdown('<p style="font-family: Share Tech Mono, monospace; color: #00d4ff; letter-spacing: 3px; font-size: 0.8rem; text-transform: uppercase;">3-MODEL CNN ENSEMBLE // FREQUENCY DOMAIN ANALYSIS // v2.0</p>', unsafe_allow_html=True)
st.divider()

# ─────────────────────────────────────────
# MODEL LOADING
# ─────────────────────────────────────────
@st.cache_resource
def load_models_cached():
    return load_all_models()

with st.spinner("Loading 3 CNN models — first run takes 2–3 minutes..."):
    models = load_models_cached()

loaded_count = len([v for v in models.values() if v is not None])
st.markdown(f'''
<div style="background: rgba(0,255,136,0.06); border: 1px solid rgba(0,255,136,0.3); 
border-left: 3px solid #00ff88; border-radius: 2px; padding: 0.8rem 1.2rem;
font-family: Share Tech Mono, monospace; font-size: 0.8rem; color: #00ff88; letter-spacing: 2px;">
▶ SYSTEM READY — {loaded_count}/3 CNN MODELS LOADED
</div>
''', unsafe_allow_html=True)
st.divider()

# ─────────────────────────────────────────
# MODE SELECTOR
# ─────────────────────────────────────────
mode = st.radio("Select input type:", ["📷 Image", "🎥 Video"], horizontal=True)
st.divider()

# ─────────────────────────────────────────
# IMAGE MODE
# ─────────────────────────────────────────
if mode == "📷 Image":
    uploaded_file = st.file_uploader("Upload a face image", type=["jpg", "jpeg", "png", "webp"])

    if uploaded_file is not None:
        try:
            image = load_and_validate_image(uploaded_file)
            info = get_image_info(image)
            
            st.image(image, use_column_width=True)
            
            col1, col2 = st.columns(2)
            col1.metric("Width", f"{info['width']}px")
            col2.metric("Height", f"{info['height']}px")
            st.divider()

            if st.button("🔍 Analyse Image", type="primary", use_container_width=True):
                with st.spinner("Running 3 CNN models + FFT analysis..."):
                    freq_result = analyze_frequency_domain(image)
                    ensemble_result = ensemble_predict(models, image, freq_result=freq_result)
                    
                    # SECTION A — MAIN VERDICT BOX
                    if ensemble_result["is_deepfake"]:
                        risk = ensemble_result["risk_level"]
                        conf = ensemble_result["ensemble_confidence_pct"]
                        st.markdown(f'''
                        <div class="verdict-fake">
                            <p class="verdict-label">⚠ DEEPFAKE DETECTED</p>
                            <p class="verdict-sub">Risk Level: {risk} — Ensemble Confidence: {conf}%</p>
                        </div>
                        ''', unsafe_allow_html=True)
                    else:
                        conf = ensemble_result["ensemble_confidence_pct"]
                        st.markdown(f'''
                        <div class="verdict-real">
                            <p class="verdict-label">✓ AUTHENTIC</p>
                            <p class="verdict-sub">No manipulation detected — Confidence: {conf}%</p>
                        </div>
                        ''', unsafe_allow_html=True)
                            
                    metrics_cols = st.columns(3)
                    metrics_cols[0].metric("Ensemble Confidence", f"{ensemble_result['ensemble_confidence_pct']}%")
                    metrics_cols[1].metric("CNN Votes: Fake", f"{ensemble_result['votes_fake_raw']} / {ensemble_result['models_used']}")
                    metrics_cols[2].metric("CNN Votes: Real", f"{ensemble_result['votes_real_raw']} / {ensemble_result['models_used']}")

                    # SECTION B — ENSEMBLE EXPLANATION
                    st.info(get_ensemble_explanation(ensemble_result))

                    # SECTION C — PER MODEL BREAKDOWN
                    with st.expander("🔬 Per-Model CNN Results", expanded=True):
                        st.markdown('<div class="section-header">CNN Model Votes</div>', unsafe_allow_html=True)
                        for result in ensemble_result["model_results"]:
                            badge = 'model-badge-fake">⚠ FAKE' if result["is_fake"] else 'model-badge-real">✓ REAL'
                            st.markdown(f'''
                            <div class="model-row">
                                <span class="model-name">{result["model"]}</span>
                                <span class="{badge}</span>
                                <span class="model-conf">{result["confidence_pct"]}%</span>
                            </div>
                            ''', unsafe_allow_html=True)

                    # SECTION D — FREQUENCY ANALYSIS
                    with st.expander("📡 Frequency Domain Analysis (FFT)", expanded=False):
                        score = freq_result["ai_suspicion_score"]
                        pct = freq_result["ai_suspicion_pct"]
                        color = freq_score_to_color(score)
                        
                        st.markdown(f'''
                        <div class="section-header">Spectral Analysis</div>
                        <p style="font-family: Share Tech Mono, monospace; font-size: 0.75rem; 
                        color: #8892b0; letter-spacing: 1px; margin-bottom: 0.8rem;">
                        {freq_result["freq_verdict"]}
                        </p>
                        <div style="display: flex; justify-content: space-between; margin-bottom: 0.3rem;">
                            <span style="font-family: Share Tech Mono, monospace; font-size: 0.7rem; 
                            color: #8892b0; letter-spacing: 2px; text-transform: uppercase;">AI SUSPICION SCORE</span>
                            <span style="font-family: Rajdhani, sans-serif; font-weight: 700; 
                            font-size: 1rem; color: {color};">{pct}%</span>
                        </div>
                        <div class="fft-bar-wrap">
                            <div class="fft-bar-fill" style="width: {pct}%; background: {color};"></div>
                        </div>
                        ''', unsafe_allow_html=True)
                        
                        f_cols = st.columns(2)
                        f_cols[0].metric("Frequency Variance", freq_result["freq_variance"])
                        f_cols[1].metric("High-Freq Ratio", freq_result["high_freq_ratio"])
                        
                        st.info(get_frequency_interpretation(freq_result))
                        
        except Exception as e:
            st.error("Analysis failed. Please try a different image.")

# ─────────────────────────────────────────
# VIDEO MODE
# ─────────────────────────────────────────
elif mode == "🎥 Video":
    uploaded_file = st.file_uploader("Upload a video", type=["mp4", "mov", "avi"])

    if uploaded_file is not None:
        tmp_path = None
        try:
            tmp_path = save_uploaded_video(uploaded_file)
            st.video(tmp_path)
            
            meta = get_video_metadata(tmp_path)
            v_cols = st.columns(3)
            v_cols[0].metric("Duration", f"{meta.get('duration_seconds', 0)}s")
            v_cols[1].metric("FPS", f"{meta.get('fps', 0)}")
            v_cols[2].metric("Total Frames", f"{meta.get('total_frames', 0)}")
            st.divider()

            if st.button("🔍 Analyse Video", type="primary", use_container_width=True):
                with st.spinner("Extracting 8 frames and running full ensemble on each..."):
                    frames = extract_frames(tmp_path, max_frames=8)
                    
                    if not frames:
                        st.error("Could not extract frames. Try a different video file.")
                    else:
                        frame_analyses = []
                        for i, frame in enumerate(frames):
                            frame_freq = analyze_frequency_domain(frame)
                            frame_pred = ensemble_predict(models, frame, freq_result=frame_freq)
                            frame_analyses.append({
                                "frame": frame,
                                "pred": frame_pred,
                                "freq": frame_freq,
                                "num": i + 1
                            })

                        # Calculate overall video verdict
                        total_fake = sum(1 for f in frame_analyses if f["pred"]["is_deepfake"])
                        total_real = len(frame_analyses) - total_fake
                        video_is_fake = total_fake > total_real
                        avg_conf = round(np.mean([f["pred"]["ensemble_confidence_pct"] for f in frame_analyses]), 1)
                        
                        # Generate overall summary object to pass into risk formatting wrapper
                        overall_summary = {
                            "is_deepfake": video_is_fake,
                            "ensemble_confidence_pct": avg_conf,
                            "risk_level": "HIGH RISK" if video_is_fake and avg_conf >= 75 else ("MEDIUM RISK" if video_is_fake and avg_conf >= 50 else ("LOW RISK" if video_is_fake else "LIKELY AUTHENTIC"))
                        }

                        # Show OVERALL VERDICT
                        if overall_summary["is_deepfake"]:
                            risk = overall_summary["risk_level"]
                            conf = overall_summary["ensemble_confidence_pct"]
                            st.markdown(f'''
                            <div class="verdict-fake">
                                <p class="verdict-label">⚠ DEEPFAKE DETECTED</p>
                                <p class="verdict-sub">Risk Level: {risk} — Ensemble Confidence: {conf}%</p>
                            </div>
                            ''', unsafe_allow_html=True)
                        else:
                            conf = overall_summary["ensemble_confidence_pct"]
                            st.markdown(f'''
                            <div class="verdict-real">
                                <p class="verdict-label">✓ AUTHENTIC</p>
                                <p class="verdict-sub">No manipulation detected — Confidence: {conf}%</p>
                            </div>
                            ''', unsafe_allow_html=True)
                            
                        res_cols = st.columns(3)
                        res_cols[0].metric("Average Confidence", f"{avg_conf}%")
                        res_cols[1].metric("Fake Frames", f"{total_fake} / {len(frame_analyses)}")
                        res_cols[2].metric("Real Frames", f"{total_real} / {len(frame_analyses)}")

                        # Show FRAME GRID
                        st.subheader("Frame-by-Frame Analysis")
                        grid_cols = st.columns(4)
                        for idx, fa in enumerate(frame_analyses):
                            col = grid_cols[idx % 4]
                            with col:
                                st.image(fa["frame"], use_column_width=True, caption=f"Frame {fa['num']}")
                                if fa["pred"]["is_deepfake"]:
                                    st.error(f"🚨 FAKE {fa['pred']['ensemble_confidence_pct']}%")
                                else:
                                    st.success(f"✅ REAL {fa['pred']['ensemble_confidence_pct']}%")
                                st.caption(f"FFT: {fa['freq']['ai_suspicion_pct']}% suspicious")

                        # Show FRAME DATA TABLE
                        with st.expander("📊 Full Frame Data Table"):
                            table_data = []
                            for fa in frame_analyses:
                                table_data.append({
                                    "Frame No.": fa["num"],
                                    "Verdict": "Fake" if fa["pred"]["is_deepfake"] else "Real",
                                    "CNN Confidence %": fa["pred"]["ensemble_confidence_pct"],
                                    "FFT Suspicion %": fa["freq"]["ai_suspicion_pct"],
                                    "Fake CNN Votes": fa["pred"]["votes_fake_raw"],
                                    "Real CNN Votes": fa["pred"]["votes_real_raw"],
                                })
                            st.dataframe(pd.DataFrame(table_data), use_container_width=True)
                            
        except Exception as e:
            st.error("Analysis failed. Please try a different video.")
        finally:
            if tmp_path and os.path.exists(tmp_path):
                try:
                    os.unlink(tmp_path)
                except Exception:
                    pass

# ─────────────────────────────────────────
# BOTTOM SECTION — How It Works (always visible)
# ─────────────────────────────────────────
st.divider()
st.markdown('<div class="section-header">Detection Architecture</div>', unsafe_allow_html=True)
cols = st.columns(3)
steps = [
    ("01", "INPUT", "Image or video uploaded. Video split into 8 evenly-spaced frames for temporal analysis."),
    ("02", "CNN ENSEMBLE", "3 independent EfficientNet CNNs classify each frame. Each model casts 1 vote — majority wins."),
    ("03", "FFT ANALYSIS", "2D frequency transform detects GAN spectral fingerprints invisible to the human eye."),
]

for idx, (num, title, desc) in enumerate(steps):
    with cols[idx]:
         st.markdown(f'''
        <div class="step-card">
            <div class="step-number">{num}</div>
            <div class="step-title">{title}</div>
            <div class="step-desc">{desc}</div>
        </div>
        ''', unsafe_allow_html=True)

st.divider()
st.markdown('''
<p style="font-family: Share Tech Mono, monospace; font-size: 0.65rem; 
color: rgba(136,146,176,0.4); letter-spacing: 2px; text-align: center; text-transform: uppercase;">
AIML DIPLOMA 2025–26 // CNN: EfficientNet Ensemble // Dataset Ref: FaceForensics++ DFDC CelebDF
</p>
''', unsafe_allow_html=True)
