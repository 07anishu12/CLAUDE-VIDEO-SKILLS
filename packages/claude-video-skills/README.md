# Claude Video Skills — AI Video Editing & Generation Skills for Claude Code

Claude Video Skills is an installable library of reusable Claude Code workflows for AI video editing, music videos, lyric videos, reels, animation, motion graphics, and cinematic video production. Choose a specialist for the requested look and let Claude inspect the media, prepare a preview, then render after your approval.

## Categories

The library preserves the source collection's five categories: Animated videos, Reel formats, Motion effects, Edit styles, and Looks. It includes song-wise production such as lyric-led and beat-synchronized edits, and raw-footage workflows for talking heads, podcasts, interviews, education, and business reels.

## Install

Clone this repository, then copy `.claude/skills/` into your project's `.claude/skills/` directory. For global use, copy the skill folders into `~/.claude/skills/`. Claude Code discovers a skill from each `<skill-name>/SKILL.md`; restart or open a new session if it does not appear. Keep the package `scripts/` directory nearby if you use its media utility.

```sh
mkdir -p /path/to/your-project/.claude
cp -R .claude/skills /path/to/your-project/.claude/
# Global installation:
mkdir -p ~/.claude/skills
cp -R .claude/skills/* ~/.claude/skills/
```

## Invoke

Use `/claude-video` as the natural-language router, or call an individual skill by its listed name:

```text
/claude-video Make a Hindi lyric video from this MP3 and lyrics. Preview first.
/madhubani-kahani Turn this Hindi narration into a painted story video.
/comic-podcast-reel Edit this podcast clip with a comic-book treatment.
```

Direct skill invocation uses Claude Code's standard `/skill-name` convention. The router selects only a relevant workflow; it does not claim programmatic chaining where unsupported.

## Skill directory

The complete per-skill index is in [`../../research/inventory.csv`](../../research/inventory.csv) and the corresponding independently installable folders are under `.claude/skills/`. Each folder contains its own `SKILL.md`.

## Workflow and dependencies

Inputs can include MP4/MOV/WebM video, MP3/WAV/M4A audio, PNG/JPEG/WebP images, scripts, lyrics, and references. Availability depends on local codecs and installed tools. FFmpeg and FFprobe are needed for media inspection and rendering. Use `python3 scripts/media.py inspect <file>`, `contact-sheet <video> <image>`, and `validate <render>`. Some advanced tasks (forced alignment, transcription, animation rendering) require separately installed tools; skills must report missing capabilities rather than invent timing or claim a successful render.

Video workflows preserve source files, prepare a preview/contact sheet when practical, request approval before final rendering, preserve original audio by default, and ask before overwriting outputs. Vertical reels default to 1080×1920 at 30 fps; landscape defaults to 1920×1080 at 30 fps unless a skill or request specifies otherwise.

## Troubleshooting

- Skill not listed: confirm the `SKILL.md` file is under `.claude/skills/<name>/`, has valid YAML frontmatter, then start a fresh Claude Code session.
- Missing codec/tool: install FFmpeg and confirm `ffmpeg` and `ffprobe` are on `PATH`.
- Audio timing uncertain: provide lyrics/transcript or install a suitable forced-alignment tool; do not rely on guessed word timing.
- Preview fails: reduce preview resolution or use a supported input codec, then inspect the FFmpeg error.

## Contributing

Keep each workflow focused, independently installable, and explicit about inputs, preview, render settings, output, and limitations. Add source traceability to `research/inventory.json`; do not copy source prompt text into public files without permission. Validate with `python3 tests/validate_library.py`.
