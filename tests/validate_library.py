#!/usr/bin/env python3
"""Validate canonical catalog, skill metadata, routes, and installed bundle parity."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
catalog = json.loads((ROOT / "catalog/skills.json").read_text(encoding="utf-8"))
entries = catalog["skills"]
assert len(entries) == 80, f"expected 80 specialist workflows, found {len(entries)}"
assert len({item["id"] for item in entries}) == 80
assert len({item["command"] for item in entries}) == 80
assert all(item["id"] == item["command"].removeprefix("/") for item in entries)
counts = {category: sum(item["category"] == category for item in entries) for category in catalog["categories"]}
assert counts == {"Animated videos": 52, "Reel formats": 7, "Motion effects": 7, "Edit styles": 7, "Looks": 7}, counts

def validate_skill(path: Path, expected: str):
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\nname: ([a-z0-9-]+)\ndescription: \"(.+)\"\n---\n", text)
    assert match, f"invalid or missing metadata: {path}"
    assert match.group(1) == expected, f"metadata name mismatch: {path}"
    for section in ("## Purpose", "## When to use", "## Inputs and dependencies", "## Treatment-specific workflow", "## Render workflow", "## Failure handling", "## Example"):
        assert section in text, f"missing {section}: {path}"
    for ref in re.findall(r"`(engine/[^`]+)`", text):
        target = ROOT / ref.split()[0]
        assert target.exists(), f"broken engine reference {ref}: {path}"

for item in entries:
    skill = ROOT / "skills" / item["id"] / "SKILL.md"
    assert skill.is_file(), f"missing canonical skill {skill}"
    validate_skill(skill, item["id"])

router = ROOT / "skills/claude-video/SKILL.md"
router_text = router.read_text(encoding="utf-8")
assert re.match(r"^---\nname: claude-video\ndescription: \".+\"\n---\n", router_text)
for section in ("## Route the request", "## Production process", "## What the local engine does", "## Specialist command directory"):
    assert section in router_text, f"router is missing {section}"
for item in entries:
    assert item["command"] in router_text, f"router does not list {item['command']}"
readme = (ROOT / "README.md").read_text(encoding="utf-8")
readme_commands = re.findall(r"^\| (/[-a-z0-9]+) \|", readme, flags=re.MULTILINE)
assert len(readme_commands) == 80 and set(readme_commands) == {item["command"] for item in entries}, "README specialist command table differs from catalog"
for arg in ("install.sh", "uninstall.sh", "install.ps1", "uninstall.ps1"):
    assert (ROOT / "installers" / arg).is_file(), f"README refers to a missing installer: {arg}"

assert (ROOT / "engine/video.py").is_file()
assert (ROOT / "installers/manage.py").is_file()
assert (ROOT / "README.md").is_file()
print(f"PASS: {len(entries)} canonical skills, router, route references, and categories {counts}")
