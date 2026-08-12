#!/usr/bin/env bash
# Shared commit gate check (git pre-commit / manual).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
export PYTHONPATH="${ROOT}/scripts${PYTHONPATH:+:$PYTHONPATH}"

exec python3 "${ROOT}/scripts/_phase_gate_check.py"
