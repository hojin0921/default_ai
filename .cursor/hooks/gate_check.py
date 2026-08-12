#!/usr/bin/env python3
"""Cursor hook: gate code writes, git commit, and gate.sh self-approval."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from lib.phase_gate import (  # noqa: E402
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


def main() -> None:
    payload = read_stdin_json()
    root = find_repo_root(ROOT)
    gate = load_gate(root)

    tool = str(payload.get("tool_name") or payload.get("tool") or "")
    hook_event = str(payload.get("hook_event_name") or "")
    tool_input = payload.get("tool_input") or {}
    if isinstance(tool_input, str):
        try:
            tool_input = json.loads(tool_input)
        except json.JSONDecodeError:
            tool_input = {}

    command = ""
    if isinstance(tool_input, dict):
        command = str(tool_input.get("command") or "")
    if not command:
        command = str(payload.get("command") or "")

    if hook_event == "beforeShellExecution" or (tool == "Shell" and command):
        if shell_mutates_gate(command):
            emit(
                deny(
                    "phase-gate: Agent cannot change the gate via shell. "
                    "Ask the human to run ./scripts/gate.sh …"
                )
            )
            return
        if shell_is_git_commit(command) and not can_commit(gate):
            emit(
                deny(
                    "phase-gate: git commit blocked (allow_commit=false). "
                    "Human: ./scripts/gate.sh allow-commit after Verify/User Test, "
                    "or ./scripts/gate.sh off for Small work."
                )
            )
            return
        if hook_event == "beforeShellExecution":
            emit(allow())
            return

    path = extract_tool_path(tool_input if isinstance(tool_input, dict) else {})
    if path and is_gate_file(path, root):
        emit(
            deny(
                "phase-gate: Agent cannot modify .cursor/gate.json. "
                "Human: ./scripts/gate.sh …"
            )
        )
        return

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
        return

    emit(allow())


if __name__ == "__main__":
    main()
