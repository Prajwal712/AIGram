"""
content_verifier.py — Image safety verification and caption generation.

Uses Google Gemini Vision to analyze generated images for content safety
and automatically generate engaging Instagram captions with hashtags.
"""

import os
import json
import requests

from google import genai
from google.genai import types
from src.config import GEMINI_API_KEY, GEMINI_MODEL

# Initialize Gemini client
_client = genai.Client(api_key=GEMINI_API_KEY)

# Temporary file used during verification
_TEMP_IMAGE_PATH = "temp_img.jpg"


def verify_and_caption(image_url: str, concept: str) -> dict:
    """
    Download, verify, and generate a caption for an AI-generated image.

    Performs two tasks via Gemini Vision:
      1. Safety check — flags NSFW, violent, or hateful content.
      2. Caption generation — creates an engaging Instagram caption with hashtags.

    Args:
        image_url: Public URL of the generated image.
        concept:   Original concept used for image generation.

    Returns:
        A dict with keys:
          - "status":  "SAFE" or "UNSAFE"
          - "caption": The generated Instagram caption (if SAFE).
    """
    print("[*] Verifying image and generating caption via Gemini Vision...")

    # 1. Download the image temporarily for Gemini Vision inspection
    img_data = requests.get(image_url, timeout=60).content
    with open(_TEMP_IMAGE_PATH, "wb") as f:
        f.write(img_data)

    # 2. Upload to Gemini Files API
    uploaded_file = _client.files.upload(file=_TEMP_IMAGE_PATH)

    # 3. Analyze with Gemini Vision
    prompt = f"""
    Analyze this image based on the concept: '{concept}'.
    1. Is the image safe for a general audience (no NSFW, violence, or hate speech)?
    2. Write an engaging Instagram caption reflecting the concept. Include 3-5 hashtags.

    Respond STRICTLY in this JSON format:
    {{
        "status": "SAFE" or "UNSAFE",
        "caption": "Your caption here"
    }}
    """

    response = _client.models.generate_content(
        model=GEMINI_MODEL,
        contents=[uploaded_file, prompt],
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
        ),
    )

    # 4. Clean up temporary files (local + cloud)
    _client.files.delete(name=uploaded_file.name)
    if os.path.exists(_TEMP_IMAGE_PATH):
        os.remove(_TEMP_IMAGE_PATH)

    return json.loads(response.text)
