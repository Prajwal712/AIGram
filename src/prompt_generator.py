"""
prompt_generator.py — AI-powered image prompt generation.

Uses Google Gemini to transform a simple concept into a highly detailed
prompt suitable for AI image generators.
"""

import re
import time
from google import genai
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


def _generate_with_retry(system_prompt: str) -> str:
    """Try the primary model first, then fallbacks, with retry logic."""
    models_to_try = [GEMINI_MODEL] + GEMINI_FALLBACK_MODELS

    for model in models_to_try:
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                response = _client.models.generate_content(
                    model=model,
                    contents=system_prompt,
                )
                return response.text.strip()

            except (ServerError, ClientError) as e:
                error_str = str(e)
                is_rate_limit = "429" in error_str or "RESOURCE_EXHAUSTED" in error_str
                is_overloaded = "503" in error_str or "UNAVAILABLE" in error_str

                if is_rate_limit or is_overloaded:
                    # Try to extract server-suggested retry delay
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


def generate_image_prompt(concept: str) -> str:
    """
    Generate a detailed, art-director-quality image prompt from a concept.

    Includes automatic retry with exponential backoff and fallback models
    for Gemini 503/429 errors.

    Args:
        concept: A short description of the desired image theme.

    Returns:
        A detailed prompt string optimized for AI image generators.
    """
    print(f"[*] Generating detailed image prompt for: '{concept}'")

    system_prompt = (
        "You are an expert art director. Write a highly detailed, "
        "single-paragraph prompt for an AI image generator based on this "
        f"concept: '{concept}'. Specify realistic lighting, 4k resolution, "
        "composition, and mood. Do NOT include any text in the image. "
        "Output ONLY the prompt string."
    )

    return _generate_with_retry(system_prompt)
