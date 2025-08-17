import os
from typing import Literal
from openai import OpenAI
try:
    from elevenlabs.client import ElevenLabs
except Exception:
    ElevenLabs = None

def tts_synthesize_to_mp3_bytes(text: str) -> bytes:
    provider: Literal['openai','elevenlabs'] = os.getenv('TTS_PROVIDER','openai').lower()

    if provider == 'elevenlabs':
        if ElevenLabs is None:
            raise RuntimeError('elevenlabs package not installed')
        client = ElevenLabs(api_key=os.getenv('ELEVENLABS_API_KEY'))
        voice_id = os.getenv('ELEVENLABS_VOICE_ID','EXAVITQu4vr4xnSDxMaL')
        audio_bytes = b""
        for chunk in client.text_to_speech.convert(
            voice_id=voice_id,
            optimize_streaming_latency=0,
            output_format='mp3_22050_32',
            text=text,
        ):
            audio_bytes += chunk
        return audio_bytes

    # OpenAI TTS
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    resp = client.audio.speech.create(
        model=os.getenv('OPENAI_TTS_VOICE_MODEL','gpt-4o-mini-tts'),
        voice=os.getenv('OPENAI_TTS_VOICE','alloy'),
        input=text
    )
    return resp.read()
