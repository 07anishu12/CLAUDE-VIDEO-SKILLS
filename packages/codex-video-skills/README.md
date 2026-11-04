# Claude Video Skills for Codex and compatible agents

This folder contains the Codex installation bundle for the unified Claude Video Skills project. Its skill files follow the Agent Skills folder convention. The root [README](../../README.md) provides the unified product guide, examples, limits, and complete 80-command reference.

## Install in Codex

Copy the bundle into the project where Codex will use it:

~~~bash
mkdir -p /path/to/your-project/.agents
cp -R packages/codex-video-skills/.agents/skills /path/to/your-project/.agents/
~~~

For personal Codex skills shared across projects, use ~/.agents/skills/. Codex’s skill picker is available through /skills; explicit invocation uses the $skill-name syntax. In this existing bundle, the main router folder is codex-video, so use $codex-video.

To install only the router, copy packages/codex-video-skills/.agents/skills/codex-video into the target .agents/skills/ directory.

## Install in Antigravity

Antigravity also discovers workspace skills under .agents/skills/ and supports /skill-name invocation in its app and CLI. The same bundle can be copied into a workspace:

~~~bash
mkdir -p /path/to/your-project/.agents
cp -R packages/codex-video-skills/.agents/skills /path/to/your-project/.agents/
~~~

Antigravity documents ~/.gemini/config/skills/ as its global skill location. This repository’s bundle has not been verified inside an Antigravity session, and no marketplace plugin is included in this folder.

For the router only, copy the codex-video folder instead of the full skills directory.

## Main entry point and specialists

Use natural language with $codex-video in Codex, or /codex-video in Antigravity. For a specialist, select or invoke the installed skill by its folder name. Consult the root README for the complete command list and current differences between the reference names and installed folder names.

## Rendering

The bundle contains instructions, not a complete editor or a generative video model. FFmpeg and FFprobe are needed for the repository’s media helper. Other capabilities depend on available tools and models; verify them before promising generated visuals or precise lyric timing.
