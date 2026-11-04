# Skill coverage report

Validated against the canonical `catalog/skills.json` and `skills/` tree.

| Stage | Count | Validation |
|---|---:|---|
| Catalog entries | 80 | Unique IDs and command names; ID equals command without `/` |
| Canonical skills | 80 / 80 | Valid metadata, required workflow sections, and engine references |
| Claude router | 1 | Metadata, routing guidance, production workflow, and all specialist references |
| Generated platform copies | 160 / 160 | `python3 tools/build_bundles.py --check` |
| Installer full-library test | 3 agent targets | Temporary project installs for Claude Code, Codex, and Antigravity |
| Render integration tests | 2 cases | Transitions, external audio, subtitle track, contact sheet, speed-adjusted source audio |

| Category | Count |
|---|---:|
| Animated videos | 52 |
| Reel formats | 7 |
| Motion effects | 7 |
| Edit styles | 7 |
| Looks | 7 |

Validation confirms structure and routing references. It does not establish that each creative workflow has been rendered or visually approved end to end.
