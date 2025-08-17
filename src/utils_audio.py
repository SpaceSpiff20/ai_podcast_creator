from pydub import AudioSegment, effects
from pydub.generators import Sine
import os

def ensure_intro_music(path:str)->AudioSegment:
    if os.path.exists(path):
        return AudioSegment.from_file(path)
    # fallback: generate a simple 2-second tone if no music file provided
    return Sine(440).to_audio_segment(duration=2000).apply_gain(-10)

def normalize(audio: AudioSegment) -> AudioSegment:
    return effects.normalize(audio)

def stitch_episode(voice: AudioSegment, intro: AudioSegment, outro: AudioSegment) -> AudioSegment:
    bed = intro + AudioSegment.silent(duration=400) + voice + AudioSegment.silent(duration=400) + outro
    return normalize(bed)

def export_mp3(seg: AudioSegment, out_path: str, bitrate: str = "192k"):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    seg.export(out_path, format="mp3", bitrate=bitrate)
