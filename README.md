# Claude Video Skills — AI Video Editing & Generation Skills for Claude Code, Codex and AI Agents

Claude Video Skills is an open collection of **80 specialized video-production workflows** and one intelligent entry point, **claude-video**. Describe the result you want; a compatible coding agent can inspect your assets, select a relevant workflow, help plan an edit, and use the tools available in your environment.

Create or edit music videos, Hindi and English lyric videos, Reels, YouTube Shorts, podcast clips, animated stories, cinematic edits, explainers, motion graphics, talking-head videos, educational and news-style videos, B-roll edits, kinetic typography, social videos, and video presentations.

This is an independent community project. It is not affiliated with Anthropic, OpenAI, Google, or Gemini. Agent instructions guide a workflow; they are not themselves an AI video-generation model. Actual editing and rendering depend on the installed engine, codecs, models, and tools.

For Claude Code video editing and AI-assisted video production, Claude Video Skills combines reusable AI agent skills with a small FFmpeg utility. Use compatible tools for video editing automation; a video production agent can guide the workflow, while the host and installed tools perform the actual work.

## Quick installation

Clone the repository, then copy the appropriate skills folder into the project where you use your agent.

### Claude Code

~~~bash
git clone https://github.com/07anishu12/CLAUDE-VIDEO-SKILLS.git
cd CLAUDE-VIDEO-SKILLS
mkdir -p /path/to/your-project/.claude
cp -R packages/claude-video-skills/.claude/skills /path/to/your-project/.claude/
~~~

For just the main skill:

~~~bash
mkdir -p /path/to/your-project/.claude/skills
cp -R packages/claude-video-skills/.claude/skills/claude-video /path/to/your-project/.claude/skills/
~~~

### OpenAI Codex

~~~bash
mkdir -p /path/to/your-project/.agents
cp -R packages/codex-video-skills/.agents/skills /path/to/your-project/.agents/
~~~

Codex also discovers personal skills in ~/.agents/skills/. In Codex, use /skills to browse or type $ and select a skill. The current Codex bundle names its router codex-video, so invoke it as $codex-video.

To install only that router:

~~~bash
mkdir -p /path/to/your-project/.agents/skills
cp -R packages/codex-video-skills/.agents/skills/codex-video /path/to/your-project/.agents/skills/
~~~

### Google Antigravity

Antigravity supports Agent Skills in the workspace .agents/skills/ directory. You can use the same skill files:

~~~bash
mkdir -p /path/to/your-project/.agents
cp -R packages/codex-video-skills/.agents/skills /path/to/your-project/.agents/
~~~

Antigravity discovers relevant skills automatically; the Antigravity app and CLI also support /<skill-name> invocation. In the current bundle, the router folder is named codex-video. For global installation, Antigravity documents ~/.gemini/config/skills/.

To install only the router, copy the codex-video folder into your project’s .agents/skills/ directory:

~~~bash
mkdir -p /path/to/your-project/.agents/skills
cp -R packages/codex-video-skills/.agents/skills/codex-video /path/to/your-project/.agents/skills/
~~~

The repository does not currently include a one-command installer. These copy commands install the checked-in skill folders without replacing unrelated skills. Start a new session or reload skills after installation if needed.

## Supported agents

The skills use the portable Agent Skills format. Claude Code discovers project skills in .claude/skills/ ([official docs](https://code.claude.com/docs/en/skills)). Codex and Antigravity discover workspace skills in .agents/skills/ ([Codex docs](https://learn.chatgpt.com/docs/build-skills), [Antigravity docs](https://antigravity.google/docs/skills?app=antigravity-ide)). Skill invocation differs by host: Claude Code uses /skill-name, Codex supports explicit selection through $skill-name, and Antigravity supports /skill-name in its app and CLI. Compatibility depends on the host implementing this format and its local discovery behavior.

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

In Codex, choose the codex-video skill with $codex-video; in Antigravity, use /codex-video or let the agent select it based on your request. Skill invocation names are platform-specific.

## All 80 Video Skills & Commands

The command reference below preserves all 80 specialist names. The existing platform bundles are organized by descriptive skill-folder names; a few differ from these command aliases. In those cases, invoke the installed folder name shown under the selected package’s skills directory.

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
$codex-video
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

The repository includes a small FFmpeg-backed media helper for:

- Inspecting media metadata with FFprobe
- Creating a contact sheet from video
- Validating that a rendered video has a video stream, duration, and expected dimensions

Install FFmpeg and FFprobe and make both commands available on your PATH. Run the helper from the repository root:

~~~bash
python3 shared/scripts/media.py --help
python3 shared/scripts/media.py inspect path/to/media.mp4
python3 shared/scripts/media.py contact-sheet path/to/video.mp4 out/contact.png
python3 shared/scripts/media.py validate out/final.mp4
~~~

The helper does not currently provide a general-purpose timeline renderer, AI footage generation, speech recognition, or forced lyric alignment. Those capabilities depend on other local tools or models and should be checked before promising a result.

FFmpeg video automation here means media inspection, contact-sheet creation, and output checks. It is not a standalone music video generator or AI animation model.

## Output formats

The helper inspects existing files and validates video outputs, including MP4. Skills may instruct an agent to render with available local media tools. Resolution, frame rate, codecs, captions, and other output details depend on the chosen workflow and installed tools; inspect the result before sharing it.

## Troubleshooting

- **A skill is missing:** Confirm it was copied into the correct agent directory and refresh or restart the agent session.
- **The helper cannot inspect a file:** Check that FFmpeg/FFprobe are installed and that the input codec is supported.
- **A command name is not found:** Use the skill folder name currently installed in the platform package; some catalog aliases differ from bundle folder names.
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
