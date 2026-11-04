#!/usr/bin/env python3
"""Generate platform skill bundles from the canonical skills/ source tree."""
from __future__ import annotations

import argparse
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANONICAL = ROOT / "skills"
TARGETS = {
    ROOT / "packages/claude-video-skills/.claude/skills": "claude-video",
    ROOT / "packages/codex-video-skills/.agents/skills": "claude-video",
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail if generated bundles differ")
    args = parser.parse_args()
    for target, _ in TARGETS.items():
        if args.check:
            actual = {p.parent.name: p.read_bytes() for p in target.glob("*/SKILL.md")} if target.exists() else {}
            expected = {p.parent.name: p.read_bytes() for p in CANONICAL.glob("*/SKILL.md")}
            if actual != expected:
                raise SystemExit(f"Generated skill bundle is stale: {target}; run python3 tools/build_bundles.py")
            continue
        target.mkdir(parents=True, exist_ok=True)
        # Remove only skill folders in these declared generated output directories.
        for child in target.iterdir():
            if child.is_dir() and (child / "SKILL.md").is_file():
                shutil.rmtree(child)
        for source in CANONICAL.iterdir():
            if source.is_dir() and (source / "SKILL.md").is_file():
                shutil.copytree(source, target / source.name)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
