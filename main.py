"""
main.py — Entry point for the AI Instagram Bot.

Run this file to execute the full content creation and publishing pipeline.
Provide a concept as a command-line argument, or edit the default below.

Usage:
    python main.py
    python main.py "Your custom concept here"
"""

import sys
from src.config import validate_config
from src.pipeline import run_pipeline

# ── Default concept (used when no CLI argument is provided) ───────────────────
DEFAULT_CONCEPT = (
    "A comparison between India and the world showing the importance "
    "of cleanliness, inspiring a clean India vision."
)


def main():
    """Parse arguments, validate config, and run the pipeline."""

    # Accept an optional concept from the command line
    if len(sys.argv) > 1:
        concept = " ".join(sys.argv[1:])
    else:
        concept = DEFAULT_CONCEPT

    # Validate all required environment variables before starting
    validate_config()

    # Run the full pipeline
    success = run_pipeline(concept)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()