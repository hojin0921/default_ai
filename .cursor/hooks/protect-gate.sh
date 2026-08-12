#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
export PYTHONPATH="$(cd "${SCRIPT_DIR}/../.." && pwd)/scripts${PYTHONPATH:+:$PYTHONPATH}"
exec python3 "${SCRIPT_DIR}/protect_gate.py"
