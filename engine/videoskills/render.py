"""Render small edit timelines with FFmpeg using an explicit JSON project file."""
from __future__ import annotations

import json
import math
import os
import subprocess
import tempfile
from pathlib import Path

from .media import MediaError, probe, require_tools, validate_video
from .subtitles import validate_srt

TRANSITIONS = {"fade", "wipeleft", "wiperight", "slideleft", "slideright", "circleopen", "dissolve"}


def _number(value, label, low, high):
    try:
        number = float(value)
    except (TypeError, ValueError) as exc:
        raise MediaError(f"{label} must be a number") from exc
    if not math.isfinite(number) or not low <= number <= high:
        raise MediaError(f"{label} must be between {low} and {high}")
    return number


def _resolve_media(value, base, label):
    path = Path(value).expanduser()
    path = path if path.is_absolute() else base / path
    path = path.resolve()
    if not path.is_file():
        raise MediaError(f"{label} does not exist: {path}")
    return path


def render_project(project_file: str | Path, overwrite: bool = False) -> dict:
    file = Path(project_file).expanduser().resolve()
    try:
        project = json.loads(file.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise MediaError(f"Cannot read project JSON {file}: {exc}") from exc
    if not isinstance(project, dict) or not isinstance(project.get("clips"), list) or not project["clips"]:
        raise MediaError("Project must contain a non-empty 'clips' array")

    width, height = project.get("width", 1080), project.get("height", 1920)
    fps = _number(project.get("fps", 30), "fps", 1, 120)
    if not isinstance(width, int) or not isinstance(height, int) or not (16 <= width <= 7680 and 16 <= height <= 7680):
        raise MediaError("width and height must be integers between 16 and 7680")
    output = _resolve_output(project.get("output", "out/claude-video.mp4"), file.parent)
    if output.exists() and not overwrite:
        raise MediaError(f"Refusing to overwrite existing output: {output}; pass --overwrite after review")
    output.parent.mkdir(parents=True, exist_ok=True)

    ffmpeg, _ = require_tools()
    base = file.parent
    normalized = []
    input_args = [ffmpeg, "-hide_banner", "-loglevel", "error", "-nostdin"]
    durations = []
    for index, clip in enumerate(project["clips"]):
        if not isinstance(clip, dict) or not clip.get("path"):
            raise MediaError(f"clips[{index}] needs a path")
        path = _resolve_media(clip["path"], base, f"clips[{index}].path")
        info = probe(path)
        image = path.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tif", ".tiff"}
        if not image and not info["video"]:
            raise MediaError(f"Clip has no video stream: {path}")
        start = _number(clip.get("start", 0), f"clips[{index}].start", 0, 31_536_000)
        if image:
            if "duration" not in clip:
                raise MediaError(f"Still image clips[{index}] require a duration in seconds")
            duration = _number(clip["duration"], f"clips[{index}].duration", 0.05, 86_400)
            input_args += ["-loop", "1", "-framerate", str(fps), "-t", str(duration), "-i", str(path)]
            has_audio = False
        else:
            source_duration = info["duration_seconds"]
            duration = _number(clip.get("duration", source_duration - start), f"clips[{index}].duration", 0.05, 86_400)
            if start + duration > source_duration + 0.05:
                raise MediaError(f"Requested segment exceeds source duration for {path}")
            input_args += ["-ss", str(start), "-i", str(path)]
            has_audio = bool(info["audio"])
        speed = _number(clip.get("speed", 1), f"clips[{index}].speed", 0.25, 4)
        duration /= speed
        brightness = _number(clip.get("brightness", 0), f"clips[{index}].brightness", -1, 1)
        contrast = _number(clip.get("contrast", 1), f"clips[{index}].contrast", 0, 3)
        saturation = _number(clip.get("saturation", 1), f"clips[{index}].saturation", 0, 3)
        zoom = _number(clip.get("zoom", 1), f"clips[{index}].zoom", 1, 2)
        normalized.append({"duration": duration, "has_audio": has_audio, "speed": speed, "brightness": brightness, "contrast": contrast, "saturation": saturation, "zoom": zoom})
        durations.append(duration)

    transition = project.get("transition", {})
    if not isinstance(transition, dict):
        raise MediaError("transition must be an object")
    transition_type = transition.get("type", "cut")
    if transition_type not in TRANSITIONS | {"cut"}:
        raise MediaError(f"Unsupported transition type {transition_type!r}")
    transition_duration = _number(transition.get("duration", 0.35), "transition.duration", 0.05, 5) if transition_type != "cut" else 0
    if transition_duration and (len(normalized) < 2 or any(d <= transition_duration for d in durations)):
        raise MediaError("Each clip must be longer than the transition")

    filters = []
    video_labels, audio_labels = [], []
    silence_input_indexes = {}
    next_input = len(normalized)
    if not project.get("audio") and len(normalized) > 1:
        for clip_index, item in enumerate(normalized):
            if not item["has_audio"]:
                silence_input_indexes[clip_index] = next_input
                input_args += ["-f", "lavfi", "-t", str(item["duration"] * item["speed"]), "-i", "anullsrc=channel_layout=stereo:sample_rate=48000"]
                next_input += 1
    for index, item in enumerate(normalized):
        duration = item["duration"] * item["speed"]
        speed = item["speed"]
        zoom = item["zoom"]
        scaled_w, scaled_h = math.ceil(width * zoom), math.ceil(height * zoom)
        graph = (
            f"[{index}:v]trim=duration={duration:.6f},setpts=(PTS-STARTPTS)/{speed:.6f},"
            f"scale={scaled_w}:{scaled_h}:force_original_aspect_ratio=increase,"
            f"crop={width}:{height},fps={fps:g},setsar=1,"
            f"eq=brightness={item['brightness']:.6f}:contrast={item['contrast']:.6f}:saturation={item['saturation']:.6f},"
            f"format=yuv420p[v{index}]"
        )
        filters.append(graph)
        video_labels.append(f"[v{index}]")
        if (len(normalized) > 1 or item["speed"] != 1) and not project.get("audio"):
            if item["has_audio"]:
                audio_source = f"[{index}:a:0]"
            else:
                silence_index = silence_input_indexes[index]
                audio_source = f"[{silence_index}:a:0]"
            filters.append(f"{audio_source}atrim=duration={item['duration']*item['speed']:.6f},asetpts=(PTS-STARTPTS)/{item['speed']:.6f},aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo[a{index}]")
            audio_labels.append(f"[a{index}]")

    if len(video_labels) == 1:
        final_video = video_labels[0]
    elif transition_type == "cut":
        filters.append("".join(video_labels) + f"concat=n={len(video_labels)}:v=1:a=0[vout]")
        final_video = "[vout]"
    else:
        current, accumulated = video_labels[0], durations[0]
        for index in range(1, len(video_labels)):
            offset = accumulated - transition_duration
            label = f"vx{index}"
            filters.append(f"{current}{video_labels[index]}xfade=transition={transition_type}:duration={transition_duration:.6f}:offset={offset:.6f}[{label}]")
            current, accumulated = f"[{label}]", accumulated + durations[index] - transition_duration
        final_video = current

    final_audio = None
    if project.get("audio"):
        audio_path = _resolve_media(project["audio"], base, "audio")
        audio_info = probe(audio_path)
        if not audio_info["audio"]:
            raise MediaError(f"Audio input has no audio stream: {audio_path}")
        input_args += ["-i", str(audio_path)]
        final_audio = f"{next_input}:a:0"
    elif audio_labels:
        if transition_type == "cut":
            filters.append("".join(audio_labels) + f"concat=n={len(audio_labels)}:v=0:a=1[aout]")
            final_audio = "[aout]"
        else:
            current, accumulated = audio_labels[0], durations[0]
            for index in range(1, len(audio_labels)):
                label = f"ax{index}"
                filters.append(f"{current}{audio_labels[index]}acrossfade=d={transition_duration:.6f}:c1=tri:c2=tri[{label}]")
                current, accumulated = f"[{label}]", accumulated + durations[index] - transition_duration
            final_audio = current
    elif normalized[0]["has_audio"]:
        final_audio = "0:a:0"

    captions = project.get("captions")
    subtitle_input = None
    if captions:
        subtitle_path = _resolve_media(captions, base, "captions")
        validate_srt(subtitle_path)
        subtitle_input = next_input + (1 if project.get("audio") else 0)
        input_args += ["-i", str(subtitle_path)]

    graph = ";".join(filters)
    total = sum(durations) - (transition_duration * (len(durations) - 1) if transition_type != "cut" else 0)
    fd, temp_name = tempfile.mkstemp(prefix=f".{output.stem}.", suffix=".mp4", dir=output.parent)
    os.close(fd)
    temp = Path(temp_name)
    temp.unlink()
    try:
        cmd = input_args
        if graph:
            cmd += ["-filter_complex", graph]
        cmd += ["-map", final_video, "-c:v", "libx264", "-preset", str(project.get("preset", "medium")), "-crf", str(int(_number(project.get("crf", 20), "crf", 0, 51))), "-r", str(fps), "-pix_fmt", "yuv420p", "-movflags", "+faststart"]
        if final_audio:
            cmd += ["-map", final_audio, "-c:a", "aac", "-b:a", "192k"]
            if project.get("audio"):
                fade = _number(project.get("audio_fade_out", 0), "audio_fade_out", 0, max(total, 0.01))
                audio_filter = f"apad,atrim=duration={total:.6f}"
                if fade:
                    audio_filter += f",afade=t=out:st={max(0, total-fade):.6f}:d={fade:.6f}"
                cmd += ["-af", audio_filter]
        else:
            cmd += ["-an"]
        if subtitle_input is not None:
            cmd += ["-map", f"{subtitle_input}:s:0", "-c:s", "mov_text"]
        cmd += ["-t", f"{total:.6f}", "-f", "mp4", str(temp)]
        try:
            subprocess.run(cmd, check=True, capture_output=True, text=True, timeout=1800)
        except subprocess.CalledProcessError as exc:
            detail = (exc.stderr or "").strip().splitlines()
            raise MediaError("FFmpeg render failed: " + (detail[-1] if detail else "see FFmpeg log")) from exc
        validate_video(temp, width, height)
        if overwrite:
            os.replace(temp, output)
        else:
            try:
                os.link(temp, output)
            except FileExistsError as exc:
                raise MediaError(f"Output appeared during render; refusing to overwrite: {output}") from exc
            temp.unlink()
    finally:
        if temp.exists():
            temp.unlink()
    return {"output": str(output), "duration_seconds": total, "width": width, "height": height, "fps": fps, "audio": final_audio is not None, "captions": bool(captions)}


def _resolve_output(value, base):
    if not value or not isinstance(value, str):
        raise MediaError("Project output must be a file path")
    path = Path(value).expanduser()
    path = path if path.is_absolute() else base / path
    path = path.resolve()
    if path.suffix.lower() != ".mp4":
        raise MediaError("Output filename must end in .mp4")
    return path
