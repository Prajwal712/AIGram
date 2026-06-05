"""
content_verifier.py — Image safety verification and caption generation.

Uses Google Gemini Vision to analyze generated images for content safety
and automatically generate engaging Instagram captions with hashtags.
"""

import json
import re
import time

from google import genai
from google.genai import types
from google.genai.errors import ServerError, ClientError
from src.config import (
    GEMINI_API_KEY, GEMINI_MODEL, GEMINI_FALLBACK_MODELS,
    MAX_RETRIES, INITIAL_BACKOFF,
)

# Initialize Gemini client
_client = genai.Client(api_key=GEMINI_API_KEY)


def _extract_retry_delay(error_message: str) -> int | None:
    """Extract retry delay from a Gemini rate-limit error message."""
    match = re.search(r'retry in (\d+)', str(error_message), re.IGNORECASE)
    return int(match.group(1)) if match else None


def verify_and_caption(image_path: str, concept: str) -> dict:
    """
    Verify and generate a caption for an AI-generated image.

    Performs two tasks via Gemini Vision:
      1. Safety check — flags NSFW, violent, or hateful content.
      2. Caption generation — creates an engaging Instagram caption with hashtags.

    Includes automatic retry with exponential backoff and fallback models
    for Gemini 503/429 errors.

    Args:
        image_path: Local file path of the generated image.
        concept:    Original concept used for image generation.

    Returns:
        A dict with keys:
          - "status":  "SAFE" or "UNSAFE"
          - "caption": The generated Instagram caption (if SAFE).
    """
    print("[*] Verifying image and generating caption via Gemini Vision...")

    # Upload the local image to Gemini Files API
    uploaded_file = _client.files.upload(file=image_path)

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

    try:
        models_to_try = [GEMINI_MODEL] + GEMINI_FALLBACK_MODELS

        for model in models_to_try:
            for attempt in range(1, MAX_RETRIES + 1):
                try:
                    response = _client.models.generate_content(
                        model=model,
                        contents=[uploaded_file, prompt],
                        config=types.GenerateContentConfig(
                            response_mime_type="application/json",
                        ),
                    )
                    return json.loads(response.text)

                except (ServerError, ClientError) as e:
                    error_str = str(e)
                    is_rate_limit = "429" in error_str or "RESOURCE_EXHAUSTED" in error_str
                    is_overloaded = "503" in error_str or "UNAVAILABLE" in error_str

                    if is_rate_limit or is_overloaded:
                        suggested_delay = _extract_retry_delay(error_str)
                        wait = suggested_delay or INITIAL_BACKOFF * (2 ** (attempt - 1))

                        if attempt < MAX_RETRIES:
                            error_type = "rate-limited" if is_rate_limit else "overloaded"
                            print(f"[!] {model} {error_type} (attempt {attempt}/{MAX_RETRIES}). "
                                  f"Retrying in {wait}s...")
                            time.sleep(wait)
                        else:
                            print(f"[!] {model} unavailable after {MAX_RETRIES} attempts. "
                                  f"Trying next model...")
                            break  # Move to next model
                    else:
                        raise  # Non-retryable error

        raise RuntimeError("All Gemini models unavailable. Please try again later.")

    finally:
        # Always clean up the cloud upload
        _client.files.delete(name=uploaded_file.name)
