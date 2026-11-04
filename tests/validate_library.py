#!/usr/bin/env python3
"""Validate inventory coverage and installable platform skill bundles."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
data = json.loads((ROOT / "research/inventory.json").read_text())
entries = data["skills"]
assert len(entries) == data["actual_count"] == 80, f"inventory count mismatch: {len(entries)}"
assert len({e["source_id"] for e in entries}) == len(entries), "duplicate source IDs"
assert len({e["new_skill_id"] for e in entries}) == len(entries), "duplicate skill IDs"
assert all(e["prompt_status"] in {"complete", "partial", "inaccessible"} for e in entries)
assert all(e["source_url"].startswith("https://aanshai.vercel.app/skills#") for e in entries)

for pkg, parent in [("claude-video-skills", ".claude/skills"), ("codex-video-skills", ".agents/skills")]:
    base = ROOT / "packages" / pkg / parent
    assert base.is_dir(), f"missing skill root {base}"
    for entry in entries:
        skill = base / entry["new_skill_id"] / "SKILL.md"
        assert skill.is_file(), f"missing {skill}"
        text = skill.read_text()
        assert text.startswith("---\nname: ") and "\ndescription: " in text.split("---", 2)[1], skill
        assert all(section in text for section in ("## When to use", "## Required assets", "## Workflow", "## Technical settings", "## Outputs and checks", "## Example")), skill
        assert f"/{entry['new_skill_id']}" in text
    main = "claude-video" if pkg == "claude-video-skills" else "codex-video"
    assert (base / main / "SKILL.md").is_file(), f"missing router in {pkg}"
    assert (ROOT / "packages" / pkg / "scripts/media.py").is_file()

cats = {c: sum(e["category"] == c for e in entries) for c in data["categories"]}
assert cats == {"Animated videos": 52, "Reel formats": 7, "Motion effects": 7, "Edit styles": 7, "Looks": 7}, cats
for path in [ROOT / "README.md", ROOT / "packages/claude-video-skills/README.md", ROOT / "packages/codex-video-skills/README.md"]:
    assert path.is_file() and path.stat().st_size > 300
assert (ROOT / "LICENSE").is_file()
print(f"PASS: {len(entries)} inventory entries, {len(entries)*2} specialist bundles, two routers, category counts {cats}")
