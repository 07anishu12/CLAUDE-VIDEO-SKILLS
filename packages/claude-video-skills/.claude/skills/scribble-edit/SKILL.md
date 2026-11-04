---
name: scribble-edit
description: "Your own clip covered in live marker doodles, like the Justin Bieber “Where Are Ü Now” video from How to do this with Claude (Ep 5): the wall behind you fills with hand-drawn stars, rockets, cats and lightning, crowns and shades stick to your face as you move, a neon line traces your body, and the whole look changes on every beat. Use for scribble doodle edit requests."
---

# Scribble doodle edit

## Purpose
Your own clip covered in live marker doodles, like the Justin Bieber “Where Are Ü Now” video from How to do this with Claude (Ep 5): the wall behind you fills with hand-drawn stars, rockets, cats and lightning, crowns and shades stick to your face as you move, a neon line traces your body, and the whole look changes on every beat.

## When to use
Use this specialist for the exact treatment above. Keep its defining look and purpose; do not replace it with a generic cinematic edit.

## Inputs and dependencies
- Expected material: a 9:16 clip of you moving (a plain wall behind you works best) and the song MP3
- Accept supported local media such as MP4, MOV, WebM, MP3, WAV, M4A, PNG, JPEG, and WebP when the installed FFmpeg build can decode it.
- Require Python 3.10+ and FFmpeg/FFprobe for rendering. Optional transcription, forced-alignment, 3D, or generative-media tools must be checked before use; never imply they are installed.
- Do not overwrite source media. Do not invent lyrics, claims, dialogue, or precise timestamps.

## Treatment-specific workflow
1. Read the supplied narration/script/lyrics, identify scenes and actions, and make a shot list with timing tied to supplied audio where available.
2. Create a consistent visual language and recurring-character/prop notes before making shots; use user assets or tools that are actually available.
3. Build motion and transitions from the narrative beats. Keep subtitles in the original supplied writing system.
4. Translate the purpose and user references into concrete shots, timing, motion, color, captions, and transitions for this one treatment: Your own clip covered in live marker doodles, like the Justin Bieber “Where Are Ü Now” video from How to do this with Claude (Ep 5): the wall behind you fills with hand-drawn stars, rockets, cats and lightning, crowns and shades stick to your face as you move, a neon line traces your body, and the whole look changes on every beat.
5. Select the output ratio from the request; for a reel, start with the requested or source aspect ratio. Preserve the source frame rate when practical, otherwise use 30 fps.

## Render workflow
1. Locate and inspect supplied assets with the installed `video.py inspect` command (in a repository checkout: `python3 engine/video.py inspect path/to/media`); confirm duration, streams, dimensions, and frame rate.
2. Ask only for an essential missing asset. For songs, inspect the audio and estimate BPM only if the optional analyzer is available. Use supplied lyrics or a transcript; use verified timestamps/forced alignment for word timing. If unavailable or uncertain, keep line-level timing approximate and disclose it.
3. Create an edit plan with the shot sequence and output path. Use engine/video.py quick-edit for a trim, crop, speed, grade, audio-bed, or cut-based montage, or write a JSON timeline and run engine/video.py render project.json for per-clip settings and transitions.
4. Make a low-resolution preview render under out/scribble-edit/preview.mp4 and create a contact sheet. Show the preview/contact sheet and request approval for substantial creative changes.
5. After approval, render the final H.264/AAC MP4 under out/scribble-edit/final.mp4. Keep source audio by default for a single source clip; for multiple clips, preserve clip audio through the renderer or use a user-selected audio bed.
6. Validate the output with engine/video.py validate file. Report the actual output path and any unavailable effects or alignment features.

## Failure handling
- If FFmpeg/FFprobe is missing, report the missing executable and stop before rendering.
- If a codec is unsupported, identify it from FFprobe and offer a conversion or alternate input.
- If a preview/final render fails, preserve sources and any prior output; report FFmpeg's error and do not claim a completed MP4.
- Ask before replacing any existing output.

## Example
/scribble-edit Apply the Scribble doodle edit treatment to my supplied media. Make a review preview first.
