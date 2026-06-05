"""
image_uploader.py — Upload images to ImgBB for public hosting.

Uploads local image files to ImgBB to get publicly accessible URLs,
which are required by the Instagram Graph API for publishing.
"""

import base64
import requests

from src.config import IMGBB_API_KEY


def upload_to_imgbb(image_path: str) -> str | None:
    """
    Upload a local image file to ImgBB and return its public URL.

    Args:
        image_path: Local file path of the image to upload.

    Returns:
        The public URL of the uploaded image, or None on failure.
    """
    print("[*] Uploading image to ImgBB for public hosting...")

    try:
        with open(image_path, "rb") as f:
            image_data = base64.b64encode(f.read()).decode("utf-8")

        response = requests.post(
            "https://api.imgbb.com/1/upload",
            data={
                "key": IMGBB_API_KEY,
                "image": image_data,
            },
            timeout=60,
        )

        result = response.json()

        if result.get("success"):
            public_url = result["data"]["url"]
            print(f"[+] Image uploaded: {public_url}")
            return public_url
        else:
            print(f"[-] ImgBB upload failed: {result}")
            return None

    except requests.RequestException as e:
        print(f"[-] ImgBB upload failed (network error): {e}")
        return None
    except Exception as e:
        print(f"[-] ImgBB upload failed: {e}")
        return None
