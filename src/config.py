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

# ── Model Configuration ──────────────────────────────────────────────────────
GEMINI_MODEL = "gemini-2.5-flash"

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
    }
    missing = [name for name, value in required.items() if not value]

    if missing:
        print(f"[!] Missing required environment variables: {', '.join(missing)}")
        print("    Please check your .env file.")
        sys.exit(1)
