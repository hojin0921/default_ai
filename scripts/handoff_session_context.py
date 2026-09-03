#!/usr/bin/env python3
"""Emit chat handoff context for session-start hooks (Cursor, Claude Code, plain)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from lib.chat_handoff import read_handoff_for_session  # noqa: E402
from lib.phase_gate import find_repo_root, load_gate  # noqa: E402


def build_context(root: Path | None = None) -> str | None:
    root = root or find_repo_root(ROOT)
    gate = load_gate(root)
    return read_handoff_for_session(root, gate)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Print handoff context for session hooks")
    parser.add_argument(
        "--format",
        choices=("plain", "cursor-json", "claude-json"),
        default="plain",
        help="Output format (default: plain)",
    )
    args = parser.parse_args(argv)

    context = build_context()
    if not context:
        if args.format == "plain":
            return 0
        if args.format == "cursor-json":
            sys.stdout.write("{}")
            return 0
        sys.stdout.write(
            json.dumps(
                {
                    "hookSpecificOutput": {
                        "hookEventName": "SessionStart",
                        "additionalContext": "",
                    }
                },
                ensure_ascii=False,
            )
        )
        return 0

    if args.format == "plain":
        sys.stdout.write(context)
        return 0

    if args.format == "cursor-json":
        sys.stdout.write(json.dumps({"additional_context": context}, ensure_ascii=False))
        return 0

    # claude-json
    sys.stdout.write(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "SessionStart",
                    "additionalContext": context,
                }
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
