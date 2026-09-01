#!/usr/bin/env python3
"""Cursor hook: gate code writes, git commit, and direct gate.json shell edits."""

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
    code_write_block_hint,
    deny,
    emit,
    extract_tool_path,
    find_repo_root,
    gate_cli_hint,
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
                    "phase-gate: do not edit .cursor/gate.json via shell. "
                    f"After an explicit human chat choice, run {gate_cli_hint()} … "
                    "(or ask the human to run the same command)."
                )
            )
            return
        if shell_is_git_commit(command) and not can_commit(gate):
            hint = ""
            if gate.get("enabled") and gate.get("allow_commit") and not gate.get(
                "verify_approved"
            ):
                hint = " verify_approved=false; run approve-verify before allow-commit."
            elif gate.get("enabled") and not gate.get("allow_commit"):
                hint = " allow_commit=false; pick 통과 in chat (approve-verify + allow-commit)."
            emit(
                deny(
                    "phase-gate: git commit blocked."
                    + hint
                    + f" Or {gate_cli_hint()} off for Small work."
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
                "phase-gate: Agent cannot modify .cursor/gate.json directly. "
                f"After an explicit human chat choice, run {gate_cli_hint()} … "
                "(or human runs the same command)."
            )
        )
        return

    if path and is_code_path(path, root) and not can_write_code(gate):
        hint = code_write_block_hint(gate)
        emit(
            deny(
                "phase-gate: code write blocked.\n"
                f"  enabled={gate.get('enabled')} plan_approved={gate.get('plan_approved')} "
                f"phase={gate.get('phase')} step={gate.get('step')}\n"
                f"  explore_approved={gate.get('explore_approved')} "
                f"document_approved={gate.get('document_approved')} "
                f"plan_body_approved={gate.get('plan_body_approved')} "
                f"phase_has_ui={gate.get('phase_has_ui')} "
                f"design_spec_approved={gate.get('design_spec_approved')} "
                f"verify_approved={gate.get('verify_approved')}\n"
                + (f"  Hint: {hint}\n" if hint else "")
                + "  Each Delivery step needs its specialist + approve-* before advance."
            )
        )
        return

    emit(allow())


if __name__ == "__main__":
    main()
