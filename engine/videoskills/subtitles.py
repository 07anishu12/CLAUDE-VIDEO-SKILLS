"""Subtitle validation and SRT generation from supplied timed segments."""
from __future__ import annotations

import re
from pathlib import Path


class SubtitleError(ValueError):
    pass


def _clock(seconds: float) -> str:
    if seconds < 0:
        raise SubtitleError("Subtitle times cannot be negative")
    ms = round(seconds * 1000)
    hours, ms = divmod(ms, 3_600_000)
    minutes, ms = divmod(ms, 60_000)
    secs, ms = divmod(ms, 1000)
    return f"{hours:02}:{minutes:02}:{secs:02},{ms:03}"


def write_srt(segments: list[dict], output: str | Path) -> Path:
    if not segments:
        raise SubtitleError("Provide at least one timed subtitle segment")
    chunks = []
    prior_start = -1.0
    for index, segment in enumerate(segments, 1):
        try:
            start, end, text = float(segment["start"]), float(segment["end"]), str(segment["text"])
        except (KeyError, TypeError, ValueError) as exc:
            raise SubtitleError(f"Segment {index} needs numeric start/end and text") from exc
        if start < prior_start or end <= start or not text.strip():
            raise SubtitleError(f"Segment {index} has invalid or unordered timing/text")
        prior_start = start
        text = re.sub(r"\r\n?", "\n", text).strip().replace("\x00", "")
        chunks.append(f"{index}\n{_clock(start)} --> {_clock(end)}\n{text}")
    path = Path(output).expanduser().resolve()
    if path.exists():
        raise FileExistsError(f"Refusing to overwrite subtitle file: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n\n".join(chunks) + "\n", encoding="utf-8")
    return path


def validate_srt(path: str | Path) -> int:
    text = Path(path).read_text(encoding="utf-8-sig")
    matches = re.findall(r"(?m)^\d+\s*\n(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\s*\n(.+?)(?=\n\s*\n|\Z)", text, re.S)
    if not matches:
        raise SubtitleError("No valid SRT subtitle cues found")
    return len(matches)
