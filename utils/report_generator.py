# Phase 3 — UI Polish + Viva Features

def build_image_report(image_info, prediction_result):
    """
    Builds a formatted text report for a single image analysis.
    
    Args:
        image_info: dict containing width, height, mode, etc.
        prediction_result: dict containing label, confidence_pct, all_scores, etc.
        
    Returns:
        str: Formatted report text.
    """
    width = image_info.get("width", "Unknown")
    height = image_info.get("height", "Unknown")
    mode = image_info.get("mode", "Unknown")
    
    verdict = prediction_result["label"].upper()
    confidence = prediction_result["confidence_pct"]
    
    all_scores_str = ""
    for score in prediction_result["all_scores"]:
        label = score["label"].title()
        pct = round(score["score"] * 100, 2)
        all_scores_str += f"  {label}:  {pct}%\n"
        
    report = f"""═══════════════════════════════════
DEEPFAKE DETECTION REPORT — IMAGE
═══════════════════════════════════
Input: {width} x {height} px | Mode: {mode}
───────────────────────────────────
Verdict:      {verdict}
Confidence:   {confidence}%
───────────────────────────────────
All Scores:
{all_scores_str.rstrip()}
═══════════════════════════════════"""
    
    return report

def build_video_report(video_metadata, prediction_summary, frame_count):
    """
    Builds a formatted text report for a video analysis.
    
    Args:
        video_metadata: dict containing duration, fps, etc.
        prediction_summary: dict containing overall_verdict, overall_confidence_pct, fake/real_frame_count, etc.
        frame_count: number of frames extracted and analyzed
        
    Returns:
        str: Formatted report text.
    """
    duration = video_metadata.get("duration_seconds", "Unknown")
    fps = video_metadata.get("fps", "Unknown")
    
    verdict = prediction_summary["overall_verdict"].upper()
    confidence = prediction_summary["overall_confidence_pct"]
    
    fake_count = prediction_summary["fake_frame_count"]
    real_count = prediction_summary["real_frame_count"]
    
    report = f"""═══════════════════════════════════
DEEPFAKE DETECTION REPORT — VIDEO
═══════════════════════════════════
Input: Duration {duration}s | FPS: {fps}
Frames Analysed: {frame_count}
───────────────────────────────────
Verdict:      {verdict}
Confidence:   {confidence}%
───────────────────────────────────
Analysis Summary:
  Fake Frames: {fake_count}
  Real Frames: {real_count}
═══════════════════════════════════"""
    
    return report
