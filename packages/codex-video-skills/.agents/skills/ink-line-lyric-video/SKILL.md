---
name: ink-line-lyric-video
description: "A fast lyric video drawn as ONE glowing ink line that never breaks, like the Main Aur Tu reel: the line morphs into a new drawing on every key word, with the camera punching on every kick. Use when asked for ink-line lyric video video production or editing.
---

# Ink-line lyric video

## When to use
Use this workflow for ink-line lyric video requests in the **Animated videos** collection. Preserve this specific visual intent; do not substitute a generic cinematic treatment.

## Required assets and formats
- Inputs: a song MP3 and its lyrics, one sung line per row
- Accept common video formats (MP4, MOV, WebM), audio (MP3, WAV, M4A), images (PNG, JPEG, WebP), and text scripts/lyrics when relevant. Confirm installed tools support the detected codec.
- Keep source media read-only. Do not fabricate lyrics, timestamps, quotes, footage, or source-dependent detail.

## Workflow
1. Locate the supplied files and inspect duration, dimensions, frame rate, audio streams, and codec with `ffprobe`. Report missing essential inputs only.
2. Turn the request into a concise production plan specific to this treatment: shots/scenes, timing, typography, motion, transitions, color, and audio behavior. When audio or lyrics are involved, inspect the track and align timing to measured vocal/music events; mark uncertain alignment instead of guessing.
3. Make a working project directory under `out/ink-line-lyric-video/` and keep originals untouched. Use FFmpeg filters or a small reproducible script; use existing footage and assets unless the user requests generated visuals.
4. Render a representative low-resolution preview or contact sheet before the final render. Show it to the user and ask for approval or requested revisions. Never overwrite an existing output without asking.
5. Apply revisions, then render the approved result. Preserve original audio unless asked to change it. Keep titles/captions inside platform safe areas and do not alter a person's appearance automatically.

## Technical settings
- Default: 9:16 vertical, 1080×1920 at 30 fps. Match the source frame rate when that is more appropriate; otherwise use 30 fps.
- Use H.264 video and AAC audio in MP4 for broad playback compatibility. Preserve source aspect ratio through crop/pad decisions made explicit in the plan.
- For lyric or speech captions, preserve the supplied script and writing system; use forced alignment if available. Do not claim word-level accuracy without alignment evidence.

## Outputs and checks
- Save project notes, preview, and final MP4 under `out/ink-line-lyric-video/`.
- Verify the output exists, has non-zero duration, expected dimensions/frame rate, readable audio, and no obvious dropped/blank frames. Provide exact file paths and summarize any limitations.
- If a dependency or alignment tool is missing, explain the limitation and offer a workable reduced workflow rather than claiming success.

## Example
`/ink-line-lyric-video Make a ink-line lyric video from the attached media. Preview first.`
