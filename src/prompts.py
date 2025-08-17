SYSTEM_PROMPT = """
You are a veteran podcast writer and editor. You write engaging, accurate, and structured
scripts that sound natural when spoken aloud, with short sentences, good pacing, and
occasional rhetorical questions. Avoid filler words and jargon.
"""

SCRIPT_PROMPT = """
Write a {duration_min}-minute podcast script about: "{topic}".

Audience: {audience}
Persona: {persona} (tone: {voice_style})

Structure:
- Cold open (1-2 punchy lines to hook interest)
- Brief intro
- 3–5 segments with transitions + examples
- One takeaway per segment
- Recap + CTA

Constraints:
- Keep sentences short for TTS.
- Use concrete examples.
- Add [pause] sparingly.
{sources_block}

Return JSON with: title, description, script, bullets.
"""

NOTES_PROMPT = """
Create show notes for the episode with:
- Title
- 1-paragraph summary
- 5 key takeaways
- Links (if any provided)
Return Markdown.
"""
