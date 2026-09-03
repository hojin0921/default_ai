#!/usr/bin/env python3
"""Install git hooks and configure Cursor hooks for the detected Python."""

from __future__ import annotations

import json
import os
import stat
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from lib.python_exec import python_command_string, resolve_python_argv  # noqa: E402

HOOKS_JSON = ROOT / ".cursor" / "hooks.json"


def _chmod_exec(path: Path) -> None:
    if os.name == "nt":
        return
    try:
        mode = path.stat().st_mode
        path.chmod(mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    except OSError:
        pass


def _update_hooks_json(python_cmd: str) -> None:
    if not HOOKS_JSON.is_file():
        return

    def hook_cmd(name: str) -> str:
        return f"{python_cmd} scripts/cursor_hook.py {name}"

    data = {
        "version": 1,
        "hooks": {
            "sessionStart": [
                {
                    "command": hook_cmd("session_start"),
                    "timeout": 10,
                }
            ],
            "preToolUse": [
                {
                    "command": hook_cmd("protect_gate"),
                    "matcher": "Write|StrReplace|Delete",
                    "failClosed": True,
                    "timeout": 10,
                },
                {
                    "command": hook_cmd("gate_check"),
                    "matcher": "Write|StrReplace|Delete",
                    "failClosed": True,
                    "timeout": 10,
                },
                {
                    "command": hook_cmd("gate_check"),
                    "matcher": "Shell",
                    "failClosed": True,
                    "timeout": 10,
                },
            ],
            "beforeShellExecution": [
                {
                    "command": hook_cmd("gate_check"),
                    "failClosed": True,
                    "timeout": 10,
                }
            ],
        },
    }
    HOOKS_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _update_claude_settings(python_cmd: str) -> None:
    path = ROOT / ".claude" / "settings.json"
    if not path.parent.is_dir():
        return
    handoff_cmd = f"{python_cmd} scripts/handoff_session_context.py --format claude-json"
    data = {
        "hooks": {
            "SessionStart": [
                {
                    "matcher": "startup|clear|fork",
                    "hooks": [
                        {
                            "type": "command",
                            "command": handoff_cmd,
                        }
                    ],
                }
            ]
        }
    }
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    os.chdir(ROOT)
    py_argv = resolve_python_argv()
    python_cmd = python_command_string()

    subprocess.run(["git", "config", "core.hooksPath", ".githooks"], check=True)

    executables = [
        ROOT / ".githooks" / "pre-commit",
        ROOT / "scripts" / "gate.sh",
        ROOT / "scripts" / "phase-gate-check.sh",
        ROOT / "scripts" / "install-hooks.sh",
        ROOT / "scripts" / "new-project.sh",
        ROOT / "scripts" / "_gate_cli.py",
        ROOT / "scripts" / "cursor_hook.py",
        ROOT / "scripts" / "install_hooks.py",
        ROOT / "scripts" / "new_project.py",
        ROOT / ".cursor" / "hooks" / "gate-check.sh",
        ROOT / ".cursor" / "hooks" / "protect-gate.sh",
        ROOT / ".cursor" / "hooks" / "gate_check.py",
        ROOT / ".cursor" / "hooks" / "protect_gate.py",
        ROOT / ".cursor" / "hooks" / "session_start.py",
        ROOT / "scripts" / "handoff_session_context.py",
    ]
    for path in executables:
        if path.is_file():
            _chmod_exec(path)

    _update_hooks_json(python_cmd)
    _update_claude_settings(python_cmd)

    print("Installed: core.hooksPath=.githooks")
    print(f"Python for hooks: {python_cmd}")
    print("Chat handoff: Cursor sessionStart + Claude Code SessionStart (.claude/settings.json)")
    print("Phase gate CLI:")
    if os.name == "nt":
        print(r"  .\scripts\gate.cmd status")
        print(f"  {python_cmd} scripts/_gate_cli.py status")
    else:
        print("  ./scripts/gate.sh status")
    proc = subprocess.run(["git", "config", "--get", "core.hooksPath"], capture_output=True, text=True)
    if proc.stdout.strip():
        print(proc.stdout.strip())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
