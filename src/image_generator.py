"""
image_generator.py — AI image generation via Pollinations AI.

Generates images from detailed text prompts using the Pollinations AI
free API endpoint (no API key required).
"""

import time
import urllib.parse
import requests

from src.config import IMAGE_WIDTH, IMAGE_HEIGHT


def generate_image(image_prompt: str) -> str | None:
    """
    Generate an image from a text prompt using Pollinations AI.

    Args:
        image_prompt: A detailed text prompt describing the desired image.

    Returns:
        The public URL of the generated image, or None on failure.
    """
    print("[*] Generating image via Pollinations AI (No key required)...")

    try:
        encoded_prompt = urllib.parse.quote(image_prompt)
        seed = int(time.time())

        image_url = (
            f"https://image.pollinations.ai/p/{encoded_prompt}"
            f"?width={IMAGE_WIDTH}&height={IMAGE_HEIGHT}"
            f"&seed={seed}&nologo=true"
        )

        # Verify the URL returns a successful response
        verify_res = requests.head(image_url, timeout=30)

        if verify_res.status_code == 200:
            return image_url
        else:
            print(f"[-] Pollinations AI endpoint returned status: {verify_res.status_code}")
            return None

    except requests.RequestException as e:
        print(f"[-] Image generation failed (network error): {e}")
        return None
    except Exception as e:
        print(f"[-] Image generation failed: {e}")
        return None
