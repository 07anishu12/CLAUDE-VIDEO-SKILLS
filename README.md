# Claude Video Skills — AI Video Editing & Generation Skills for Claude Code

Video Skills Core is the shared engineering project behind **Claude Video Skills** and **Codex Video Skills**: installable agent workflows for video editing, music videos, reels, animation, motion effects, edit styles, and looks.

The source audit covered [aanshai.vercel.app/skills](https://aanshai.vercel.app/skills). It advertised and exposed 80 entries across the site's original five categories. The local research archive and audit are in `research/`; source prompt text is excluded from version control because redistribution permission was not established. Public skill instructions are independently authored.

## Distributions

- [Claude Video Skills](packages/claude-video-skills/README.md) — Claude Code skills in `.claude/skills/`.
- [Codex Video Skills](packages/codex-video-skills/README.md) — Codex skills in `.agents/skills/`.

## Repository layout

- `packages/` — separate, installable platform packages.
- `packages/shared-skills/` — shared skill source set.
- `shared/scripts/media.py` — FFmpeg-backed inspection, preview contact-sheet, and output validation utility.
- `research/` — source inventory, audit, extraction log, and local excluded prompt archive.
- `reports/` — coverage, validation, and limitations.

## Validation

Run `python3 tests/validate_library.py` and `python3 -m unittest discover -s tests -v` to validate inventory/manifests and smoke-test the media helper with a temporary synthetic clip. Run `python3 shared/scripts/media.py --help` to inspect the media utility commands. FFmpeg and FFprobe are required for media operations.

## Source attribution

The source inventory records names, categories, commands, descriptions, input cues, and source anchors for traceability. It does not grant rights to source prompt text or artwork. Do not redistribute those materials without permission or a compatible license.
