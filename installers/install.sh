#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(dirname -- "$0")"
python3 "$SCRIPT_DIR/manage.py" "$@"
