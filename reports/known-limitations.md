# Known limitations

- The 80 specialist skills are workflow instructions, not 80 separate renderers. They share a local FFmpeg editing engine.
- The engine edits user-provided video, image, and audio. It does not generate novel footage, animation, 3D scenes, music, or speech.
- Accurate transcription, lyric recognition, and forced word alignment are not included. Song lyric timing must be supplied or obtained from a separately installed model and verified.
- BPM and beat estimates are optional, depend on librosa, and are estimates rather than ground truth.
- FFmpeg filter and codec availability depends on the user's build. The renderer supports tested MP4/H.264/AAC output but has not been evaluated across every camera codec or long-form project.
- PowerShell installer scripts and native host-side skill discovery were not testable in this environment.
- No native marketplace plugin package is included. Install skills through the repository installer.
