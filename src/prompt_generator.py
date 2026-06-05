"""
prompt_generator.py — AI-powered image prompt generation.

Uses Google Gemini to transform a simple concept into a highly detailed
prompt suitable for AI image generators.
"""

from google import genai
from src.config import GEMINI_API_KEY, GEMINI_MODEL

# Initialize Gemini client
_client = genai.Client(api_key=GEMINI_API_KEY)


def generate_image_prompt(concept: str) -> str:
    """
    Generate a detailed, art-director-quality image prompt from a concept.

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

    response = _client.models.generate_content(
        model=GEMINI_MODEL,
        contents=system_prompt,
    )

    return response.text.strip()
