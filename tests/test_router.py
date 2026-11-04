"""Static route coverage for realistic router scenarios (not a model evaluation)."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = json.loads((ROOT / "catalog/skills.json").read_text(encoding="utf-8"))
SKILLS = {item["id"] for item in CATALOG["skills"]}
ROUTER = (ROOT / "skills/claude-video/SKILL.md").read_text(encoding="utf-8")


class RouterRouteTests(unittest.TestCase):
    def test_expected_specialists_are_present_for_user_scenarios(self):
        scenarios = {
            "Create a Hindi lyric video": "hindi-lyric-video",
            "Edit a podcast into short-form reels": "podcast-reel-edit",
            "Create an animated educational explainer": "3d-explainer",
            "Produce a cinematic music video": "beat-transition-edit",
            "Create a news-style video": "news-report",
            "Add motion graphics and particle effects": "particle-text",
            "Turn a long video into multiple short clips": "youtube-clips",
            "Create a video using supplied footage and audio": "lyric-video",
            "Combine animation, transitions, captions, and music": "beat-transition-edit",
            "Handle a request without a specialist": None,
        }
        for request, skill in scenarios.items():
            with self.subTest(request=request):
                if skill:
                    self.assertIn(skill, SKILLS)
                    self.assertIn(f"/{skill}", ROUTER)
        self.assertIn("For multiple compatible treatments", ROUTER)
        self.assertIn("If no specialist fits", ROUTER)
        self.assertIn("ask only for essential", ROUTER.lower())
        self.assertIn("Never claim a skill was invoked", ROUTER)
        self.assertIn("does not synthesize footage", ROUTER)


if __name__ == "__main__":
    unittest.main()
