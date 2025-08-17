import os, subprocess, tempfile
from pathlib import Path

def _ffmpeg(*args):
    proc = subprocess.run(["ffmpeg", "-y", *args], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if proc.returncode != 0:
        raise RuntimeError(f"ffmpeg failed:\n{proc.stderr}")
    return proc

def ensure_intro_music(path: str) -> str:
    if os.path.exists(path):
        return path
    tmp = Path(tempfile.gettempdir()) / "intro_tone.mp3"
    _ffmpeg("-f", "lavfi", "-i", "sine=frequency=440:duration=2:sample_rate=44100", "-filter:a", "volume=-10dB", str(tmp))
    return str(tmp)

def ensure_outro_music(path: str) -> str:
    if os.path.exists(path):
        return path
    tmp = Path(tempfile.gettempdir()) / "outro_tone.mp3"
    _ffmpeg("-f", "lavfi", "-i", "sine=frequency=660:duration=2:sample_rate=44100", "-filter:a", "volume=-10dB", str(tmp))
    return str(tmp)

def write_bytes_to_mp3(data: bytes, out_path: str):
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "wb") as f:
        f.write(data)

def concat_and_normalize(intro_path: str, voice_path: str, outro_path: str, out_path: str, bitrate="192k"):
    _ffmpeg(
        "-i", intro_path,
        "-i", voice_path,
        "-i", outro_path,
        "-filter_complex", "[0:a][1:a][2:a]concat=n=3:v=0:a=1, loudnorm=I=-16:TP=-1.5:LRA=11[a]",
        "-map", "[a]",
        "-b:a", bitrate,
        out_path
    )
