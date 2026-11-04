---
name: shutter-stack
description: "Photo cards that drop in on a camera flash, stacking up. Use for shutter stack requests."
---

# Shutter stack

## Purpose
Photo cards that drop in on a camera flash, stacking up.

## When to use
Use this specialist for the exact treatment above. Keep its defining look and purpose; do not replace it with a generic cinematic edit.

## Inputs and dependencies
- Expected material: a 9:16 talking-head clip
- Accept supported local media such as MP4, MOV, WebM, MP3, WAV, M4A, PNG, JPEG, and WebP when the installed FFmpeg build can decode it.
- Require Python 3.10+ and FFmpeg/FFprobe for rendering. Optional transcription, forced-alignment, 3D, or generative-media tools must be checked before use; never imply they are installed.
- Do not overwrite source media. Do not invent lyrics, claims, dialogue, or precise timestamps.

## Treatment-specific workflow
1. Locate the precise spoken, visual, or musical moment where the requested effect communicates meaning; do not cover unrelated content.
2. Create the effect as a bounded overlay/composite and keep the underlying source readable.
3. Show a representative still or low-resolution preview of the effect in context before full export.
4. Translate the purpose and user references into concrete shots, timing, motion, color, captions, and transitions for this one treatment: Photo cards that drop in on a camera flash, stacking up.
5. Select the output ratio from the request; for a reel, start with the requested or source aspect ratio. Preserve the source frame rate when practical, otherwise use 30 fps.

## Render workflow
1. Locate and inspect supplied assets with the installed `video.py inspect` command (in a repository checkout: `python3 engine/video.py inspect path/to/media`); confirm duration, streams, dimensions, and frame rate.
2. Ask only for an essential missing asset. For songs, inspect the audio and estimate BPM only if the optional analyzer is available. Use supplied lyrics or a transcript; use verified timestamps/forced alignment for word timing. If unavailable or uncertain, keep line-level timing approximate and disclose it.
3. Create an edit plan with the shot sequence and output path. Use engine/video.py quick-edit for a trim, crop, speed, grade, audio-bed, or cut-based montage, or write a JSON timeline and run engine/video.py render project.json for per-clip settings and transitions.
4. Make a low-resolution preview render under out/shutter-stack/preview.mp4 and create a contact sheet. Show the preview/contact sheet and request approval for substantial creative changes.
5. After approval, render the final H.264/AAC MP4 under out/shutter-stack/final.mp4. Keep source audio by default for a single source clip; for multiple clips, preserve clip audio through the renderer or use a user-selected audio bed.
6. Validate the output with engine/video.py validate file. Report the actual output path and any unavailable effects or alignment features.

## Failure handling
- If FFmpeg/FFprobe is missing, report the missing executable and stop before rendering.
- If a codec is unsupported, identify it from FFprobe and offer a conversion or alternate input.
- If a preview/final render fails, preserve sources and any prior output; report FFmpeg's error and do not claim a completed MP4.
- Ask before replacing any existing output.

## Example
/shutter-stack Apply the Shutter stack treatment to my supplied media. Make a review preview first.
