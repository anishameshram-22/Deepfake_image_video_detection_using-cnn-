# Upgrade Phase 2 — Ensemble Model Engine

import streamlit as st
from transformers import pipeline

MODELS = {
    "GAN Face Detector":  "dima806/deepfake_vs_real_image_detection",
    "AI Image Detector":  "haywoodsloan/ai-image-detector-deploy",
    "SDXL Detector":      "Organika/sdxl-detector",
}

FAKE_LABEL_ALIASES = ["fake", "artificial", "ai-generated", "ai_generated", "1", "generated"]

__all__ = ["load_all_models", "ensemble_predict", "get_ensemble_explanation"]

@st.cache_resource
def load_all_models():
    """
    Loads all 3 CNN classifiers from HuggingFace. Cached by Streamlit so models load only once. 
    Individual models that fail to load are marked None and skipped during prediction.
    """
    loaded = {}
    for name, model_id in MODELS.items():
        try:
            loaded[name] = pipeline("image-classification", model=model_id)
        except Exception:
            loaded[name] = None
    return loaded

def run_single_model(clf, model_name, pil_image):
    """
    Runs a single loaded HuggingFace pipeline on an image and formats the result.
    """
    if clf is None:
        return None
        
    try:
        raw_results = clf(pil_image)
        top = raw_results[0]
        label = top["label"].strip().lower()
        is_fake = label in FAKE_LABEL_ALIASES
        
        return {
            "model": model_name,
            "verdict": "Fake" if is_fake else "Real",
            "is_fake": is_fake,
            "confidence": top["score"],
            "confidence_pct": round(top["score"] * 100, 1),
            "raw": raw_results
        }
    except Exception:
        return None

def ensemble_predict(models_dict, pil_image, freq_result=None):
    """
    Runs all loaded models and aggregates their predictions, incorporating optional frequency analysis.
    """
    # Step 1 — Run all models
    model_results = []
    for model_name, clf in models_dict.items():
        result = run_single_model(clf, model_name, pil_image)
        if result is not None:
            model_results.append(result)

    # Step 2 — Count CNN votes
    votes_fake = sum(1 for r in model_results if r["is_fake"])
    votes_real = sum(1 for r in model_results if not r["is_fake"])

    # Step 3 — Add frequency analysis as soft vote
    freq_bonus = 0.0
    if freq_result is not None:
        score = freq_result["ai_suspicion_score"]
        if score >= 0.6:
            freq_bonus = 0.5
        elif score >= 0.3:
            freq_bonus = 0.25
            
    votes_fake_weighted = votes_fake + freq_bonus
    votes_real_weighted = float(votes_real)

    # Step 4 — Final verdict
    is_deepfake = votes_fake_weighted > votes_real_weighted
    total_weighted = votes_fake_weighted + votes_real_weighted
    
    if total_weighted > 0:
        winning_votes = max(votes_fake_weighted, votes_real_weighted)
        ensemble_confidence_pct = round(float(winning_votes / total_weighted) * 100.0, 1)
    else:
        ensemble_confidence_pct = 50.0

    # Step 5 — Determine risk level string
    if is_deepfake and ensemble_confidence_pct >= 75: 
        risk_level = "HIGH RISK"
    elif is_deepfake and ensemble_confidence_pct >= 50: 
        risk_level = "MEDIUM RISK"
    elif is_deepfake: 
        risk_level = "LOW RISK"
    else: 
        risk_level = "LIKELY AUTHENTIC"

    # Step 6 — Return dict
    return {
        "is_deepfake": is_deepfake,
        "final_verdict": "Fake" if is_deepfake else "Real",
        "ensemble_confidence_pct": ensemble_confidence_pct,
        "votes_fake_raw": votes_fake,
        "votes_real_raw": votes_real,
        "votes_fake_weighted": round(float(votes_fake_weighted), 2),
        "votes_real_weighted": round(float(votes_real_weighted), 2),
        "freq_bonus_applied": round(float(freq_bonus), 2),
        "model_results": model_results,
        "models_used": len(model_results),
        "risk_level": risk_level
    }

def get_ensemble_explanation(ensemble_result):
    """
    Provides a plain English explanation of the ensemble prediction result.
    """
    n = ensemble_result["models_used"]
    fake_votes = ensemble_result["votes_fake_raw"]
    real_votes = ensemble_result["votes_real_raw"]
    freq_bonus = ensemble_result["freq_bonus_applied"]
    conf = ensemble_result["ensemble_confidence_pct"]
    is_fake = ensemble_result["is_deepfake"]

    if is_fake:
        return f"{fake_votes} out of {n} CNN models flagged this as fake, with frequency analysis adding {freq_bonus} additional weight. Combined ensemble confidence: {conf}%. Multiple independent models agreeing on a fake verdict significantly reduces the chance of a false positive."
    else:
        return f"{real_votes} out of {n} CNN models classified this as real. Frequency analysis added {freq_bonus} weight toward fake — not enough to override the CNN majority. Ensemble confidence: {conf}%. Consider testing with a higher resolution, uncompressed version if you suspect manipulation."
