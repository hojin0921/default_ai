#!/usr/bin/env python3
"""Cursor hooks entry point (cross-platform). Usage: python scripts/cursor_hook.py <hook_name>"""

from __future__ import annotations

import runpy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VALID_HOOKS = frozenset({"gate_check", "protect_gate"})


def main(argv: list[str]) -> int:
    if len(argv) != 1 or argv[0] not in VALID_HOOKS:
        print(
            f"usage: cursor_hook.py <{'|'.join(sorted(VALID_HOOKS))}>",
            file=sys.stderr,
        )
        return 1
    hook = argv[0]
    script = ROOT / ".cursor" / "hooks" / f"{hook}.py"
    if not script.is_file():
        print(f"missing hook script: {script}", file=sys.stderr)
        return 1
    runpy.run_path(str(script), run_name="__main__")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
