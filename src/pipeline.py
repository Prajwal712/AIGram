"""
pipeline.py — Orchestrates the full content creation pipeline.

Chains together all pipeline stages:
  1. Prompt Generation  →  Gemini crafts a detailed image prompt
  2. Image Generation   →  Pollinations AI renders the image
  3. Content Verification → Gemini Vision checks safety & writes caption
  4. Publishing         →  Instagram Graph API publishes the post
"""

from src.prompt_generator import generate_image_prompt
from src.image_generator import generate_image
from src.content_verifier import verify_and_caption
from src.instagram_publisher import publish_to_instagram


def run_pipeline(concept: str) -> bool:
    """
    Execute the full AI Instagram content pipeline.

    Args:
        concept: A short description of the desired post theme.

    Returns:
        True if the post was published successfully, False otherwise.
    """
    print("=" * 60)
    print("  AI Instagram Bot — Content Pipeline")
    print("=" * 60)
    print(f"\n📝 Concept: {concept}\n")

    # ── Stage 1: Generate Detailed Prompt ─────────────────────────────────
    print("-" * 40)
    detailed_prompt = generate_image_prompt(concept)
    print(f"\n✅ Prompt Generated:\n{detailed_prompt}\n")

    # ── Stage 2: Generate Image ───────────────────────────────────────────
    print("-" * 40)
    img_url = generate_image(detailed_prompt)
    if not img_url:
        print("\n❌ Pipeline aborted: Image generation failed.")
        return False
    print(f"\n✅ Image Generated: {img_url}\n")

    # ── Stage 3: Verify & Caption ─────────────────────────────────────────
    print("-" * 40)
    analysis = verify_and_caption(img_url, concept)
    print(f"\n✅ Analysis Result: {analysis}\n")

    if analysis.get("status") != "SAFE":
        print("❌ Pipeline aborted: Image flagged as UNSAFE.")
        return False

    # ── Stage 4: Publish to Instagram ─────────────────────────────────────
    print("-" * 40)
    caption = analysis.get("caption", "")
    success = publish_to_instagram(img_url, caption)

    if success:
        print("\n🎉 Pipeline completed successfully!")
    else:
        print("\n❌ Pipeline failed at the publishing stage.")

    return success
