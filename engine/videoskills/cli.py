"""Command-line interface for Video Skills Core."""
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
import tempfile
from pathlib import Path

from . import __version__
from .audio import analyze
from .media import MediaError, contact_sheet, probe, require_tools, tools, validate_video
from .render import render_project
from .subtitles import SubtitleError, validate_srt, write_srt


def _quick_project(args):
    clips = []
    for path in args.input:
        clip = {"path": str(Path(path).expanduser().resolve())}
        if args.start is not None:
            clip["start"] = args.start
        if args.duration is not None:
            clip["duration"] = args.duration
        if args.speed != 1:
            clip["speed"] = args.speed
        if args.zoom != 1:
            clip["zoom"] = args.zoom
        if args.brightness != 0:
            clip["brightness"] = args.brightness
        if args.contrast != 1:
            clip["contrast"] = args.contrast
        if args.saturation != 1:
            clip["saturation"] = args.saturation
        clips.append(clip)
    project = {
        "clips": clips, "output": str(Path(args.output).expanduser().resolve()),
        "width": args.width, "height": args.height, "fps": args.fps,
    }
    if args.audio:
        project["audio"] = str(Path(args.audio).expanduser().resolve())
        project["audio_fade_out"] = args.audio_fade_out
    if args.captions:
        project["captions"] = str(Path(args.captions).expanduser().resolve())
    if args.transition != "cut":
        project["transition"] = {"type": args.transition, "duration": args.transition_duration}
    with tempfile.TemporaryDirectory(prefix="claude-video-project-") as temp:
        path = Path(temp) / "project.json"
        path.write_text(json.dumps(project), encoding="utf-8")
        return render_project(path, overwrite=args.overwrite)


def parser():
    p = argparse.ArgumentParser(prog="video-skills", description="Inspect media and render safe, reviewable video edits.")
    p.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    sub = p.add_subparsers(dest="command", required=True)
    sub.add_parser("check", help="report required and optional tools")
    i = sub.add_parser("inspect", help="inspect image, audio, or video metadata"); i.add_argument("input", type=Path)
    c = sub.add_parser("contact-sheet", help="create a still contact sheet from a video"); c.add_argument("input", type=Path); c.add_argument("output", type=Path); c.add_argument("--columns", type=int, default=4)
    v = sub.add_parser("validate", help="verify a rendered MP4"); v.add_argument("input", type=Path); v.add_argument("--width", type=int); v.add_argument("--height", type=int)
    a = sub.add_parser("analyze-audio", help="measure silence and, if installed, estimate beats/BPM"); a.add_argument("input", type=Path)
    r = sub.add_parser("render", help="render a JSON timeline project"); r.add_argument("project", type=Path); r.add_argument("--overwrite", action="store_true")
    q = sub.add_parser("quick-edit", help="trim or concatenate clips into an MP4")
    q.add_argument("--input", action="append", required=True, type=Path); q.add_argument("--output", required=True, type=Path)
    q.add_argument("--width", type=int, default=1080); q.add_argument("--height", type=int, default=1920); q.add_argument("--fps", type=float, default=30)
    q.add_argument("--start", type=float); q.add_argument("--duration", type=float); q.add_argument("--speed", type=float, default=1)
    q.add_argument("--zoom", type=float, default=1); q.add_argument("--brightness", type=float, default=0); q.add_argument("--contrast", type=float, default=1); q.add_argument("--saturation", type=float, default=1)
    q.add_argument("--audio", type=Path); q.add_argument("--audio-fade-out", type=float, default=0); q.add_argument("--captions", type=Path)
    q.add_argument("--transition", choices=["cut", "fade", "wipeleft", "wiperight", "slideleft", "slideright", "circleopen", "dissolve"], default="cut")
    q.add_argument("--transition-duration", type=float, default=0.35); q.add_argument("--overwrite", action="store_true")
    s = sub.add_parser("subtitles", help="validate SRT or create it from accurate timed segments")
    ss = s.add_subparsers(dest="subtitle_command", required=True)
    sv = ss.add_parser("validate"); sv.add_argument("input", type=Path)
    sw = ss.add_parser("write"); sw.add_argument("segments_json", type=Path); sw.add_argument("output", type=Path)
    return p


def main(argv=None):
    args = parser().parse_args(argv)
    try:
        if args.command == "check":
            result = tools()
            result["librosa"] = importlib.util.find_spec("librosa") is not None
            print(json.dumps(result, indent=2))
            return 0 if result["ffmpeg"] and result["ffprobe"] else 2
        if args.command == "inspect":
            print(json.dumps(probe(args.input), indent=2)); return 0
        if args.command == "contact-sheet":
            print(contact_sheet(args.input, args.output, args.columns)); return 0
        if args.command == "validate":
            print(json.dumps(validate_video(args.input, args.width, args.height), indent=2)); return 0
        if args.command == "analyze-audio":
            print(json.dumps(analyze(args.input), indent=2)); return 0
        if args.command == "render":
            print(json.dumps(render_project(args.project, args.overwrite), indent=2)); return 0
        if args.command == "quick-edit":
            print(json.dumps(_quick_project(args), indent=2)); return 0
        if args.command == "subtitles":
            if args.subtitle_command == "validate":
                print(json.dumps({"cues": validate_srt(args.input)})); return 0
            segments = json.loads(args.segments_json.read_text(encoding="utf-8"))
            print(write_srt(segments, args.output)); return 0
    except (MediaError, SubtitleError, OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 2
