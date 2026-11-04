# Coverage report

Based on `research/inventory.json` generated from the live source audit (2026-11-04).

| Stage | Count | Evidence |
|---|---:|---|
| Discovered | 80 / 80 advertised | 80 unique source card IDs |
| Extracted | 80 / 80 | All expanded prompts were available in server-rendered HTML and archived locally |
| Analyzed | 80 / 80 screened | Inventory includes available input cues, prompt status, steps, dimensions/rates/aspect, render keywords, dependency keywords, and approval signals |
| Retained | 0 | Public workflows use independently authored, portable instructions |
| Improved / re-engineered | 80 / 80 packaged workflows | Public workflows normalize asset checks, preview approval, output safety, render defaults, and failure reporting while preserving each title/category/description |
| Packaged | 80 / 80 in each distribution | 160 specialist manifests plus two router skills |
| Tested | 80 metadata/workflow manifests | `python3 tests/validate_library.py`; utility smoke test details in `test-results.md` |

## Source category counts

| Source category | Discovered | Packaged per platform |
|---|---:|---:|
| Animated videos | 52 | 52 |
| Reel formats | 7 | 7 |
| Motion effects | 7 | 7 |
| Edit styles | 7 | 7 |
| Looks | 7 | 7 |

“Analyzed” here means structured screening and metadata extraction of each expanded prompt, not human editorial sign-off on every visual treatment. Full prompt text is held in `research/source-prompts/` locally and excluded from Git because redistribution permission was not established.
