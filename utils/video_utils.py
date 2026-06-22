# Phase 1 — Preprocessing Pipeline

import cv2
import numpy as np
from PIL import Image
import tempfile

def extract_frames(video_path, max_frames=8):
    """
    Extracts evenly spaced frames from a video.

    Args:
        video_path (str): The path to the video file.
        max_frames (int, optional): The maximum number of frames to extract. Defaults to 8.

    Returns:
        list of PIL.Image.Image: A list of extracted frames as PIL Image objects.

    Raises:
        ValueError: If the video cannot be opened or yields zero frames.
    """
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        cap.release()
        raise ValueError(f"Failed to open video file: {video_path}")
        
    extracted_frames = []
    try:
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        if total_frames <= 0:
            raise ValueError("Video contains zero frames or frame count cannot be determined.")
            
        # Determine evenly spaced frame indices
        indices = np.linspace(0, total_frames - 1, min(max_frames, total_frames), dtype=int)
        
        for idx in indices:
            cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
            ret, frame = cap.read()
            if ret:
                # Convert BGR (OpenCV default) to RGB
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # Convert to PIL Image
                pil_img = Image.fromarray(rgb_frame)
                extracted_frames.append(pil_img)
            else:
                continue
                
        if len(extracted_frames) == 0:
            raise ValueError("Failed to extract any frames from the video.")
            
        return extracted_frames
    finally:
        cap.release()

def get_video_metadata(video_path):
    """
    Retrieves metadata from a video file.

    Args:
        video_path (str): The path to the video file.

    Returns:
        dict: A dictionary containing total_frames, fps, duration_seconds, width, and height.
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return {}
        
    try:
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = float(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        duration_seconds = round(float(total_frames / fps), 2) if fps > 0 else 0.0
        fps_rounded = round(float(fps), 1)
        
        return {
            "total_frames": total_frames,
            "fps": fps_rounded,
            "duration_seconds": duration_seconds,
            "width": width,
            "height": height
        }
    finally:
        cap.release()

def save_uploaded_video(uploaded_file):
    """
    Saves a Streamlit uploaded video file to a temporary location.

    Args:
        uploaded_file (streamlit.runtime.uploaded_file_manager.UploadedFile): The uploaded video file.

    Returns:
        str: The path to the saved temporary file.
    """
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    try:
        temp_file.write(uploaded_file.read())
        uploaded_file.seek(0)
    finally:
        temp_file.close()
        
    return temp_file.name
