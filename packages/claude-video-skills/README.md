# Claude Video Skills: Claude Code bundle

This folder is a generated distribution snapshot of the canonical skill library in [`/skills`](../../skills/). Do not edit copied skills here; update the canonical files and regenerate with `python3 tools/build_bundles.py`.

For the full 80-skill catalog, platform guidance, verified capabilities, and current installation steps, see the [root README](../../README.md).

Install into a project with the repository installer:

```bash
./installers/install.sh --agent claude --project-dir /path/to/project
```

Claude Code discovers skills under `.claude/skills/` and invokes the main router as `/claude-video`. Rendering requires the separate FFmpeg/FFprobe tools described in the root guide.
