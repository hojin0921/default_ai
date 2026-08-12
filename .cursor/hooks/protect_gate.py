#!/usr/bin/env python3
"""Cursor hook: block Agent writes to .cursor/gate.json."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from lib.phase_gate import (  # noqa: E402
    allow,
    deny,
    emit,
    extract_tool_path,
    find_repo_root,
    is_gate_file,
    read_stdin_json,
)


def main() -> None:
    payload = read_stdin_json()
    tool_input = payload.get("tool_input") or {}
    if isinstance(tool_input, str):
        try:
            tool_input = json.loads(tool_input)
        except json.JSONDecodeError:
            tool_input = {}

    path = extract_tool_path(tool_input)
    root = find_repo_root(ROOT)

    if path and is_gate_file(path, root):
        emit(
            deny(
                "phase-gate: Agent cannot modify .cursor/gate.json. "
                "Human must run ./scripts/gate.sh (approve-plan|advance|allow-commit|…)."
            )
        )
        return

    emit(allow())


if __name__ == "__main__":
    main()
