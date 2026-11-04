# Claude Video Skills — AI Video Editing & Generation Skills for Claude Code, Codex and AI Agents

Claude Video Skills is an open collection of **80 specialized video-production workflows** and one intelligent entry point, **claude-video**. Describe the result you want; a compatible coding agent can inspect your assets, select a relevant workflow, help plan an edit, and use the tools available in your environment.

Create or edit music videos, Hindi and English lyric videos, Reels, YouTube Shorts, podcast clips, animated stories, cinematic edits, explainers, motion graphics, talking-head videos, educational and news-style videos, B-roll edits, kinetic typography, social videos, and video presentations.

This is an independent community project. It is not affiliated with Anthropic, OpenAI, Google, or Gemini. Agent instructions guide a workflow; they are not themselves an AI video-generation model. Actual editing and rendering depend on the installed engine, codecs, models, and tools.

For Claude Code video editing and AI-assisted video production, Claude Video Skills combines reusable AI agent skills with a small FFmpeg utility. Use compatible tools for video editing automation; a video production agent can guide the workflow, while the host and installed tools perform the actual work.

## Quick installation

Clone the repository, then run the installer for the project where you want to use the skills. It installs canonical skills and the local engine without replacing unrelated files.

### Claude Code

~~~bash
git clone https://github.com/07anishu12/CLAUDE-VIDEO-SKILLS.git
cd CLAUDE-VIDEO-SKILLS
./installers/install.sh --agent claude --project-dir /path/to/your-project
~~~

For just the main skill:

~~~bash
./installers/install.sh --agent claude --project-dir /path/to/your-project --skills claude-video
~~~

### OpenAI Codex

~~~bash
./installers/install.sh --agent codex --project-dir /path/to/your-project
~~~

Codex also discovers personal skills in `~/.agents/skills/`. Browse with `/skills` or invoke the router with `$claude-video`.

To install only that router:

~~~bash
./installers/install.sh --agent codex --project-dir /path/to/your-project --skills claude-video
~~~

### Google Antigravity

Antigravity supports Agent Skills in the workspace `.agents/skills/` directory. Install the canonical skills with:

~~~bash
./installers/install.sh --agent antigravity --project-dir /path/to/your-project
~~~

Antigravity discovers workspace skills from `.agents/skills/` and supports slash invocation in its agent interface. For user-level installation, the installer targets `~/.gemini/config/skills/`.

To install only the router:

~~~bash
./installers/install.sh --agent antigravity --project-dir /path/to/your-project --skills claude-video
~~~

The installer also supports `--agent auto`, `--scope user`, `--dry-run`, `--upgrade`, and `--uninstall`. Because Codex and Antigravity share `.agents/skills/`, auto-detection asks you to select one unless the host provides a detectable environment variable. If a managed target differs from the package, installation stops unless `--upgrade` is given; upgrades save a backup. On Windows, use `installers/install.ps1` and `installers/uninstall.ps1`. Refresh the agent session after installation.

## Supported agents

The skills use the portable Agent Skills format. Claude Code discovers project skills in `.claude/skills/` ([official docs](https://code.claude.com/docs/en/skills)). Codex and Antigravity discover workspace skills in `.agents/skills/` ([Codex docs](https://learn.chatgpt.com/docs/build-skills), [Antigravity docs](https://antigravity.google/docs/skills?app=antigravity-ide)). Invocation differs by host: Claude Code uses `/skill-name`, Codex supports `$skill-name`, and Antigravity uses its Agent Skills interface. Compatibility depends on each host's current discovery behavior.

## What you can create

- AI-assisted music videos and lyric videos in Hindi, English, and other supplied languages
- Instagram Reels, YouTube Shorts, podcast clips, and talking-head edits
- Animated stories, comic treatments, watercolor-style videos, and explainers
- Cinematic montages, news-style videos, educational edits, and B-roll sequences
- Motion graphics, typography, captions, transitions, and video presentations

The skills help an agent choose and execute a workflow. They do not promise generated footage: a separate image, video, transcription, or alignment model is needed for those capabilities. Use supplied media when no generation model is available.

## The main claude-video command

In Claude Code, invoke the router with /claude-video and describe the deliverable in natural language. It is intended to select the closest specialist workflow and guide the work based on the files and tools available.

~~~text
/claude-video

Create a Hindi lyric video from this song.
Use cinematic visuals and synchronized lyrics.
~~~

~~~text
/claude-video

Turn this podcast into a 45-second Instagram Reel.
Add captions, transitions and B-roll.
~~~

~~~text
/claude-video

Create an animated story from this script.
Use a watercolor illustration style.
~~~

~~~text
/claude-video

Make a cinematic music video using these images and audio.
~~~

In Codex, invoke the router as `$claude-video`. In Antigravity, invoke `/claude-video` where slash skill invocation is enabled, or let the agent select it from `.agents/skills/`.

## All 80 Video Skills & Commands

The command reference below lists the 80 canonical specialist skill names. Each command matches its installed folder name, so the same specialist is independently discoverable in every supported skill directory.

### Animated videos

| Command | What it does |
|---|---|
| /3d-explainer | Create animated 3D-style educational explainers. |
| /aarti-video | Create devotional and aarti-themed videos. |
| /anime-fight | Create anime-style fight sequences. |
| /anime-reel | Create anime-inspired short videos. |
| /baba-pusho | Create the corresponding character/story video workflow. |
| /bairan-style | Create videos using the corresponding visual style. |
| /beat-transition-edit | Synchronize video transitions with musical beats. |
| /blueprint-explainer | Create blueprint-inspired animated explainers. |
| /comic-reel | Create comic-book-style short videos. |
| /crayon-carousel | Create crayon-style illustrated video sequences. |
| /flicker-edit | Create flicker-based editing effects. |
| /glass-to-neon-lyrics | Create glass-to-neon lyric animations. |
| /glow-lyrics | Create glowing animated lyric videos. |
| /hindi-lyric-video | Create Hindi lyric videos. |
| /ink-line-lyrics | Create ink-line lyric animations. |
| /katha-video | Create animated storytelling and katha videos. |
| /kids-story | Create animated children's stories. |
| /kinetic-lyrics | Create kinetic typography lyric videos. |
| /latent-comic | Create comic-inspired visual storytelling. |
| /latent-reel | Create stylized short-form reels. |
| /lyric-video | Create synchronized lyric videos. |
| /madhubani-kahani | Create Madhubani-inspired animated stories. |
| /madira-peekar-soo-gaye | Create the corresponding music/story video. |
| /maut-ke-bare-mai-sochte-ho | Create the corresponding narrative video. |
| /minimal-lyrics | Create minimalist lyric videos. |
| /mirzapur-video | Create the corresponding cinematic visual style. |
| /neon-lyrics | Create neon-themed lyric videos. |
| /news-report | Create news-report-style videos. |
| /night-glow-lyrics | Create night-glow lyric animations. |
| /painted-beat-edit | Create painted visuals synchronized with music. |
| /paper-cutout | Create paper-cutout animation videos. |
| /party-lyrics | Create energetic party lyric videos. |
| /personal-explainer | Create personalized explainer videos. |
| /pink-spotify-clip-lyrics | Create Spotify-inspired pink lyric clips. |
| /podcast-cartoon | Convert podcast content into cartoon-style videos. |
| /podcast-comic | Create comic-style podcast videos. |
| /podcast-explainer | Convert podcast topics into explainer videos. |
| /pusho-reel | Create the corresponding short-form video workflow. |
| /rap-video | Create rap music videos. |
| /red-rap-lyrics | Create red-themed rap lyric animations. |
| /scribble-edit | Create scribble-based editing effects. |
| /shadow-puppet | Create shadow-puppet-style animations. |
| /sketch-doodle-edit | Create sketch and doodle editing effects. |
| /sketch-music-video | Create sketch-style music videos. |
| /sketch-to-motion | Transform sketch visuals into motion. |
| /spotify-particle-lyrics | Create particle-based Spotify-inspired lyric videos. |
| /street-interview | Create street-interview-style videos. |
| /talking-head-edit | Edit talking-head videos. |
| /titan-anime | Create the corresponding anime-inspired video workflow. |
| /watercolor-lyrics | Create watercolor lyric videos. |
| /watercolor-map | Create watercolor animated map journeys. |
| /woof-woof | Create the corresponding playful animated video workflow. |

### Reel formats

| Command | What it does |
|---|---|
| /business-short-form-reels | Create business-focused short-form reels. |
| /depth-ui-reel | Create depth-based user-interface reels. |
| /educational-youtube-editor | Edit educational YouTube videos. |
| /personal-broll-library | Organize and use personal B-roll footage. |
| /personal-short-form-reels | Create personalized short-form reels. |
| /ranking-format | Create ranking and tier-list videos. |
| /youtube-clips | Convert longer YouTube videos into shorter clips. |

### Motion effects

| Command | What it does |
|---|---|
| /glass-stat-card | Create glass-style animated statistic cards. |
| /led-matrix-text | Create LED-matrix typography effects. |
| /match-cut | Create match-cut transitions. |
| /particle-chart | Create animated particle-based charts. |
| /particle-text | Create particle-based typography. |
| /price-tag-zoom | Create price-tag zoom effects. |
| /shutter-stack | Create shutter-stack transitions. |

### Edit styles

| Command | What it does |
|---|---|
| /dark-red-timeline-motion-graphics | Create dark-red timeline motion graphics. |
| /hindi-pastel-reel-edit | Create Hindi reels with pastel styling. |
| /instagram-ui-hinglish | Create Hinglish videos with Instagram-inspired UI. |
| /iphone-style-by-aansh | Create iPhone-style UI video overlays. |
| /kinetic-talking-head-edit | Create kinetic talking-head edits. |
| /podcast-reel-edit | Edit podcasts into engaging reels. |
| /red-kinetic-collage-edit | Create red kinetic collage videos. |

### Looks

| Command | What it does |
|---|---|
| /breaking-news | Create breaking-news-style video layouts. |
| /cinema-scope | Apply cinematic CinemaScope styling. |
| /comic-halftone | Apply comic halftone visual effects. |
| /magazine-cover | Create animated magazine-cover visuals. |
| /neon-outline | Apply neon outline effects. |
| /rgb-glitch-live | Create RGB glitch effects. |
| /triptych-timecode | Create triptych and timecode layouts. |

## Example workflows

~~~text
$claude-video
Edit this interview into a 30-second vertical short. Keep the original audio.
~~~

~~~text
/claude-video
Use these supplied photos and this audio to make a landscape slideshow. Preview before final export.
~~~

~~~text
/claude-video
Add the particle-chart treatment to the moment I discuss quarterly revenue.
~~~

## Video engine and dependencies

The repository includes an FFmpeg-backed editing engine for:

- Inspecting media metadata with FFprobe
- Creating contact sheets
- Rendering a JSON timeline with trims, multiple clips, crop/resize, speed, zoom, basic color controls, cut concatenation, supported cross-transitions, optional audio beds/fades, and SRT subtitle tracks
- Validating that a rendered MP4 has a video stream, duration, and expected dimensions

Install FFmpeg and FFprobe and make both commands available on your PATH. The CLI is `engine/video.py`:

~~~bash
python3 engine/video.py --help
python3 engine/video.py check
python3 engine/video.py inspect path/to/media.mp4
python3 engine/video.py contact-sheet path/to/video.mp4 out/contact.png
python3 engine/video.py quick-edit --input path/to/video.mp4 --output out/final.mp4 --width 1080 --height 1920
python3 engine/video.py validate out/final.mp4
~~~

For a complete timeline, `engine/video.py render project.json` accepts explicit clip/audio/caption paths and supported filters. Audio analysis measures silence with FFmpeg; BPM estimates are optional and require librosa. No transcription, forced lyric alignment, image/video generation model, 3D scene generator, or generative API is bundled. There is no native Claude or Antigravity plugin package; use the verified skill installer for those hosts.

Skills are agent instructions; the Python/FFmpeg engine performs concrete edits to supplied media; external models are separate optional tools; the rendered MP4 is the output artifact. The engine does not generate novel footage by itself.

## Output formats

The renderer exports H.264/AAC MP4, with optional SRT captions muxed as a text subtitle track. Timeline dimensions and frame rate are configurable; the CLI defaults to vertical 1080×1920 at 30 fps. Inspect every output before sharing it.

## Troubleshooting

- **A skill is missing:** Confirm it was copied into the correct agent directory and refresh or restart the agent session.
- **The helper cannot inspect a file:** Check that FFmpeg/FFprobe are installed and that the input codec is supported.
- **A command name is not found:** Confirm the canonical command folder is present under the platform's skill directory, then refresh the agent session.
- **Lyrics are mistimed:** Provide corrected lyric text and timestamps or install a compatible alignment tool. Do not assume song transcription is accurate.
- **A requested visual cannot be rendered:** The workflow may need a separate image/video-generation model or animation application. Use available assets and disclose tool limits.

## Common questions

### Does this generate video in Claude, ChatGPT, or Google Gemini?

No model is bundled here. The skills provide instructions that compatible agents can follow with available local tools. Claude Code skills, OpenAI Codex skills, and Google Antigravity skills are discovered through each host’s own mechanism. ChatGPT video editing, Google Gemini video generation, or Claude AI video generation requires a compatible agent surface and separate media-generation capability; this repository does not provide those models.

### Can I use this as an AI lyric video creator or AI reel editor?

It provides AI lyric video and AI reel-editing workflows, not a generative model. Accurate song lyrics and word-level timing require user-provided text or a suitable transcription/alignment tool. AI animation skills also need a compatible image/video-generation or animation tool to create new imagery.

### Can I use these with ChatGPT, Gemini, or other AI agents?

Possibly. ChatGPT or Gemini agent environments and other coding agents must support the Agent Skills folder format and provide access to the filesystem and required media tools. This project does not claim native ChatGPT Video Editing or Gemini Video integration, or compatibility with every agent.

## Limitations

Claude Video Skills provides agent instructions and a small media helper. It does not guarantee generated footage or a finished render for every style. Rendering depends on FFmpeg, the input codecs, the host agent’s file/shell tools, optional external models, and the specific workflow. Native skill discovery and invocation vary by agent.

## Contributing

Keep skill descriptions accurate about their inputs, required dependencies, rendering steps, and limits. Run the repository’s validation and media smoke tests before submitting changes. Avoid introducing external credentials or overwriting user media.

## License

This repository is distributed under the [MIT License](LICENSE).
