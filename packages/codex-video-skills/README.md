# Claude Video Skills: Codex and Antigravity bundle

This folder is a generated distribution snapshot of the canonical skill library in [`/skills`](../../skills/). Do not edit copied skills here; update canonical files and regenerate with `python3 tools/build_bundles.py`.

See the [root README](../../README.md) for the 80-skill catalog, installation steps, supported host differences, renderer requirements, and limitations.

Install into a project with the repository installer:

```bash
./installers/install.sh --agent codex --project-dir /path/to/project
./installers/install.sh --agent antigravity --project-dir /path/to/project
```

Codex discovers project skills under `.agents/skills/` and uses `$claude-video` for the router. Antigravity also uses workspace `.agents/skills/`; invoke skills through its current Agent Skills interface. Rendering requires FFmpeg and FFprobe as documented in the root guide.
