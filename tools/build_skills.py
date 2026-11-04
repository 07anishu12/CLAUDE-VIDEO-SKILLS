#!/usr/bin/env python3
"""Generate the canonical 80 standalone skill files from the product catalog."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = json.loads((ROOT / "catalog/skills.json").read_text(encoding="utf-8"))

CATEGORY_WORKFLOWS = {
    "Animated videos": [
        "Read the supplied narration/script/lyrics, identify scenes and actions, and make a shot list with timing tied to supplied audio where available.",
        "Create a consistent visual language and recurring-character/prop notes before making shots; use user assets or tools that are actually available.",
        "Build motion and transitions from the narrative beats. Keep subtitles in the original supplied writing system.",
    ],
    "Reel formats": [
        "Find the strongest self-contained hook and useful payoff; preserve the speaker's meaning and do not invent claims.",
        "Plan vertical-safe framing, concise captions, sensible cut points, and a clear ending. Use transcript timing only when supplied or verified.",
        "For long source footage, create candidate segments with in/out points and show the user the edit plan before rendering.",
    ],
    "Motion effects": [
        "Locate the precise spoken, visual, or musical moment where the requested effect communicates meaning; do not cover unrelated content.",
        "Create the effect as a bounded overlay/composite and keep the underlying source readable.",
        "Show a representative still or low-resolution preview of the effect in context before full export.",
    ],
    "Edit styles": [
        "Preserve the original speaker, argument, and natural facial appearance. Identify pauses and emphasis from media rather than invented transcript text.",
        "Apply the named pacing, framing, caption, and graphic treatment consistently across the clip.",
        "Keep captions and interface graphics in platform-safe margins and retain a clean version if the treatment obscures content.",
    ],
    "Looks": [
        "Treat this as a visual finish for supplied footage: preserve shot content and apply the named palette, texture, framing, or graphic presentation.",
        "Compare representative frames before/after so skin tones, highlights, captions, and source detail remain legible.",
        "Avoid suggesting generated footage: use supplied imagery and FFmpeg-supported filters unless a separate media-generation tool is available.",
    ],
}

def make_skill(entry: dict) -> str:
    sid, title, category = entry["id"], entry["title"], entry["category"]
    purpose = (entry.get("purpose") or f"Apply the {title} treatment to user-supplied media.").strip()
    inputs = (entry.get("inputs") or "User-supplied video, images, audio, or script as appropriate to the requested treatment.").strip()
    aspect = "vertical 1080×1920" if category in ("Reel formats", "Edit styles") else "the requested or source aspect ratio"
    cues = "\n".join(f"{i}. {line}" for i, line in enumerate(CATEGORY_WORKFLOWS[category], 1))
    example = f"/{sid} Apply the {title} treatment to my supplied media. Make a review preview first."
    return f'''---
name: {sid}
description: "{purpose.replace(chr(34), chr(39))[:700]} Use for {title.lower()} requests."
---

# {title}

## Purpose
{purpose}

## When to use
Use this specialist for the exact treatment above. Keep its defining look and purpose; do not replace it with a generic cinematic edit.

## Inputs and dependencies
- Expected material: {inputs}
- Accept supported local media such as MP4, MOV, WebM, MP3, WAV, M4A, PNG, JPEG, and WebP when the installed FFmpeg build can decode it.
- Require Python 3.10+ and FFmpeg/FFprobe for rendering. Optional transcription, forced-alignment, 3D, or generative-media tools must be checked before use; never imply they are installed.
- Do not overwrite source media. Do not invent lyrics, claims, dialogue, or precise timestamps.

## Treatment-specific workflow
{cues}
4. Translate the purpose and user references into concrete shots, timing, motion, color, captions, and transitions for this one treatment: {purpose}
5. Select the output ratio from the request; for a reel, start with {aspect}. Preserve the source frame rate when practical, otherwise use 30 fps.

## Render workflow
1. Locate and inspect supplied assets with the installed `video.py inspect` command (in a repository checkout: `python3 engine/video.py inspect path/to/media`); confirm duration, streams, dimensions, and frame rate.
2. Ask only for an essential missing asset. For songs, inspect the audio and estimate BPM only if the optional analyzer is available. Use supplied lyrics or a transcript; use verified timestamps/forced alignment for word timing. If unavailable or uncertain, keep line-level timing approximate and disclose it.
3. Create an edit plan with the shot sequence and output path. Use engine/video.py quick-edit for a trim, crop, speed, grade, audio-bed, or cut-based montage, or write a JSON timeline and run engine/video.py render project.json for per-clip settings and transitions.
4. Make a low-resolution preview render under out/{sid}/preview.mp4 and create a contact sheet. Show the preview/contact sheet and request approval for substantial creative changes.
5. After approval, render the final H.264/AAC MP4 under out/{sid}/final.mp4. Keep source audio by default for a single source clip; for multiple clips, preserve clip audio through the renderer or use a user-selected audio bed.
6. Validate the output with engine/video.py validate file. Report the actual output path and any unavailable effects or alignment features.

## Failure handling
- If FFmpeg/FFprobe is missing, report the missing executable and stop before rendering.
- If a codec is unsupported, identify it from FFprobe and offer a conversion or alternate input.
- If a preview/final render fails, preserve sources and any prior output; report FFmpeg's error and do not claim a completed MP4.
- Ask before replacing any existing output.

## Example
{example}
'''


def main():
    skills_root = ROOT / "skills"
    skills_root.mkdir(exist_ok=True)
    for entry in CATALOG["skills"]:
        folder = skills_root / entry["id"]
        folder.mkdir(exist_ok=True)
        (folder / "SKILL.md").write_text(make_skill(entry), encoding="utf-8")
    routes = "\n".join(
        f"| {item['command']} | {item['category']} | {item['purpose'] or item['title']} |"
        for item in CATALOG["skills"]
    )
    router = f'''---
name: claude-video
description: "Directs AI video editing and production across music videos, lyric videos, reels, animation, explainers, podcasts, footage edits, motion effects, and visual looks. Use when the user asks to make, edit, style, or render a video."
---

# Claude Video

Act as the user's video production director. Understand the intended deliverable, choose the closest specialist command, inspect supplied media, build an editing plan, render a preview, and produce a real validated MP4 when the local engine and input assets support the requested result.

## Route the request

1. Identify the deliverable: song or lyric video, animated story, podcast/talking head, short reel, long-video clip, explainer, news report, cinematic montage, effect, look, or custom edit.
2. Select the best matching specialist from the directory below. Match the user's requested visual treatment and source purpose; do not apply all skills or replace a specific style with a generic edit.
3. If the selected specialist is installed and the host supports invocation, ask the user to invoke its command if no direct chaining mechanism exists. Otherwise read and follow that specialist's workflow in this session. Never claim a skill was invoked when it was not.
4. For multiple compatible treatments, combine only the non-conflicting steps (for example, podcast pacing plus comic graphics). State the chosen treatment briefly.
5. If no specialist fits, apply the common inspection, planning, preview, render, and validation process below.

### Fast routes

- Hindi lyrics / Hindi song text: /hindi-lyric-video. Preserve Devanagari when supplied.
- Madhubani story: /madhubani-kahani.
- Podcast reel with clean cuts and punch-ins: /podcast-reel-edit.
- Comic treatment on a podcast: /podcast-comic.
- Anime fight: /anime-fight.
- 3D explainer: /3d-explainer. Check for Blender and a render-capable setup; this FFmpeg engine does not create 3D scenes.
- News-style explainer: /news-report.
- Watercolor map journey: /watercolor-map.
- Music-led cut timing: /beat-transition-edit. Use measured BPM/beat estimates only when the optional analyzer is installed.
- Talking-head captions: /talking-head-edit.
- Short from long-form video: /youtube-clips.

## Production process

1. Locate and inspect user-provided clips, audio, images, lyrics, transcripts, scripts, and references. Never overwrite source media. Ask only for essential missing material.
2. For a song, inspect duration/streams and run audio analysis. BPM is an estimate; do not treat it as exact. Never infer lyrics from music as ground truth. Use supplied/corrected lyrics and actual alignment data for word timing; if alignment is unavailable, ask for timings or use clearly labeled line-level approximations.
3. For a supplied reference, describe observable shot order, pacing, graphic treatment, aspect ratio, and transitions. Do not promise frame-perfect reconstruction.
4. Produce a concise storyboard/timeline specifying shot lengths, focal content, transitions, text, audio, output ratio, and known tool limits.
5. Discover the engine in this order: environment variable VIDEO_SKILLS_ENGINE pointing to video.py; repository engine/video.py; installed project .claude-video/engine/video.py; installed user engine under the user's home .claude-video/engine/video.py; or a plugin-bundled engine folder. Check --help and dependencies before use.
6. Render a low-resolution proxy using the same timeline (for example 360x640 or 640x360 at 12 fps), then create a contact sheet. Show the preview. Ask approval when style, shot selection, or substantial edits are involved; trivial requested trims do not need an extra approval round.
7. Render the final approved MP4 at vertical 1080x1920 for reels or landscape 1920x1080 for YouTube unless requested otherwise. Preserve audio by default and ask before replacing existing outputs.
8. Validate video stream, duration, dimensions, audio/subtitle tracks, and file size with the engine. Return the exact output path and any unavailable feature.

## What the local engine does

The engine edits user-provided video, image, and audio material with FFmpeg: metadata inspection, trims, multiple-clip concatenation, crop/resize, speed, zoom crop, simple color controls, fades, supported cross-transitions, SRT subtitle tracks, contact sheets, and MP4 validation. It does not synthesize footage, characters, 3D scenes, music, or accurate song lyrics. Use a separate media-generation or transcription model only when it is actually available and authorized.

## Specialist command directory

All 80 individual command names and purposes:

| Command | Category | Best fit |
|---|---|---|
{routes}

## Missing capability handling

If the user asks for generated animation, image generation, forced lyric alignment, or 3D and no suitable model/tool is available, explain the missing component and offer an edit using provided assets. Do not label a still-image montage as generated animation. If the engine or codec fails, preserve all sources, report the actual error, and do not claim a final render.
'''
    router_dir = skills_root / "claude-video"
    router_dir.mkdir(exist_ok=True)
    (router_dir / "SKILL.md").write_text(router, encoding="utf-8")
    print(f"Generated {len(CATALOG['skills'])} canonical specialist skills plus the claude-video router")

if __name__ == "__main__":
    main()
