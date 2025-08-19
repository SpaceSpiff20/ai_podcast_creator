import os
import base64
from typing import Literal
from openai import OpenAI
try:
    from elevenlabs.client import ElevenLabs
except Exception:
    ElevenLabs = None
try:
    from speechify import Speechify
    from speechify.tts import GetSpeechOptionsRequest
except Exception:
    Speechify = None

def tts_synthesize_to_mp3_bytes(text: str) -> bytes:
    provider: Literal['openai','elevenlabs','speechify'] = os.getenv('TTS_PROVIDER','openai').lower()

    if provider == 'speechify':
        if Speechify is None:
            raise RuntimeError('speechify package not installed')
        
        client = Speechify(token=os.getenv('SPEECHIFY_API_KEY'))
        voice_id = os.getenv('SPEECHIFY_VOICE_ID', 'scott')
        model = os.getenv('SPEECHIFY_MODEL', 'simba-english')
        language = os.getenv('SPEECHIFY_LANGUAGE', 'en-US')
        
        # Speechify API call
        response = client.tts.audio.speech(
            audio_format="mp3",
            input=text,
            language=language,
            model=model,
            options=GetSpeechOptionsRequest(
                loudness_normalization=True,
                text_normalization=True
            ),
            voice_id=voice_id
        )
        
        # Speechify returns a response object with base64 encoded audio_data
        # Decode the base64 audio data to get the actual bytes
        if hasattr(response, 'audio_data') and response.audio_data:
            return base64.b64decode(response.audio_data)
        else:
            raise RuntimeError('No audio data received from Speechify API')

    elif provider == 'elevenlabs':
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
