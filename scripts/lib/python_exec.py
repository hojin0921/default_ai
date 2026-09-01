#!/usr/bin/env python3
"""Resolve a Python executable argv prefix for cross-platform scripts and hooks."""

from __future__ import annotations

import shutil
import subprocess
import sys
from typing import Sequence


def resolve_python_argv() -> list[str]:
    """Return argv prefix to invoke Python 3 (e.g. ['python3'] or ['py', '-3'])."""
    if getattr(resolve_python_argv, "_cached", None):
        return list(resolve_python_argv._cached)  # type: ignore[attr-defined]

    # Prefer generic commands for hooks.json (portable across machines).
    generic: tuple[list[str], ...] = (
        (["python3"],) if sys.platform != "win32" else (["python"], ["py", "-3"])
    )
    for argv in generic:
        if _python_ok(argv):
            resolve_python_argv._cached = tuple(argv)  # type: ignore[attr-defined]
            return list(argv)

    candidates: tuple[list[str], ...] = (
        [sys.executable],
        ["python3"],
        ["python"],
        ["py", "-3"],
    )
    seen: set[tuple[str, ...]] = set()
    for argv in candidates:
        key = tuple(argv)
        if key in seen:
            continue
        seen.add(key)
        if _python_ok(argv):
            resolve_python_argv._cached = tuple(argv)  # type: ignore[attr-defined]
            return list(argv)

    # Last resort: current interpreter (may still fail on fresh machines).
    resolve_python_argv._cached = (sys.executable,)  # type: ignore[attr-defined]
    return [sys.executable]


def python_command_string() -> str:
    """Single string for hooks.json (e.g. 'python3' or 'py -3')."""
    return " ".join(resolve_python_argv())


def _python_ok(argv: Sequence[str]) -> bool:
    exe = argv[0]
    if not exe:
        return False
    if len(argv) == 1 and not PathLike_exists(exe) and shutil.which(exe) is None:
        return False
    try:
        proc = subprocess.run(
            [*argv, "-c", "import sys; raise SystemExit(0 if sys.version_info >= (3, 8) else 1)"],
            capture_output=True,
            text=True,
            timeout=15,
        )
        return proc.returncode == 0
    except (OSError, subprocess.TimeoutExpired):
        return False


def PathLike_exists(path: str) -> bool:
    from pathlib import Path

    return Path(path).is_file()
