#!/usr/bin/env python3
"""Smoke-test FFmpeg helpers with a temporary synthetic fixture."""
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "shared/scripts/media.py"


@unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "FFmpeg/FFprobe not installed")
class MediaSmokeTests(unittest.TestCase):
    def test_inspect_contact_sheet_validate(self):
        with tempfile.TemporaryDirectory(prefix="video-skills-test-") as tmp:
            base = Path(tmp)
            movie, sheet = base / "fixture.mp4", base / "contact.png"
            subprocess.run([
                "ffmpeg", "-hide_banner", "-loglevel", "error", "-f", "lavfi", "-i", "color=c=blue:s=160x90:d=1",
                "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100", "-t", "1", "-c:v", "libx264",
                "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", "-y", str(movie),
            ], check=True)
            result = subprocess.run(["python3", str(CLI), "inspect", str(movie)], check=True, capture_output=True, text=True)
            info = json.loads(result.stdout)
            self.assertEqual((info["video"]["width"], info["video"]["height"]), (160, 90))
            self.assertTrue(info["audio"])
            subprocess.run(["python3", str(CLI), "contact-sheet", str(movie), str(sheet)], check=True, capture_output=True)
            self.assertGreater(sheet.stat().st_size, 0)
            subprocess.run(["python3", str(CLI), "validate", str(movie), "--width", "160", "--height", "90"], check=True, capture_output=True)


if __name__ == "__main__":
    unittest.main()
