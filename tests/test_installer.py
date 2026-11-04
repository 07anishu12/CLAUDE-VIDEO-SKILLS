"""Exercise installer behavior only in temporary projects and homes."""
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANAGER = ROOT / "installers/manage.py"


class InstallerTests(unittest.TestCase):
    def run_manager(self, home, project, *args, extra_env=None):
        env = dict(os.environ, HOME=str(home))
        env.pop("CODEX_HOME", None); env.pop("CODEX_CLI", None)
        env.pop("ANTIGRAVITY_HOME", None); env.pop("AGY_HOME", None); env.pop("ANTIGRAVITY", None)
        env.pop("CLAUDE_CODE", None); env.pop("CLAUDE_CODE_SSE_PORT", None)
        if extra_env:
            env.update(extra_env)
        return subprocess.run([sys.executable, str(MANAGER), "--project-dir", str(project), *args], env=env, capture_output=True, text=True)

    def test_platform_paths_dry_run_reinstall_preservation_and_uninstall(self):
        with tempfile.TemporaryDirectory(prefix="video-skills-installer-test-") as temp:
            base = Path(temp); home = base / "home"; home.mkdir()
            for agent, rel in (("claude", ".claude/skills"), ("codex", ".agents/skills"), ("antigravity", ".agents/skills")):
                project = base / agent; project.mkdir()
                existing = project / rel / "unrelated" / "SKILL.md"
                existing.parent.mkdir(parents=True); existing.write_text("keep me", encoding="utf-8")
                dry = self.run_manager(home, project, "--agent", agent, "--skills", "claude-video", "--dry-run")
                self.assertEqual(dry.returncode, 0, dry.stderr)
                self.assertFalse((project / rel / "claude-video/SKILL.md").exists())
                install = self.run_manager(home, project, "--agent", agent, "--skills", "claude-video")
                self.assertEqual(install.returncode, 0, install.stderr)
                skill = project / rel / "claude-video/SKILL.md"
                self.assertTrue(skill.is_file())
                again = self.run_manager(home, project, "--agent", agent, "--skills", "claude-video")
                self.assertEqual(again.returncode, 0, again.stderr)
                self.assertEqual(existing.read_text(encoding="utf-8"), "keep me")
                removed = self.run_manager(home, project, "--agent", agent, "--uninstall")
                self.assertEqual(removed.returncode, 0, removed.stderr)
                self.assertFalse(skill.exists())
                self.assertEqual(existing.read_text(encoding="utf-8"), "keep me")

    def test_auto_detection_and_modified_file_preservation(self):
        with tempfile.TemporaryDirectory(prefix="video-skills-installer-auto-") as temp:
            base = Path(temp); home = base / "home"; home.mkdir(); project = base / "project"; project.mkdir()
            (project / ".claude").mkdir()
            installed = self.run_manager(home, project, "--agent", "auto", "--skills", "claude-video")
            self.assertEqual(installed.returncode, 0, installed.stderr)
            skill = project / ".claude/skills/claude-video/SKILL.md"
            skill.write_text("user changed this", encoding="utf-8")
            removed = self.run_manager(home, project, "--agent", "claude", "--uninstall")
            self.assertEqual(removed.returncode, 0, removed.stderr)
            self.assertEqual(skill.read_text(encoding="utf-8"), "user changed this")

    def test_full_library_install_and_ambiguous_agents(self):
        with tempfile.TemporaryDirectory(prefix="video-skills-installer-full-") as temp:
            base = Path(temp); home = base / "home"; home.mkdir()
            for agent, rel in (("claude", ".claude/skills"), ("codex", ".agents/skills"), ("antigravity", ".agents/skills")):
                project = base / f"full-{agent}"; project.mkdir()
                result = self.run_manager(home, project, "--agent", agent)
                self.assertEqual(result.returncode, 0, result.stderr)
                root = project / rel
                self.assertEqual(len(list(root.glob("*/SKILL.md"))), 81)
                self.assertTrue((project / ".claude-video/engine/video.py").is_file())
            ambiguous = base / "ambiguous"; ambiguous.mkdir(); (ambiguous / ".agents").mkdir()
            result = self.run_manager(home, ambiguous, "--agent", "auto", "--skills", "claude-video")
            self.assertEqual(result.returncode, 2)
            self.assertIn("choose --agent explicitly", result.stderr)

    def test_codex_environment_detection_user_scope_and_upgrade_backup(self):
        with tempfile.TemporaryDirectory(prefix="video-skills-installer-scope-") as temp:
            base = Path(temp); home = base / "home"; home.mkdir(); project = base / "project"; project.mkdir()
            result = self.run_manager(home, project, "--agent", "auto", "--scope", "user", "--skills", "claude-video", extra_env={"CODEX_HOME": str(home / ".codex")})
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((home / ".agents/skills/claude-video/SKILL.md").is_file())

            conflict_project = base / "conflict"; conflict_project.mkdir()
            target = conflict_project / ".claude/skills/claude-video/SKILL.md"
            target.parent.mkdir(parents=True); target.write_text("pre-existing user content", encoding="utf-8")
            refused = self.run_manager(home, conflict_project, "--agent", "claude", "--skills", "claude-video")
            self.assertEqual(refused.returncode, 2)
            self.assertEqual(target.read_text(encoding="utf-8"), "pre-existing user content")
            upgraded = self.run_manager(home, conflict_project, "--agent", "claude", "--skills", "claude-video", "--upgrade")
            self.assertEqual(upgraded.returncode, 0, upgraded.stderr)
            self.assertNotEqual(target.read_text(encoding="utf-8"), "pre-existing user content")
            backups = list((conflict_project / ".claude-video/backups").rglob("*SKILL.md"))
            self.assertEqual(len(backups), 1)
            self.assertEqual(backups[0].read_text(encoding="utf-8"), "pre-existing user content")


if __name__ == "__main__":
    unittest.main()
