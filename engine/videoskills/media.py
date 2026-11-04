"""Safe FFmpeg/FFprobe discovery and media metadata inspection."""
from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path


class MediaError(RuntimeError):
    pass


def tools() -> dict[str, str | None]:
    return {name: shutil.which(name) for name in ("ffmpeg", "ffprobe")}


def require_tools() -> tuple[str, str]:
    found = tools()
    missing = [name for name, path in found.items() if not path]
    if missing:
        raise MediaError("Missing required program(s): " + ", ".join(missing) + ". Install FFmpeg and ensure ffmpeg/ffprobe are on PATH.")
    return found["ffmpeg"], found["ffprobe"]  # type: ignore[return-value]


def probe(path: str | Path) -> dict:
    file = Path(path).expanduser().resolve()
    if not file.is_file():
        raise MediaError(f"Input file does not exist: {file}")
    _, ffprobe = require_tools()
    try:
        proc = subprocess.run([ffprobe, "-v", "error", "-show_format", "-show_streams", "-of", "json", str(file)], check=True, capture_output=True, text=True, timeout=60)
        data = json.loads(proc.stdout)
    except subprocess.CalledProcessError as exc:
        detail = (exc.stderr or "").strip().splitlines()
        raise MediaError(f"FFprobe could not read {file}: {detail[-1] if detail else 'unsupported or damaged media'}") from exc
    except (subprocess.TimeoutExpired, json.JSONDecodeError) as exc:
        raise MediaError(f"Timed out or received invalid metadata while inspecting {file}") from exc

    streams = data.get("streams", [])
    video = next((s for s in streams if s.get("codec_type") == "video"), None)
    audio = next((s for s in streams if s.get("codec_type") == "audio"), None)
    duration = data.get("format", {}).get("duration")
    if duration is None and video:
        duration = video.get("duration")
    width, height = (video.get("width"), video.get("height")) if video else (None, None)
    return {
        "path": str(file),
        "format": data.get("format", {}).get("format_name"),
        "duration_seconds": float(duration or 0),
        "video": None if not video else {
            "codec": video.get("codec_name"), "width": width, "height": height,
            "frame_rate": video.get("avg_frame_rate") or video.get("r_frame_rate"),
            "aspect_ratio": (round(width / height, 5) if width and height else None),
            "pixel_format": video.get("pix_fmt"),
        },
        "audio": None if not audio else {
            "codec": audio.get("codec_name"), "sample_rate": audio.get("sample_rate"),
            "channels": audio.get("channels"), "channel_layout": audio.get("channel_layout"),
        },
        "streams": len(streams),
    }


def validate_video(path: str | Path, width: int | None = None, height: int | None = None) -> dict:
    info = probe(path)
    if not info["video"]:
        raise MediaError("The output has no video stream")
    if info["duration_seconds"] <= 0:
        raise MediaError("The output duration is zero")
    if width is not None and info["video"]["width"] != width:
        raise MediaError(f"Expected width {width}; found {info['video']['width']}")
    if height is not None and info["video"]["height"] != height:
        raise MediaError(f"Expected height {height}; found {info['video']['height']}")
    return info


def contact_sheet(source: str | Path, output: str | Path, columns: int = 4) -> Path:
    source, output = Path(source).expanduser().resolve(), Path(output).expanduser().resolve()
    if columns < 1 or columns > 20:
        raise MediaError("Contact-sheet columns must be between 1 and 20")
    info = probe(source)
    if not info["video"]:
        raise MediaError("Contact sheets require video input")
    if output.exists():
        raise MediaError(f"Refusing to overwrite contact sheet: {output}")
    ffmpeg, _ = require_tools()
    output.parent.mkdir(parents=True, exist_ok=True)
    samples = max(1, int((info["duration_seconds"] + 2.999) // 3))
    rows = max(1, (samples + columns - 1) // columns)
    graph = f"fps=1,select='not(mod(n,3))',scale=320:-1,tile={columns}x{rows}:nb_frames={samples}"
    try:
        subprocess.run([ffmpeg, "-hide_banner", "-loglevel", "error", "-n", "-i", str(source), "-vf", graph, "-frames:v", "1", str(output)], check=True, capture_output=True, text=True, timeout=180)
    except subprocess.CalledProcessError as exc:
        raise MediaError(f"FFmpeg failed to create contact sheet: {(exc.stderr or '').strip()}") from exc
    if not output.is_file() or output.stat().st_size == 0:
        raise MediaError("FFmpeg did not create a contact sheet")
    return output
