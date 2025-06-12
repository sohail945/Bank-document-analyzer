import easyocr
from PIL import Image
import numpy as np
from PIL import ImageOps, ImageEnhance

# Load OCR reader once with both English and Urdu support
reader = easyocr.Reader(['en', 'ur'], gpu=False)


def enhance_image_for_ocr(image: Image.Image):
    # Convert to grayscale
    gray = ImageOps.grayscale(image)
    
    # Enhance contrast
    contrast = ImageEnhance.Contrast(gray).enhance(2.5)
    
    # Resize (optional): upscale image to help OCR on small text
    resized = contrast.resize((contrast.width * 2, contrast.height * 2), Image.LANCZOS)
    
    return np.array(resized)

def extract_text(image: Image.Image):
    # Convert to grayscale and enhance contrast
    gray = ImageOps.grayscale(image)
    enhancer = ImageEnhance.Contrast(gray)
    enhanced = enhancer.enhance(2.0)

    image_np = np.array(enhanced)
    result = reader.readtext(image_np, detail=0)
    text = " ".join(result)

    return text if len(text.strip()) >= 10 else "No readable text detected."
