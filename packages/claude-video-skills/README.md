# Claude Video Skills for Claude Code

This folder contains the Claude Code installation bundle for the unified Claude Video Skills project. It includes the claude-video router and specialist video workflows. The root [README](../../README.md) has the product overview, examples, limitations, and complete 80-command reference.

## Install in a project

From the repository root, copy the skill folder into the project that will use Claude Code:

~~~bash
mkdir -p /path/to/your-project/.claude
cp -R packages/claude-video-skills/.claude/skills /path/to/your-project/.claude/
~~~

For a personal installation shared across Claude Code projects, use ~/.claude/skills/ instead of the project’s .claude/skills/ directory.

To install just the router, copy packages/claude-video-skills/.claude/skills/claude-video into the target .claude/skills/ directory.

## Use

Start or refresh the Claude Code session, then run:

~~~text
/claude-video
Create a short video from these supplied clips. Show a preview first.
~~~

Claude Code also supports directly invoking a specialist with /skill-name. Use the installed folder name under .claude/skills/; the root README’s full command index contains the preserved specialist command reference and notes where names differ.

## Rendering

The skill files provide instructions. They do not include a full video editor or footage-generation model. Install FFmpeg and FFprobe if the workflow needs the repository media helper, and check optional model or application dependencies before using them.
