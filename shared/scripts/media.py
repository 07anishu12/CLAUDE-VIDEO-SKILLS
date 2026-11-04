#!/usr/bin/env python3
"""Small FFmpeg-backed media inspection, contact sheet, and render validation CLI."""
import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path


def run(args):
    return subprocess.run(args, check=True, capture_output=True, text=True)


def inspect(path: Path):
    data = json.loads(run(["ffprobe", "-v", "error", "-show_format", "-show_streams", "-of", "json", str(path)]).stdout)
    streams = data.get("streams", [])
    video = next((s for s in streams if s.get("codec_type") == "video"), None)
    audio = next((s for s in streams if s.get("codec_type") == "audio"), None)
    return {
        "path": str(path.resolve()), "duration_seconds": float(data.get("format", {}).get("duration", 0)),
        "format": data.get("format", {}).get("format_name"),
        "video": None if not video else {k: video.get(k) for k in ("codec_name", "width", "height", "r_frame_rate", "pix_fmt")},
        "audio": None if not audio else {k: audio.get(k) for k in ("codec_name", "sample_rate", "channels")},
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="command", required=True)
    i = sub.add_parser("inspect"); i.add_argument("input", type=Path)
    c = sub.add_parser("contact-sheet"); c.add_argument("input", type=Path); c.add_argument("output", type=Path); c.add_argument("--columns", type=int, default=4)
    v = sub.add_parser("validate"); v.add_argument("input", type=Path); v.add_argument("--width", type=int); v.add_argument("--height", type=int)
    a = p.parse_args()
    if not shutil.which("ffprobe") or not shutil.which("ffmpeg"):
        p.error("ffmpeg and ffprobe must be installed and available on PATH")
    if not a.input.is_file(): p.error(f"input does not exist: {a.input}")
    if a.command == "inspect":
        print(json.dumps(inspect(a.input), indent=2)); return
    if a.command == "contact-sheet":
        if a.columns < 1: p.error("--columns must be positive")
        a.output.parent.mkdir(parents=True, exist_ok=True)
        duration = inspect(a.input)["duration_seconds"]
        frames = max(1, int((duration + 2.999) // 3))
        rows = max(1, (frames + a.columns - 1) // a.columns)
        run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(a.input), "-vf", f"fps=1,select='not(mod(n,3))',scale=320:-1,tile={a.columns}x{rows}:nb_frames={frames}", "-frames:v", "1", str(a.output)])
        if not a.output.is_file() or a.output.stat().st_size == 0: p.error("contact sheet was not created")
        print(a.output.resolve()); return
    info = inspect(a.input)
    if not info["video"]: p.error("output has no video stream")
    if info["duration_seconds"] <= 0: p.error("output duration is zero")
    if a.width and info["video"]["width"] != a.width: p.error(f"expected width {a.width}, got {info['video']['width']}")
    if a.height and info["video"]["height"] != a.height: p.error(f"expected height {a.height}, got {info['video']['height']}")
    print(json.dumps(info, indent=2))


if __name__ == "__main__":
    try: main()
    except (subprocess.CalledProcessError, OSError) as exc:
        print(f"media utility error: {exc}", file=sys.stderr); sys.exit(2)
