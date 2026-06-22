# Phase 1 — Preprocessing Pipeline

from PIL import Image, UnidentifiedImageError
import io

def load_and_validate_image(file_or_path):
    """
    Loads an image from a file object or path, converts it to RGB, and validates it.

    Args:
        file_or_path (str or file-like object): The path to the image or a file object (e.g., from Streamlit).

    Returns:
        PIL.Image.Image: The validated and RGB-converted image.

    Raises:
        ValueError: If the image cannot be loaded or is corrupted.
    """
    try:
        if isinstance(file_or_path, (str, bytes)):
            img = Image.open(file_or_path)
            img.verify()
            # verify() can close or alter state, so reopen
            img = Image.open(file_or_path)
        else:
            img = Image.open(file_or_path)
            img.verify()
            # Reset pointer and reopen
            file_or_path.seek(0)
            img = Image.open(file_or_path)
            
        # Convert to RGB (handles RGBA, grayscale, etc. automatically)
        img = img.convert("RGB")
        return img
    except (UnidentifiedImageError, IOError, SyntaxError) as e:
        raise ValueError(f"Cannot load or validate the image (might be corrupted): {e}")
    except Exception as e:
        raise ValueError(f"An unexpected error occurred while loading the image: {e}")

def preprocess_for_model(pil_image):
    """
    Resizes a PIL image to 224x224 pixels using LANCZOS resampling.

    Args:
        pil_image (PIL.Image.Image): The input image to resize.

    Returns:
        PIL.Image.Image: The resized image.
    """
    expected_size = (224, 224)
    # Use Image.Resampling.LANCZOS for PIL >= 9.1.0, fallback to Image.LANCZOS
    resample_filter = getattr(Image, 'Resampling', Image).LANCZOS # type: ignore
    return pil_image.resize(expected_size, resample=resample_filter)

def get_image_info(pil_image):
    """
    Extracts basic information from a PIL image.

    Args:
        pil_image (PIL.Image.Image): The input image.

    Returns:
        dict: A dictionary containing width, height, mode, and aspect_ratio.
    """
    width, height = pil_image.size
    aspect_ratio = round(width / height, 2) if height > 0 else 0.0
    
    return {
        "width": width,
        "height": height,
        "mode": pil_image.mode,
        "aspect_ratio": aspect_ratio
    }
