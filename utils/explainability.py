# Phase 3 — UI Polish + Viva Features

def generate_confidence_chart_data(all_scores):
    """
    Converts raw classifier scores into a format suitable for Streamlit charts.
    
    Args:
        all_scores: List of dicts with 'label' and 'score'
        
    Returns:
        dict: {"labels": [...], "values": [...]} representing percentage confidences.
    """
    labels = []
    values = []
    for score_dict in all_scores:
        labels.append(score_dict["label"].title())
        values.append(round(score_dict["score"] * 100, 2))
        
    return {"labels": labels, "values": values}

def get_verdict_explanation(is_fake, confidence_pct):
    """
    Provides a plain-English explanation of what the CNN result means.
    
    Args:
        is_fake (bool): True if classified as Fake, else False.
        confidence_pct (float): Condifence percentage 0-100.
        
    Returns:
        str: Explanation string.
    """
    if is_fake:
        if confidence_pct > 85:
            return "The CNN detected strong visual inconsistencies typical of GAN-generated faces — unnatural skin texture, lighting artefacts, or boundary blending errors."
        elif confidence_pct >= 60:
            return "The CNN found moderate signs of manipulation. The face shows some artefacts consistent with deepfake generation, though the signal is not definitive."
        else:
            return "The CNN flagged this as potentially fake, but with low confidence. Social media compression or image quality may be reducing detection accuracy."
    else:
        if confidence_pct > 85:
            return "The CNN found no significant manipulation artefacts. The facial texture, lighting, and boundaries appear consistent with authentic footage."
        elif confidence_pct >= 60:
            return "The CNN found the image likely real, though moderate confidence suggests some ambiguity — possibly due to image quality or compression."
        else:
            return "Low confidence result. The model is uncertain. Try a higher quality, uncompressed version of the image."

def get_research_context():
    """
    Returns research and context information about the model limitations and training.
    
    Returns:
        dict: Contextual research strings.
    """
    return {
        "model_type": "EfficientNet CNN (Convolutional Neural Network)",
        "training_data": "Real vs GAN-generated face images",
        "known_limitation": "Cross-dataset generalisation — models trained on one dataset may drop in accuracy on different deepfake generation methods (e.g. XceptionNet drops from 99.26% on FF++ to 51.31% on DFDC)",
        "compression_note": "Heavy compression (e.g. WhatsApp video) can reduce accuracy by 10+ percentage points by destroying pixel-level artefacts the CNN relies on",
        "paper_reference": "Based on: Deepfake Image and Video Detection Using CNNs — AIML Diploma Project 2025–26"
    }
