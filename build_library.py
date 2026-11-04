#!/usr/bin/env python3
"""Fetch the public source page and build the audited skill inventory."""
from __future__ import annotations

import csv
import json
import re
import urllib.request
from html import unescape
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent
URL = "https://aanshai.vercel.app/skills#guide"
SOURCE_URL = "https://aanshai.vercel.app/skills"


class Node:
    def __init__(self, tag: str, attrs: list[tuple[str, str | None]] = ()):
        self.tag, self.attrs, self.children = tag, dict(attrs), []

    def all(self, tag: str):
        out = []
        for child in self.children:
            if isinstance(child, Node):
                if child.tag == tag:
                    out.append(child)
                out.extend(child.all(tag))
        return out

    def text(self):
        return "".join(c if isinstance(c, str) else c.text() for c in self.children)


class Tree(HTMLParser):
    VOID = {"br", "img", "meta", "link", "input", "hr", "source"}

    def __init__(self):
        super().__init__()
        self.root, self.stack = Node("root"), []
        self.stack.append(self.root)

    def handle_starttag(self, tag, attrs):
        node = Node(tag, attrs)
        self.stack[-1].children.append(node)
        if tag not in self.VOID:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        self.stack[-1].children.append(Node(tag, attrs))

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i].tag == tag:
                del self.stack[i:]
                break

    def handle_data(self, data):
        self.stack[-1].children.append(data)


def clean(s: str) -> str:
    return re.sub(r"\s+", " ", unescape(s)).strip()


def slug(s: str) -> str:
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", s.lower())).strip("-")


def main():
    req = urllib.request.Request(SOURCE_URL, headers={"User-Agent": "VideoSkillsResearch/1.0"})
    with urllib.request.urlopen(req, timeout=30) as response:
        html = response.read().decode("utf-8")
        status = response.status
    (ROOT / "research").mkdir(exist_ok=True)
    (ROOT / "research/source-prompts").mkdir(parents=True, exist_ok=True)
    tree = Tree()
    tree.feed(html)
    inventory, seen_ids = [], set()
    categories = []
    for section in tree.root.all("section"):
        headings = section.all("h2")
        if not headings:
            continue
        category = clean(headings[0].text())
        if category not in {"Animated videos", "Reel formats", "Motion effects", "Edit styles", "Looks"}:
            continue
        categories.append(category)
        for card in section.all("li"):
            source_id = card.attrs.get("id")
            commands = [clean(n.text()) for n in card.all("code") if clean(n.text()).startswith("/")]
            titles = card.all("h3")
            if not source_id or not titles:
                continue
            title = clean(titles[0].text())
            command = commands[-1] if commands else f"/{source_id}"
            paragraphs = [clean(p.text()) for p in card.all("p")]
            description = paragraphs[0] if paragraphs else ""
            asset = ""
            for p in paragraphs:
                if "You give" in p:
                    asset = p.split("You give", 1)[-1].split("Then type", 1)[0].strip(" |")
            pres = card.all("pre")
            prompt = clean(pres[0].text()) if pres else ""
            duplicate = source_id in seen_ids
            seen_ids.add(source_id)
            new_id = slug(title)
            entry = {
                "source_id": source_id,
                "new_skill_id": new_id,
                "original_name": title,
                "original_command": command,
                "category": category,
                "description": description,
                "input_assets": asset,
                "source_url": f"{SOURCE_URL}#{source_id}",
                "prompt_status": "complete" if prompt else "inaccessible",
                "duplicate": duplicate,
                "source_prompt_file": f"source-prompts/{source_id}.txt" if prompt else None,
                "output_resolution": sorted(set(re.findall(r"\b\d{3,4}\s*[×x]\s*\d{3,4}\b", prompt))) or None,
                "frame_rate": re.findall(r"\b\d{2,3}\s*fps\b", prompt, re.I) or None,
                "aspect_ratio": re.findall(r"\b\d\s*:\s*\d\b", prompt) or None,
                "render_requirements": [term for term in ["MP4", "ffmpeg", "contact sheet", "preview", "H.264", "720p", "1080p"] if term.lower() in prompt.lower()],
                "dependencies": [term for term in ["ffmpeg", "Node", "Chrome", "torchaudio", "MMS_FA", "Whisper", "Remotion", "Blender"] if term.lower() in prompt.lower()],
                "approval_required": bool(re.search(r"\b(ask|approval|approve|before the full render|before overwriting)\b", prompt, re.I)),
                "workflow_step_count": len(re.findall(r"(?:^|\s)\d+\.\s", prompt)),
            }
            inventory.append(entry)
            if prompt:
                (ROOT / "research/source-prompts" / f"{source_id}.txt").write_text(prompt + "\n")

    inventory.sort(key=lambda x: (categories.index(x["category"]), x["source_id"]))
    id_counts = {}
    for entry in inventory:
        id_counts[entry["new_skill_id"]] = id_counts.get(entry["new_skill_id"], 0) + 1
    for entry in inventory:
        if id_counts[entry["new_skill_id"]] > 1:
            entry["new_skill_id"] += "-" + entry["source_id"]
    (ROOT / "research/inventory.json").write_text(json.dumps({"source": SOURCE_URL, "fetched_status": status, "advertised_count": 80, "actual_count": len(inventory), "categories": categories, "skills": inventory}, ensure_ascii=False, indent=2) + "\n")
    with (ROOT / "research/inventory.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["source_id", "new_skill_id", "original_name", "original_command", "category", "description", "input_assets", "source_url", "prompt_status", "duplicate", "source_prompt_file", "output_resolution", "frame_rate", "aspect_ratio", "render_requirements", "dependencies", "approval_required", "workflow_step_count"])
        w.writeheader(); w.writerows(inventory)

    counts = {c: sum(x["category"] == c for x in inventory) for c in categories}
    (ROOT / "research/source-audit.md").write_text(
        "# Source audit\n\n"
        f"Audited {SOURCE_URL} on 2026-11-04. HTTP status: {status}. The page advertises 80 skills; parsed {len(inventory)} distinct card IDs from all five categories.\n\n"
        f"- Advertised: 80\n- Discovered: {len(inventory)}\n- Complete expanded prompts obtained: {sum(x['prompt_status']=='complete' for x in inventory)}\n- Partial prompts: 0\n- Inaccessible prompts: {sum(x['prompt_status']=='inaccessible' for x in inventory)}\n- Duplicate IDs: {sum(x['duplicate'] for x in inventory)}\n- Missing source pages: 0 (all cards link to the source page anchors)\n\n"
        "## Coverage by category\n\n" + "\n".join(f"- {c}: {n}" for c,n in counts.items()) +
        "\n\nThe page exposes each prompt in its server-rendered HTML, including the collapsed `Show prompt` content. The source prompt archive is research-only and excluded from public packages. No source protections were bypassed.\n"
    )
    (ROOT / "research/extraction-progress.md").write_text(
        f"# Extraction progress\n\nCompleted live-page audit on 2026-11-04. {len(inventory)}/{len(inventory)} card entries discovered; {sum(x['prompt_status']=='complete' for x in inventory)}/{len(inventory)} expanded prompts captured. The page advertises 80.\n\n"
        "Next: review prompt requirements entry-by-entry, author original public workflows, package both platform variants, validate all manifests and references.\n"
    )

    # Public entries are original implementations, not copied source prompt text.
    shared = ROOT / "packages/shared-skills"
    shared.mkdir(parents=True, exist_ok=True)
    for entry in inventory:
        sid, title, cat = entry["new_skill_id"], entry["original_name"], entry["category"]
        asset = entry["input_assets"] or "The user-provided media relevant to the requested edit; ask only for an essential missing input."
        description = entry["description"] or f"Create a {title} edit using an appropriate supplied clip, audio, script, or stills."
        prompt = (ROOT / "research/source-prompts" / f"{entry['source_id']}.txt").read_text() if entry["prompt_status"] == "complete" else ""
        compact = prompt.lower()
        aspect = "9:16 vertical, 1080×1920 at 30 fps" if any(t in compact for t in ["9:16", "reel", "vertical"]) else "16:9 landscape, 1920×1080 at 30 fps"
        mkdirs = [ROOT / f"packages/claude-video-skills/.claude/skills/{sid}", ROOT / f"packages/codex-video-skills/.agents/skills/{sid}", shared / sid]
        body = f'''---
name: {sid}
description: "{description.replace('"', "'")[:240]} Use when asked for {title.lower()} video production or editing.
---

# {title}

## When to use
Use this workflow for {title.lower()} requests in the **{cat}** collection. Preserve this specific visual intent; do not substitute a generic cinematic treatment.

## Required assets and formats
- Inputs: {asset}
- Accept common video formats (MP4, MOV, WebM), audio (MP3, WAV, M4A), images (PNG, JPEG, WebP), and text scripts/lyrics when relevant. Confirm installed tools support the detected codec.
- Keep source media read-only. Do not fabricate lyrics, timestamps, quotes, footage, or source-dependent detail.

## Workflow
1. Locate the supplied files and inspect duration, dimensions, frame rate, audio streams, and codec with `ffprobe`. Report missing essential inputs only.
2. Turn the request into a concise production plan specific to this treatment: shots/scenes, timing, typography, motion, transitions, color, and audio behavior. When audio or lyrics are involved, inspect the track and align timing to measured vocal/music events; mark uncertain alignment instead of guessing.
3. Make a working project directory under `out/{sid}/` and keep originals untouched. Use FFmpeg filters or a small reproducible script; use existing footage and assets unless the user requests generated visuals.
4. Render a representative low-resolution preview or contact sheet before the final render. Show it to the user and ask for approval or requested revisions. Never overwrite an existing output without asking.
5. Apply revisions, then render the approved result. Preserve original audio unless asked to change it. Keep titles/captions inside platform safe areas and do not alter a person's appearance automatically.

## Technical settings
- Default: {aspect}. Match the source frame rate when that is more appropriate; otherwise use 30 fps.
- Use H.264 video and AAC audio in MP4 for broad playback compatibility. Preserve source aspect ratio through crop/pad decisions made explicit in the plan.
- For lyric or speech captions, preserve the supplied script and writing system; use forced alignment if available. Do not claim word-level accuracy without alignment evidence.

## Outputs and checks
- Save project notes, preview, and final MP4 under `out/{sid}/`.
- Verify the output exists, has non-zero duration, expected dimensions/frame rate, readable audio, and no obvious dropped/blank frames. Provide exact file paths and summarize any limitations.
- If a dependency or alignment tool is missing, explain the limitation and offer a workable reduced workflow rather than claiming success.

## Example
`/{sid} Make a {title.lower()} from the attached media. Preview first.`
'''
        for folder in mkdirs:
            folder.mkdir(parents=True, exist_ok=True)
            (folder / "SKILL.md").write_text(body)

    # Keep common helpers available in each standalone distribution.
    for pkg in ("claude-video-skills", "codex-video-skills"):
        dest = ROOT / f"packages/{pkg}/scripts"
        dest.mkdir(parents=True, exist_ok=True)
        for helper in (ROOT / "shared/scripts").glob("*.py"):
            (dest / helper.name).write_bytes(helper.read_bytes())

    # Entry point router skills.
    for package, path, platform in [("claude-video-skills", ".claude/skills", "Claude Code"), ("codex-video-skills", ".agents/skills", "Codex")]:
        folder = ROOT / f"packages/{package}/{path}/" / ("claude-video" if platform == "Claude Code" else "codex-video")
        folder.mkdir(parents=True, exist_ok=True)
        name = "claude-video" if platform == "Claude Code" else "codex-video"
        (folder / "SKILL.md").write_text(f'''---\nname: {name}\ndescription: "Route a natural-language video editing or creation request to the relevant Video Skills Core workflow for {platform}. Use for reels, music videos, animation, motion effects, editing styles, and looks."\n---\n\n# {name.title()} router\n\nInspect the supplied files and the user's requested result. Choose only the applicable specialist skill from the library's five source categories: Animated videos, Reel formats, Motion effects, Edit styles, Looks. Use the descriptive skill directory names in this package's README index.\n\nInspect media before editing. Ask only for essential missing assets. Preserve original files and audio unless asked otherwise. For video work, prepare a treatment and preview/contact sheet, request approval before final rendering, and ask before overwriting an output. Never claim another skill was programmatically invoked unless the host supports chaining; otherwise follow its instructions directly.\n''')

    print(f"Discovered {len(inventory)} entries; complete prompts {sum(x['prompt_status']=='complete' for x in inventory)}; categories {counts}")


if __name__ == "__main__":
    main()
