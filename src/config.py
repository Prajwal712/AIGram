"""
config.py — Centralized configuration and environment variable loading.

Loads all required credentials and API keys from the .env file
and exposes them as module-level constants.
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ── Meta / Instagram Credentials ─────────────────────────────────────────────
META_ACCESS_TOKEN = os.getenv("META_ACCESS_TOKEN")
IG_USER_ID = os.getenv("IG_USER_ID")

# ── Google Gemini API ─────────────────────────────────────────────────────────
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# ── Pollinations AI API ──────────────────────────────────────────────────────
POLLINATIONS_API_KEY = os.getenv("POLLINATIONS_API_KEY")

# ── ImgBB API (Image Hosting) ────────────────────────────────────────────────
IMGBB_API_KEY = os.getenv("IMGBB_API_KEY")

# ── Model Configuration ──────────────────────────────────────────────────────
GEMINI_MODEL = "gemini-3.1-flash-lite"
GEMINI_FALLBACK_MODELS = ["gemini-2.0-flash", "gemini-2.5-flash-lite-preview-06-17"]

# ── Retry Configuration ──────────────────────────────────────────────────────
MAX_RETRIES = 5
INITIAL_BACKOFF = 5  # seconds

# ── Image Generation Settings ────────────────────────────────────────────────
IMAGE_WIDTH = 1024
IMAGE_HEIGHT = 1024

# ── Instagram API Settings ───────────────────────────────────────────────────
INSTAGRAM_API_VERSION = "v19.0"
PUBLISH_WAIT_SECONDS = 20  # Time to wait for Meta to process the image


def validate_config():
    """Validate that all required environment variables are set."""
    required = {
        "META_ACCESS_TOKEN": META_ACCESS_TOKEN,
        "IG_USER_ID": IG_USER_ID,
        "GEMINI_API_KEY": GEMINI_API_KEY,
        "POLLINATIONS_API_KEY": POLLINATIONS_API_KEY,
        "IMGBB_API_KEY": IMGBB_API_KEY,
    }
    missing = [name for name, value in required.items() if not value]

    if missing:
        print(f"[!] Missing required environment variables: {', '.join(missing)}")
        print("    Please check your .env file.")
        sys.exit(1)
