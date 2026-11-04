"""Audio energy, silence and optional librosa beat estimates."""
from __future__ import annotations

import json
import re
import shutil
import subprocess
from pathlib import Path

from .media import MediaError, probe, require_tools


def analyze(path: str | Path) -> dict:
    file = Path(path).expanduser().resolve()
    info = probe(file)
    if not info["audio"]:
        raise MediaError(f"No audio stream found: {file}")
    ffmpeg, _ = require_tools()
    try:
        result = subprocess.run([ffmpeg, "-hide_banner", "-i", str(file), "-af", "silencedetect=noise=-35dB:d=0.35,astats=metadata=1:reset=1", "-f", "null", "-"], capture_output=True, text=True, timeout=900)
    except subprocess.TimeoutExpired as exc:
        raise MediaError("Audio analysis timed out") from exc
    log = (result.stderr or "") + "\n" + (result.stdout or "")
    silences = []
    pending = None
    for line in log.splitlines():
        start = re.search(r"silence_start:\s*([0-9.]+)", line)
        end = re.search(r"silence_end:\s*([0-9.]+)", line)
        if start:
            pending = float(start.group(1))
        if end:
            finish = float(end.group(1))
            silences.append({"start": pending if pending is not None else 0.0, "end": finish})
            pending = None
    if pending is not None:
        silences.append({"start": pending, "end": info["duration_seconds"]})
    result_data = {"path": str(file), "duration_seconds": info["duration_seconds"], "silences": silences, "bpm": None, "beats_seconds": None, "beat_detection": "librosa not installed; silence analysis only"}
    if shutil.which("python3"):
        try:
            import librosa  # type: ignore
            audio, sr = librosa.load(str(file), sr=22050, mono=True)
            tempo, beat_frames = librosa.beat.beat_track(y=audio, sr=sr, units="frames")
            tempo_value = float(tempo[0] if hasattr(tempo, "__len__") else tempo)
            result_data.update({"bpm": round(tempo_value, 2), "beats_seconds": [round(float(x), 3) for x in librosa.frames_to_time(beat_frames, sr=sr).tolist()], "beat_detection": "librosa estimate"})
        except ImportError:
            pass
        except Exception as exc:
            result_data["beat_detection"] = f"librosa analysis unavailable: {type(exc).__name__}"
    return result_data
