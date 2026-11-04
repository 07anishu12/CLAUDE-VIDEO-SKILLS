# Codex Video Skills

Codex Video Skills brings reusable AI video editing workflows into Codex. The collection covers video editing, music video creation, lyric treatments, reels, motion effects, animated stories, and looks. Codex reads the skill instructions and uses available local tools; actual editing depends on installed media software and codecs.

## Install and discover

Copy the `.agents/skills/` directory into the root of a project. For personal, cross-project use, copy its skill folders into `~/.agents/skills/`. Each skill must remain in its own folder containing `SKILL.md`. Open or refresh the Codex session so the skill inventory can be discovered.

```sh
mkdir -p /path/to/your-project/.agents
cp -R .agents/skills /path/to/your-project/.agents/
# Personal installation:
mkdir -p ~/.agents/skills
cp -R .agents/skills/* ~/.agents/skills/
```

## Use

Ask Codex naturally or invoke a skill by name where the host exposes skill invocation:

```text
/codex-video Create a Hindi lyric video from the supplied MP3 and lyrics. Show a preview first.
/watercolor-map-journey Make a travel story from these photos and narration.
/particle-chart Add a particle chart at the revenue section in this clip.
```

Codex Video routes a request to one relevant specialist from the five maintained groups: Animated videos, Reel formats, Motion effects, Edit styles, and Looks. It follows the specialist workflow directly if the host does not support programmatic skill chaining.

## Skills and media

There are individual skill folders under `.agents/skills/`. The shared source inventory is [`../../research/inventory.csv`](../../research/inventory.csv). Skills accept common video, audio, image, and text formats when the local FFmpeg build supports them. Install FFmpeg/FFprobe for media inspection, preview sheets, and rendering. `scripts/media.py` offers inspect, contact-sheet, and validation commands.

The default experience keeps original media intact, preserves source audio, prepares a preview for user review, and asks before overwriting an output. Vertical reels default to 1080×1920/30 fps and landscape projects to 1920×1080/30 fps unless specified otherwise. Forced alignment and transcription require separate compatible tools and are not silently simulated.

## Limitations

Skills are instructions, not a bundled video editor or generative media model. Render availability, transcription quality, forced alignment, and codecs depend on the environment. Review the preview and verify the final file before sharing.

## Contributing

Keep the Codex package independently installable and retain `.agents/skills/<name>/SKILL.md` structure. Document dependencies and failure behavior. Run `python3 tests/validate_library.py` before submitting changes. The `LICENSE` covers this project's original implementation; source prompt text and artwork are not redistributed.
