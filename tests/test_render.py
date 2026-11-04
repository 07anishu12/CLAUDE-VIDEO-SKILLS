"""End-to-end tests for the canonical FFmpeg renderer."""
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "engine"))
from videoskills.media import contact_sheet, validate_video  # noqa: E402
from videoskills.render import render_project  # noqa: E402


@unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "FFmpeg/FFprobe not installed")
class RenderSmokeTests(unittest.TestCase):
    def test_render_two_clips_with_transition_audio_captions_and_contact_sheet(self):
        with tempfile.TemporaryDirectory(prefix="video-skills-render-test-") as tmp:
            base = Path(tmp)
            clips = [base / "one.mp4", base / "two.mp4"]
            colors = ["blue", "orange"]
            for clip, color in zip(clips, colors):
                subprocess.run([
                    "ffmpeg", "-hide_banner", "-loglevel", "error", "-f", "lavfi", "-i",
                    f"color=c={color}:s=160x90:r=12:d=1.5", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-an", str(clip),
                ], check=True, capture_output=True)
            audio = base / "bed.wav"
            subprocess.run([
                "ffmpeg", "-hide_banner", "-loglevel", "error", "-f", "lavfi", "-i",
                "sine=frequency=440:duration=2.6", "-c:a", "pcm_s16le", str(audio),
            ], check=True, capture_output=True)
            captions = base / "captions.srt"
            captions.write_text("1\n00:00:00,000 --> 00:00:01,200\nSynthetic test caption\n", encoding="utf-8")
            output = base / "final.mp4"
            project = base / "project.json"
            project.write_text(json.dumps({
                "clips": [{"path": str(clips[0])}, {"path": str(clips[1])}],
                "audio": str(audio), "captions": str(captions), "output": str(output),
                "width": 160, "height": 90, "fps": 12,
                "transition": {"type": "fade", "duration": 0.25},
            }), encoding="utf-8")
            result = render_project(project)
            info = validate_video(output, 160, 90)
            self.assertTrue(output.is_file() and output.stat().st_size > 0)
            self.assertAlmostEqual(info["duration_seconds"], 2.75, delta=0.3)
            self.assertTrue(info["audio"])
            self.assertTrue(result["captions"])
            sheet = base / "contact.png"
            contact_sheet(output, sheet)
            self.assertGreater(sheet.stat().st_size, 0)

    def test_speed_change_keeps_single_clip_audio_synchronized(self):
        with tempfile.TemporaryDirectory(prefix="video-skills-speed-test-") as tmp:
            base = Path(tmp); source = base / "source.mp4"; output = base / "sped-up.mp4"
            subprocess.run([
                "ffmpeg", "-hide_banner", "-loglevel", "error", "-f", "lavfi", "-i",
                "testsrc=size=160x90:rate=12:duration=2", "-f", "lavfi", "-i",
                "sine=frequency=440:duration=2", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", str(source),
            ], check=True, capture_output=True)
            project = base / "project.json"
            project.write_text(json.dumps({"clips": [{"path": str(source), "speed": 2}], "output": str(output), "width": 160, "height": 90, "fps": 12}), encoding="utf-8")
            render_project(project)
            info = validate_video(output, 160, 90)
            self.assertTrue(info["audio"])
            self.assertAlmostEqual(info["duration_seconds"], 1, delta=0.25)


if __name__ == "__main__":
    unittest.main()
