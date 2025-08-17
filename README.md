# 🎙️ AI Podcast Starter (Code + Files)

Generate a full podcast episode from a topic **using AI for script + AI voice** and export a ready-to-publish MP3, show notes, and an RSS feed.

## What you get

- `src/generate_podcast.py` — one-command pipeline
- AI script generation (OpenAI)
- AI voice TTS (OpenAI or ElevenLabs)
- Simple audio polishing & intro/outro
- Episode notes + RSS feed
- Outputs in `out/`

---

## 1) Setup

```bash
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Copy `.env.sample` to `.env` and fill values:

```bash
cp .env.sample .env
```

- `OPENAI_API_KEY` — required for script generation and OpenAI TTS.
- Choose `TTS_PROVIDER=openai` or `elevenlabs`.
- For OpenAI TTS, set `OPENAI_TTS_VOICE_MODEL` (e.g., `gpt-4o-mini-tts`) and `OPENAI_TTS_VOICE` (e.g., `alloy`).
- For ElevenLabs, set `ELEVENLABS_API_KEY` and `ELEVENLABS_VOICE_ID`.

_(Tip: You can also drop your own intro music in `assets/intro_music.mp3`.)_

---

## 2) Run

**Quick start (single topic):**

```bash
python src/generate_podcast.py \
  --topic "Why vector databases matter for RAG in 2025" \
  --duration-min 8
```

**With links to summarize (optional):**

```bash
python src/generate_podcast.py \  --topic "This week's AI news" \  --duration-min 10 \  --sources "https://openai.com" "https://arxiv.org" "https://news.ycombinator.com"
```

Outputs:

- `out/ep_YYYYMMDD_HHMMSS/episode.mp3`
- `out/ep_.../shownotes.md`
- `out/podcast.rss` (auto-updated, add to your host later)

---

## 3) How it works

1. **Script** — Prompts GPT to write a narrative of target duration with a hook, segments, and CTA.
2. **TTS** — Converts the script to voice (OpenAI or ElevenLabs).
3. **Polish** — Adds intro/outro stings, normalizes loudness, and exports MP3.
4. **Notes/RSS** — Generates show notes and updates `podcast.rss` with an `<item>`.

You can customize prompts in `src/prompts.py` and branding in `src/templates/`.

---

## 4) Hosting & Distribution

- Upload MP3 to your host (e.g., Spotify for Podcasters, Buzzsprout, Libsyn).
- Point your host to `out/podcast.rss` or use host-managed RSS.
- Also publish on YouTube (upload the audio with a static cover).

---

## 5) Common tweaks

- Replace `assets/intro_music.mp3` with your own music.
- Set `--voice-style` for tone (e.g., friendly, authoritative).
- Edit the prompt to match your show's persona.
- For a video version, pipe text into an avatar tool (e.g., Synthesia/HeyGen) separately.

---

## 6) Dev Notes

- `pydub` uses ffmpeg. Install it if you don’t have it:
  - macOS: `brew install ffmpeg`
  - Ubuntu: `sudo apt-get install ffmpeg`
  - Windows: install from https://ffmpeg.org

---

Happy podcasting! 🎧
