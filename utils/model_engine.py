# Phase 2 — CNN Model + Prediction Engine

"""
This module loads a pre-trained EfficientNet CNN from HuggingFace to perform deepfake vs real image detection.
"""

from transformers import pipeline

MODEL_ID = "dima806/deepfake_vs_real_image_detection"

def load_classifier():
    """
    Initialises and returns the HuggingFace image classification pipeline.
    This should be called with @st.cache_resource in Streamlit to avoid reloading on every run.
    """
    classifier = pipeline(task="image-classification", model=MODEL_ID)
    return classifier

def predict_single_image(classifier, pil_image):
    """
    Accepts a loaded HuggingFace pipeline and a PIL image, then predicts whether
    it is Fake or Real.
    
    Args:
        classifier: pipeline object
        pil_image: PIL Image object
        
    Returns:
        dict: A dictionary containing label, confidence, confidence_pct, is_fake, and all_scores.
    """
    all_scores = classifier(pil_image)
    top_result = all_scores[0]
    
    label = top_result['label'].title() # Ensure it's 'Fake' or 'Real'
    confidence = float(top_result['score'])
    confidence_pct = round(float(confidence) * 100.0, 2)
    is_fake = (label == "Fake")
    
    return {
        "label": label,
        "confidence": confidence,
        "confidence_pct": confidence_pct,
        "is_fake": is_fake,
        "all_scores": all_scores
    }

def predict_video_frames(classifier, frames_list):
    """
    Accepts the classifier and a list of PIL Images, predicting the result for each frame
    and calculating aggregate statistics.
    
    Args:
        classifier: pipeline object
        frames_list: list of PIL.Image.Image objects
        
    Returns:
        dict: A dictionary containing 'frame_results' and 'summary' of aggregate stats.
    """
    frame_results = []
    
    fake_confidences: list[float] = [] # type: ignore
    real_confidences: list[float] = [] # type: ignore
    
    for frame in frames_list:
        res = predict_single_image(classifier, frame)
        frame_results.append(res)
        
        if res["is_fake"]:
            fake_confidences.append(float(res["confidence"])) # type: ignore
        else:
            real_confidences.append(float(res["confidence"])) # type: ignore
            
    fake_frame_count = len(fake_confidences)
    real_frame_count = len(real_confidences)
    
    avg_fake_confidence = sum(fake_confidences) / fake_frame_count if fake_frame_count > 0 else 0.0
    avg_real_confidence = sum(real_confidences) / real_frame_count if real_frame_count > 0 else 0.0
    
    if avg_fake_confidence > avg_real_confidence:
        overall_verdict = "Fake"
        overall_confidence_pct = round(float(avg_fake_confidence) * 100.0, 2)
        is_deepfake = True
    else:
        overall_verdict = "Real"
        overall_confidence_pct = round(float(avg_real_confidence) * 100.0, 2)
        is_deepfake = False
        
    summary = {
        "avg_fake_confidence": avg_fake_confidence,
        "avg_real_confidence": avg_real_confidence,
        "fake_frame_count": fake_frame_count,
        "real_frame_count": real_frame_count,
        "overall_verdict": overall_verdict,
        "overall_confidence_pct": overall_confidence_pct,
        "is_deepfake": is_deepfake
    }
    
    return {
        "frame_results": frame_results,
        "summary": summary
    }

__all__ = ["load_classifier", "predict_single_image", "predict_video_frames"]
