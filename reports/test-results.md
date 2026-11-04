# Test results

Run on 2026-11-04 in the repository checkout.

- PASS — `python3 -m unittest discover -s tests -v`: 8 tests covering installer project/user scopes, full 80-skill installs into all three agent paths, auto-detection, dry run, reinstallation, preservation, uninstall, upgrade backup, static router scenarios, FFmpeg helpers, actual transitions/audio/SRT render, contact sheet, and speed-adjusted audio.
- PASS — `python3 tests/validate_library.py`: 80 unique canonical skills, valid frontmatter and required sections, router references, and expected category counts.
- PASS — `python3 tools/build_bundles.py --check`: Claude and Codex generated skill directories match canonical `skills/` content.
- PASS — `python3 engine/video.py check`: FFmpeg and FFprobe found. Optional librosa was not installed.
- PASS — `python3 engine/video.py --help`: CLI exposes check, inspect, contact-sheet, validate, analyze-audio, render, quick-edit, and subtitle commands.
- PASS — `git diff --check`.

The engine integration tests create temporary synthetic media and validate MP4 output with FFprobe. PowerShell scripts were not executed because PowerShell is unavailable in this environment. Host UI skill discovery was not directly tested in Claude Code, Codex, or Antigravity sessions.
