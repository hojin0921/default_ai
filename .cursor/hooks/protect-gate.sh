#!/usr/bin/env bash
# preToolUse: block Agent writes/deletes to .cursor/gate.json
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"
export PYTHONPATH="${ROOT}/scripts${PYTHONPATH:+:$PYTHONPATH}"

exec python3 - <<'PY'
import sys
from lib.phase_gate import (
    allow,
    deny,
    emit,
    extract_tool_path,
    find_repo_root,
    is_gate_file,
    read_stdin_json,
)

payload = read_stdin_json()
tool = payload.get("tool_name") or payload.get("tool") or ""
tool_input = payload.get("tool_input") or {}
if isinstance(tool_input, str):
    import json
    try:
        tool_input = json.loads(tool_input)
    except json.JSONDecodeError:
        tool_input = {}

path = extract_tool_path(tool_input)
root = find_repo_root()

# Also catch Delete
if path and is_gate_file(path, root):
    emit(
        deny(
            "phase-gate: Agent cannot modify .cursor/gate.json. "
            "Human must run ./scripts/gate.sh (approve-plan|advance|allow-commit|…)."
        )
    )
    raise SystemExit(0)

emit(allow())
PY
