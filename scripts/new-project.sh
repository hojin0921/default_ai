#!/usr/bin/env bash
# Copy this template into a new project folder, then git init + hooks + gate status.
# Usage:
#   ./scripts/new-project.sh                          # prompts for path
#   ./scripts/new-project.sh /path/to/my-new-project  # non-interactive
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
export PYTHONPATH="${ROOT}/scripts${PYTHONPATH:+:$PYTHONPATH}"
exec python3 "${ROOT}/scripts/new_project.py" "$@"
