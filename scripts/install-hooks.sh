#!/usr/bin/env bash
# Point this repo at .githooks (phase-gate pre-commit).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
export PYTHONPATH="${ROOT}/scripts${PYTHONPATH:+:$PYTHONPATH}"

exec python3 "${ROOT}/scripts/install_hooks.py" "$@"
