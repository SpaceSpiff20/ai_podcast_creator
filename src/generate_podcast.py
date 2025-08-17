import os, argparse, json
from datetime import datetime, timezone
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

from utils_audio_ffmpeg import ensure_intro_music, ensure_outro_music, write_bytes_to_mp3, concat_and_normalize
from tts_providers import tts_synthesize_to_mp3_bytes
from rss import update_rss
from prompts import SYSTEM_PROMPT, SCRIPT_PROMPT, NOTES_PROMPT

def generate_script(client, topic, duration_min, audience, persona, voice_style, sources):
    from prompts import SYSTEM_PROMPT, SCRIPT_PROMPT
    sources_block = ""
    if sources:
        src_lines = "\n".join(f"- {s}" for s in sources)
        sources_block = f"Sources to summarize and attribute lightly:\n{src_lines}"

    user_prompt = SCRIPT_PROMPT.format(
        topic=topic,
        duration_min=duration_min,
        audience=audience,
        persona=persona,
        voice_style=voice_style,
        sources_block=sources_block
    )

    # Use Chat Completions and ask for JSON directly
    chat = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT + "\nReturn a strict JSON object with keys: title, description, script, bullets."},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.7,
        response_format={"type": "json_object"},  # supported in newer SDKs; harmless if ignored
    )
    text = chat.choices[0].message.content

    import json
    try:
        return json.loads(text)
    except Exception:
        # Fallback if the model returned non-JSON text
        return {
            "title": f"{topic}",
            "description": f"A {duration_min}-minute episode about {topic}.",
            "script": text,
            "bullets": []
        }


def generate_notes(client, script_data, sources):
    prompt = NOTES_PROMPT + "\\n\\nEpisode JSON:\\n" + json.dumps(script_data)
    resp = client.responses.create(model="gpt-4.1-mini", input=[
        {"role":"system","content":"You are a precise editor."},
        {"role":"user","content":prompt}
    ])
    return resp.output_text

def main():
    load_dotenv()
    parser = argparse.ArgumentParser()
    parser.add_argument("--topic", required=True)
    parser.add_argument("--duration-min", type=int, default=8)
    parser.add_argument("--audience", default="curious professionals")
    parser.add_argument("--persona", default="friendly expert")
    parser.add_argument("--voice-style", default="confident and conversational")
    parser.add_argument("--sources", nargs="*", default=[])
    args = parser.parse_args()

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    script_data = generate_script(client, args.topic, args.duration_min, args.audience, args.persona, args.voice_style, args.sources)
    script_text = script_data["script"]

    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    ep_dir = Path("out")/f"ep_{ts}"
    ep_dir.mkdir(parents=True, exist_ok=True)

    voice_path = ep_dir/"voice.mp3"
    write_bytes_to_mp3(tts_synthesize_to_mp3_bytes(script_text), voice_path)

    audio_path = ep_dir/"episode.mp3"
    concat_and_normalize(ensure_intro_music("assets/intro_music.mp3"), str(voice_path), ensure_outro_music("assets/outro_music.mp3"), str(audio_path))

    (ep_dir/"shownotes.md").write_text(generate_notes(client, script_data, args.sources))
    (ep_dir/"episode.json").write_text(json.dumps(script_data, indent=2))

    feed_path = Path("out")/"podcast.rss"
    update_rss(str(feed_path), script_data["title"], script_data["description"], f"file://{audio_path.resolve()}", datetime.now(timezone.utc))

    print(f"✅ Episode generated at {audio_path}")

if __name__ == "__main__":
    main()
