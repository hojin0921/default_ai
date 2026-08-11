#!/usr/bin/env bash
# preToolUse (Write/StrReplace/Delete) + beforeShellExecution gate checks
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"
export PYTHONPATH="${ROOT}/scripts${PYTHONPATH:+:$PYTHONPATH}"

exec python3 - <<'PY'
import json
import sys
from lib.phase_gate import (
    allow,
    can_commit,
    can_write_code,
    deny,
    emit,
    extract_tool_path,
    find_repo_root,
    is_code_path,
    is_gate_file,
    load_gate,
    read_stdin_json,
    shell_is_git_commit,
    shell_mutates_gate,
)

payload = read_stdin_json()
root = find_repo_root()
gate = load_gate(root)

tool = str(payload.get("tool_name") or payload.get("tool") or "")
hook_event = str(payload.get("hook_event_name") or "")
tool_input = payload.get("tool_input") or {}
if isinstance(tool_input, str):
    try:
        tool_input = json.loads(tool_input)
    except json.JSONDecodeError:
        tool_input = {}

# Shell command may be at top-level for beforeShellExecution
command = ""
if isinstance(tool_input, dict):
    command = str(tool_input.get("command") or "")
if not command:
    command = str(payload.get("command") or "")

# --- shell gates ---
if hook_event == "beforeShellExecution" or (tool == "Shell" and command):
    if shell_mutates_gate(command):
        emit(
            deny(
                "phase-gate: Agent cannot change the gate via shell. "
                "Ask the human to run ./scripts/gate.sh …"
            )
        )
        raise SystemExit(0)
    if shell_is_git_commit(command) and not can_commit(gate):
        emit(
            deny(
                "phase-gate: git commit blocked (allow_commit=false). "
                "Human: ./scripts/gate.sh allow-commit after Verify/User Test, "
                "or ./scripts/gate.sh off for Small work."
            )
        )
        raise SystemExit(0)
    # beforeShellExecution done
    if hook_event == "beforeShellExecution":
        emit(allow())
        raise SystemExit(0)

# --- file write gates ---
path = extract_tool_path(tool_input if isinstance(tool_input, dict) else {})
if path and is_gate_file(path, root):
    emit(
        deny(
            "phase-gate: Agent cannot modify .cursor/gate.json. "
            "Human: ./scripts/gate.sh …"
        )
    )
    raise SystemExit(0)

if path and is_code_path(path, root) and not can_write_code(gate):
    emit(
        deny(
            "phase-gate: code write blocked.\n"
            f"  enabled={gate.get('enabled')} plan_approved={gate.get('plan_approved')} "
            f"phase={gate.get('phase')} step={gate.get('step')}\n"
            "  Need: plan_approved=true and step in implement|verify|review.\n"
            "  Human: ./scripts/gate.sh approve-plan && ./scripts/gate.sh advance implement"
        )
    )
    raise SystemExit(0)

emit(allow())
PY
