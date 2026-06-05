# 🤖 AI Instagram Bot

> **Fully automated AI-powered Instagram content creation & publishing pipeline.**

This bot takes a simple text concept (e.g. *"a serene Japanese garden at sunset"*) and autonomously generates a stunning image, verifies it for content safety, writes an engaging caption with hashtags, and publishes it directly to your Instagram account — all without manual intervention.

---

## ✨ Features

| Feature | Description |
|---|---|
| **🧠 AI Prompt Engineering** | Transforms simple concepts into rich, detailed prompts using Google Gemini |
| **🎨 AI Image Generation** | Generates high-quality 1024×1024 images via Pollinations AI (free, no key required) |
| **🛡️ Content Safety Check** | Uses Gemini Vision to flag NSFW, violent, or hateful content before publishing |
| **✍️ Auto Caption & Hashtags** | Generates engaging, context-aware Instagram captions with 3–5 relevant hashtags |
| **📤 One-Click Publishing** | Publishes directly to Instagram via the official Graph API |
| **⚙️ CLI Support** | Pass custom concepts as command-line arguments |

---

## 🏗️ Architecture

The project follows a **modular pipeline architecture** where each stage is isolated in its own module:

```
ai_insta_bot/
├── main.py                  # Entry point — CLI parsing & pipeline trigger
├── requirements.txt         # Python dependencies
├── .env                     # API keys & credentials (git-ignored)
├── .env.example             # Template for required environment variables
├── .gitignore               # Git ignore rules
├── README.md                # You are here
│
└── src/                     # Source package
    ├── __init__.py
    ├── config.py            # Centralized configuration & env validation
    ├── prompt_generator.py  # Stage 1 — Gemini prompt generation
    ├── image_generator.py   # Stage 2 — Pollinations AI image generation
    ├── content_verifier.py  # Stage 3 — Gemini Vision safety & captioning
    ├── instagram_publisher.py  # Stage 4 — Instagram Graph API publishing
    └── pipeline.py          # Orchestrator — chains all stages together
```

### Pipeline Flow

```
┌─────────────┐     ┌──────────────┐     ┌──────────────────┐     ┌─────────────┐
│   Concept    │────▶│ Gemini Flash │────▶│ Pollinations AI  │────▶│Gemini Vision│
│  (text)      │     │ (prompt gen) │     │ (image render)   │     │(safety+cap) │
└─────────────┘     └──────────────┘     └──────────────────┘     └──────┬──────┘
                                                                         │
                                                              ┌──────────▼──────────┐
                                                              │  SAFE?              │
                                                              │  ├─ YES → Publish   │
                                                              │  └─ NO  → Abort     │
                                                              └─────────────────────┘
```

---

## 🔧 Prerequisites

- **Python 3.10+**
- **Meta Developer Account** with Instagram API access
- **Google Gemini API Key** (get one at [Google AI Studio](https://aistudio.google.com/apikey))
- An **Instagram Business or Creator account** connected to a Facebook Page

---

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/Prajwal712/AIGram.git
cd AIGram
```

### 2. Create & activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # Linux / macOS
# venv\Scripts\activate         # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` and fill in your credentials:

| Variable | Where to get it |
|---|---|
| `META_ACCESS_TOKEN` | [Meta for Developers](https://developers.facebook.com/) → Instagram API → Generate Token |
| `IG_USER_ID` | Your Instagram Business Account User ID (found in the API explorer) |
| `GEMINI_API_KEY` | [Google AI Studio](https://aistudio.google.com/apikey) |

### 5. Run the bot

```bash
# Use the default concept
python main.py

# Or pass a custom concept
python main.py "A futuristic neon-lit Tokyo street at midnight with rain reflections"
```

---

## 📂 Module Breakdown

### `src/config.py`
Loads all environment variables and provides centralized constants (image dimensions, API version, timeouts). Includes a `validate_config()` function that halts execution early if any required credential is missing.

### `src/prompt_generator.py`
Takes a short concept string and uses **Gemini 2.5 Flash** to expand it into a detailed, art-director-quality prompt specifying lighting, composition, resolution, and mood.

### `src/image_generator.py`
Sends the detailed prompt to the **Pollinations AI** free endpoint to generate a 1024×1024 image. Returns a public URL — no API key required.

### `src/content_verifier.py`
Downloads the generated image, uploads it to **Gemini Vision**, and asks it to:
1. Perform a **safety check** (NSFW / violence / hate speech detection)
2. Generate an **engaging Instagram caption** with 3–5 hashtags

Returns a structured JSON response with `status` and `caption` fields.

### `src/instagram_publisher.py`
Handles the two-step Instagram API publishing flow:
1. **Create a media container** with the image URL and caption
2. **Publish the container** after a configurable wait period for Meta's image processing

### `src/pipeline.py`
Orchestrates all four stages in sequence, with clean error handling and status logging at each step. Aborts early if image generation fails or the content is flagged as unsafe.

---

## ⚙️ Configuration

All tunable settings live in `src/config.py`:

| Setting | Default | Description |
|---|---|---|
| `GEMINI_MODEL` | `gemini-2.5-flash` | Gemini model used for prompt generation & vision |
| `IMAGE_WIDTH` | `1024` | Generated image width in pixels |
| `IMAGE_HEIGHT` | `1024` | Generated image height in pixels |
| `INSTAGRAM_API_VERSION` | `v19.0` | Instagram Graph API version |
| `PUBLISH_WAIT_SECONDS` | `20` | Seconds to wait for Meta to process the image |

---

## 🛡️ Safety

- **Content filtering** is built into the pipeline — images are automatically checked for NSFW, violent, or hateful content before publishing.
- **Secrets are never committed** — `.env` is in `.gitignore`, and `.env.example` provides a safe template.
- All API calls include **timeout parameters** to prevent hanging.

---

## 📝 License

This project is for educational and personal use. Ensure your use of the Instagram Graph API complies with [Meta's Platform Terms](https://developers.facebook.com/terms/).

---

## Acknowledgements

- [Google Gemini](https://ai.google.dev/) — AI prompt generation & vision analysis
- [Pollinations AI](https://pollinations.ai/) — Free AI image generation
- [Instagram Graph API](https://developers.facebook.com/docs/instagram-api/) — Official publishing API
