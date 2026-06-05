"""
instagram_publisher.py — Instagram Graph API publishing.

Handles the two-step publishing process required by the Instagram Graph API:
  1. Create a media container with the image URL and caption.
  2. Publish the container to make it live on the feed.
"""

import time
import requests

from src.config import META_ACCESS_TOKEN, IG_USER_ID, INSTAGRAM_API_VERSION, PUBLISH_WAIT_SECONDS


def publish_to_instagram(image_url: str, caption: str) -> bool:
    """
    Publish an image to Instagram via the Graph API.

    Args:
        image_url: Public URL of the image to publish.
        caption:   Caption text for the Instagram post.

    Returns:
        True if published successfully, False otherwise.
    """
    print("[*] Uploading to Instagram Graph API...")

    base_url = f"https://graph.instagram.com/{INSTAGRAM_API_VERSION}/{IG_USER_ID}"

    # ── Step 1: Create Media Container ────────────────────────────────────
    container_url = f"{base_url}/media"
    container_payload = {
        "image_url": image_url,
        "caption": caption,
        "access_token": META_ACCESS_TOKEN,
    }

    try:
        container_res = requests.post(container_url, data=container_payload, timeout=30).json()
    except requests.RequestException as e:
        print(f"[-] Network error creating container: {e}")
        return False

    if "id" not in container_res:
        print(f"[-] Error creating container: {container_res}")
        return False

    creation_id = container_res["id"]
    print(f"[*] Container created: {creation_id}. Waiting for Meta to process the image...")
    time.sleep(PUBLISH_WAIT_SECONDS)

    # ── Step 2: Publish the Container ─────────────────────────────────────
    publish_url = f"{base_url}/media_publish"
    publish_payload = {
        "creation_id": creation_id,
        "access_token": META_ACCESS_TOKEN,
    }

    try:
        publish_res = requests.post(publish_url, data=publish_payload, timeout=30).json()
    except requests.RequestException as e:
        print(f"[-] Network error publishing post: {e}")
        return False

    if "id" in publish_res:
        print(f"[+] Successfully published to Instagram! Post ID: {publish_res['id']}")
        return True
    else:
        print(f"[-] Error publishing: {publish_res}")
        return False
