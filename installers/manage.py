#!/usr/bin/env python3
"""Install or uninstall canonical Claude Video Skills without replacing user files."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import shutil
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = json.loads((ROOT / "catalog/skills.json").read_text(encoding="utf-8"))
IDS = {entry["id"] for entry in CATALOG["skills"]}


class InstallError(RuntimeError):
    pass


def safe_path(root: Path, relative: Path) -> Path:
    """Reject traversal and symlinked parents before reading or writing a target."""
    if relative.is_absolute() or ".." in relative.parts:
        raise InstallError(f"Unsafe path in installer target: {relative}")
    root = root.resolve()
    target = root / relative
    current = root
    for part in relative.parts[:-1]:
        current = current / part
        if current.is_symlink():
            raise InstallError(f"Refusing to traverse a symbolic link: {current}")
    try:
        target.resolve(strict=False).relative_to(root)
    except ValueError as exc:
        raise InstallError(f"Installer target escapes its root: {target}") from exc
    return target


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def detect_agent(project: Path) -> str:
    env = os.environ
    if any(env.get(key) for key in ("ANTIGRAVITY_HOME", "AGY_HOME", "ANTIGRAVITY")):
        return "antigravity"
    if any(env.get(key) for key in ("CODEX_HOME", "CODEX_CLI")):
        return "codex"
    if any(env.get(key) for key in ("CLAUDE_CODE", "CLAUDE_CODE_SSE_PORT")):
        return "claude"
    has_claude, has_agents = (project / ".claude").is_dir(), (project / ".agents").is_dir()
    if has_claude and has_agents:
        raise InstallError("Both .claude and .agents exist; choose --agent explicitly (Codex and Antigravity share .agents).")
    if has_claude:
        return "claude"
    if has_agents:
        raise InstallError("Both Codex and Antigravity use .agents/skills; choose --agent explicitly unless the host sets a detectable environment variable.")
    raise InstallError("Could not infer the agent. Choose --agent claude, codex, or antigravity.")


def locations(agent: str, scope: str, project: Path, home: Path) -> tuple[Path, Path, Path]:
    if scope == "project":
        root = project
        skill_rel = {
            "claude": Path(".claude/skills"),
            "codex": Path(".agents/skills"),
            "antigravity": Path(".agents/skills"),
        }[agent]
        state_dir = project / ".claude-video"
    else:
        root = home
        skill_rel = {
            "claude": Path(".claude/skills"),
            "codex": Path(".agents/skills"),
            "antigravity": Path(".gemini/config/skills"),
        }[agent]
        state_dir = home / ".claude-video"
    return root / skill_rel, root / ".claude-video/engine", state_dir / f"install-{scope}-{agent}.json"


def load_manifest(path: Path) -> dict:
    if not path.exists():
        return {"files": {}}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise InstallError(f"Existing install manifest is unreadable; preserving it: {path}") from exc
    if not isinstance(value, dict) or not isinstance(value.get("files"), dict):
        raise InstallError(f"Existing install manifest has an unexpected format; preserving it: {path}")
    return value


def sources(skill_ids: list[str], skill_root: Path, engine_root: Path, base_root: Path) -> list[tuple[Path, Path]]:
    pairs = []
    for skill_id in skill_ids:
        source = ROOT / "skills" / skill_id / "SKILL.md"
        if not source.is_file():
            raise InstallError(f"Canonical skill is missing: {source}")
        validate_skill(source, skill_id)
        target = skill_root / skill_id / "SKILL.md"
        safe_path(base_root, target.relative_to(base_root))
        pairs.append((source, target))
    for source in sorted((ROOT / "engine").rglob("*")):
        if source.is_file() and "__pycache__" not in source.parts and source.suffix != ".pyc":
            target = engine_root / source.relative_to(ROOT / "engine")
            safe_path(base_root, target.relative_to(base_root))
            pairs.append((source, target))
    return pairs


def validate_skill(path: Path, expected_name: str) -> None:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n") or "\n---\n" not in text[4:]:
        raise InstallError(f"Invalid skill frontmatter: {path}")
    frontmatter = text[4:].split("\n---\n", 1)[0]
    values = {}
    for line in frontmatter.splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            values[key.strip()] = value.strip().strip('"')
    if values.get("name") != expected_name or not values.get("description"):
        raise InstallError(f"Skill metadata is missing or does not match folder {expected_name}: {path}")


def install(args, agent: str, project: Path, home: Path) -> dict:
    skill_root, engine_root, manifest_path = locations(agent, args.scope, project, home)
    base_root = project if args.scope == "project" else home
    if manifest_path.parent.is_symlink() or manifest_path.is_symlink():
        raise InstallError(f"Refusing to use a symbolic link for installer state: {manifest_path.parent}")
    entries = ["claude-video"] + sorted(IDS) if args.skills is None else [x.strip() for x in args.skills.split(",") if x.strip()]
    if len(set(entries)) != len(entries):
        raise InstallError("The --skills list contains duplicate names.")
    unknown = sorted(set(entries) - IDS - {"claude-video"})
    if unknown:
        raise InstallError("Unknown skill name(s): " + ", ".join(unknown))
    if not entries:
        raise InstallError("Select at least one skill.")
    prior = load_manifest(manifest_path)
    previous_files = prior["files"]
    plan, conflicts = [], []
    for source, target in sources(entries, skill_root, engine_root, base_root):
        expected = digest(source)
        old_hash = previous_files.get(str(target))
        if target.is_symlink():
            raise InstallError(f"Refusing to replace a symbolic link: {target}")
        if target.exists():
            current = digest(target)
            if current == expected:
                action = "already-current"
            elif old_hash and current == old_hash:
                action = "managed-update"
            elif args.upgrade:
                action = "backup-and-update"
            else:
                conflicts.append(str(target))
                continue
        else:
            action = "install"
        plan.append({"source": str(source), "target": str(target), "sha256": expected, "action": action})
    if conflicts:
        sample = "\n".join(f"  - {path}" for path in conflicts[:10])
        more = f"\n  ... and {len(conflicts)-10} more" if len(conflicts) > 10 else ""
        raise InstallError("Existing files differ from the package. Nothing was installed. Review them or rerun with --upgrade to back them up first:\n" + sample + more)
    if args.dry_run:
        return {"status": "dry-run", "agent": agent, "scope": args.scope, "skills": entries, "actions": plan}

    backups = []
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    for item in plan:
        source, target = Path(item["source"]), Path(item["target"])
        target.parent.mkdir(parents=True, exist_ok=True)
        if item["action"] == "already-current":
            continue
        if item["action"] == "backup-and-update":
            backup = manifest_path.parent / "backups" / stamp / (hashlib.sha256(str(target).encode()).hexdigest()[:12] + "-" + target.name)
            backup.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(target, backup)
            backups.append(str(backup))
        before = digest(target) if target.exists() else None
        with tempfile.NamedTemporaryFile(prefix=".video-skills-", dir=target.parent, delete=False) as temp:
            temp_path = Path(temp.name)
            temp.write(source.read_bytes())
        try:
            if before is None:
                try:
                    os.link(temp_path, target)
                except FileExistsError as exc:
                    raise InstallError(f"A file appeared during installation; preserving it: {target}") from exc
            else:
                if digest(target) != before:
                    raise InstallError(f"A file changed during installation; preserving it: {target}")
                os.replace(temp_path, target)
        finally:
            temp_path.unlink(missing_ok=True)

    manifest_files = dict(previous_files)
    for item in plan:
        manifest_files[item["target"]] = item["sha256"]
    manifest = {
        "product": "claude-video-skills", "agent": agent, "scope": args.scope,
        "skills": sorted(set(prior.get("skills", [])) | set(entries)),
        "files": manifest_files, "updated_at": datetime.now(timezone.utc).isoformat(),
    }
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return {
        "status": "installed", "agent": agent, "scope": args.scope, "skills": entries,
        "actions": plan, "backups": backups, "manifest": str(manifest_path), "engine": str(engine_root),
        "dependencies": {
            "python": sys.version.split()[0],
            "ffmpeg": shutil.which("ffmpeg"),
            "ffprobe": shutil.which("ffprobe"),
            "librosa": importlib.util.find_spec("librosa") is not None,
        },
    }


def uninstall(args, agent: str, project: Path, home: Path) -> dict:
    _, _, manifest_path = locations(agent, args.scope, project, home)
    base_root = project if args.scope == "project" else home
    if manifest_path.parent.is_symlink() or manifest_path.is_symlink():
        raise InstallError(f"Refusing to use a symbolic link for installer state: {manifest_path.parent}")
    manifest = load_manifest(manifest_path)
    if not manifest.get("files"):
        raise InstallError(f"No managed {agent} installation found at {manifest_path}")
    other_manifests = []
    for path in manifest_path.parent.glob("install-*.json"):
        if path == manifest_path:
            continue
        try:
            other_manifests.append(json.loads(path.read_text(encoding="utf-8")).get("files", {}))
        except (OSError, json.JSONDecodeError):
            continue
    referenced_elsewhere = set().union(*(set(row) for row in other_manifests)) if other_manifests else set()
    actions = []
    for path_text, expected in manifest["files"].items():
        path = Path(path_text)
        try:
            relative = path.relative_to(base_root)
        except ValueError as exc:
            raise InstallError(f"Installer manifest points outside its installation root; preserving everything: {path}") from exc
        safe_path(base_root, relative)
        skill_root, engine_root, _ = locations(agent, args.scope, project, home)
        if not (path.is_relative_to(skill_root) and path.name == "SKILL.md") and not (path.is_relative_to(engine_root) and path.suffix == ".py"):
            raise InstallError(f"Installer manifest contains an unexpected path; preserving everything: {path}")
        if str(path) in referenced_elsewhere:
            actions.append({"path": str(path), "action": "shared-keep"})
        elif path.is_file() and not path.is_symlink() and digest(path) == expected:
            actions.append({"path": str(path), "action": "remove"})
        elif path.exists() or path.is_symlink():
            actions.append({"path": str(path), "action": "modified-keep"})
        else:
            actions.append({"path": str(path), "action": "already-absent"})
    if args.dry_run:
        return {"status": "dry-run-uninstall", "agent": agent, "scope": args.scope, "actions": actions}
    removed = []
    for item in actions:
        if item["action"] == "remove":
            Path(item["path"]).unlink()
            removed.append(item["path"])
    manifest_path.unlink(missing_ok=True)
    for path in sorted({Path(p).parent for p in manifest["files"]}, key=lambda x: len(x.parts), reverse=True):
        try:
            path.rmdir()
        except OSError:
            pass
    return {"status": "uninstalled", "agent": agent, "scope": args.scope, "removed": removed, "preserved": [x["path"] for x in actions if x["action"] in ("shared-keep", "modified-keep")]}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--agent", choices=["auto", "claude", "codex", "antigravity"], default="auto")
    parser.add_argument("--scope", choices=["project", "user"], default="project")
    parser.add_argument("--project-dir", type=Path, default=Path.cwd())
    parser.add_argument("--skills", help="Comma-separated canonical skill names; default installs the router and all specialists.")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--upgrade", action="store_true", help="Back up differing existing files before replacing them.")
    parser.add_argument("--uninstall", action="store_true")
    args = parser.parse_args(argv)
    try:
        project, home = args.project_dir.expanduser().resolve(), Path.home().resolve()
        if not project.is_dir():
            raise InstallError(f"Project directory does not exist: {project}")
        agent = detect_agent(project) if args.agent == "auto" else args.agent
        result = uninstall(args, agent, project, home) if args.uninstall else install(args, agent, project, home)
        print(json.dumps(result, indent=2))
        return 0
    except InstallError as exc:
        print(f"installer error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
