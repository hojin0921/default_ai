#!/usr/bin/env python3
"""Cursor sessionStart hook: inject chat handoff context into new Composer sessions."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from lib.phase_gate import emit  # noqa: E402
from lib.python_exec import resolve_python_argv  # noqa: E402


def main() -> None:
    py = resolve_python_argv()
    proc = subprocess.run(
        [*py, str(ROOT / "scripts" / "handoff_session_context.py"), "--format", "cursor-json"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        emit({})
        return
    raw = proc.stdout.strip()
    if not raw or raw == "{}":
        emit({})
        return
    emit(json.loads(raw))


if __name__ == "__main__":
    main()
