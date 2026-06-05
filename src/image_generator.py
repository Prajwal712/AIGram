"""
image_generator.py — AI image generation via Pollinations AI.

Generates images from detailed text prompts using the Pollinations AI
authenticated API endpoint (requires API key).
"""

import base64
import os
import time
import requests

from src.config import IMAGE_WIDTH, IMAGE_HEIGHT, POLLINATIONS_API_KEY

# Output directory for generated images
OUTPUT_DIR = "output"


def generate_image(image_prompt: str) -> str | None:
    """
    Generate an image from a text prompt using Pollinations AI.

    Uses the OpenAI-compatible POST endpoint with b64_json response format
    to receive image data directly (no separate download needed).

    Args:
        image_prompt: A detailed text prompt describing the desired image.

    Returns:
        The local file path of the saved generated image, or None on failure.
    """
    print("[*] Generating image via Pollinations AI (Authenticated)...")

    # Truncate overly long prompts to prevent provider errors
    if len(image_prompt) > 1500:
        image_prompt = image_prompt[:1500]
        print("[!] Prompt truncated to 1500 characters.")

    try:
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        seed = int(time.time())

        # Use the OpenAI-compatible POST endpoint for image generation
        url = "https://gen.pollinations.ai/v1/images/generations"

        headers = {
            "Authorization": f"Bearer {POLLINATIONS_API_KEY}",
            "Content-Type": "application/json",
        }

        payload = {
            "prompt": image_prompt,
            "model": "zimage",
            "size": f"{IMAGE_WIDTH}x{IMAGE_HEIGHT}",
            "response_format": "b64_json",
        }

        response = requests.post(url, json=payload, headers=headers, timeout=120)

        if response.status_code == 200:
            result = response.json()
            b64_data = result["data"][0]["b64_json"]

            # Decode base64 image data and save locally
            image_bytes = base64.b64decode(b64_data)
            image_path = os.path.join(OUTPUT_DIR, f"generated_{seed}.png")

            with open(image_path, "wb") as f:
                f.write(image_bytes)

            print(f"[+] Image saved to: {image_path}")
            return image_path
        else:
            print(f"[-] Pollinations AI endpoint returned status: {response.status_code}")
            print(f"    Response: {response.text[:300]}")
            return None

    except requests.RequestException as e:
        print(f"[-] Image generation failed (network error): {e}")
        return None
    except Exception as e:
        print(f"[-] Image generation failed: {e}")
        return None
