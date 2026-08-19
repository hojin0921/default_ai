#!/usr/bin/env python3
"""Local verification for phase gate (gate.sh allowed; direct gate.json shell edits denied)."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from lib.phase_gate import (  # noqa: E402
    DEFAULT_GATE,
    can_commit,
    can_write_code,
    find_repo_root,
    load_gate,
    save_gate,
)


def hook(script: str, payload: dict) -> dict:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT / "scripts")
    p = subprocess.run(
        ["bash", script],
        input=json.dumps(payload),
        text=True,
        capture_output=True,
        cwd=str(ROOT),
        env=env,
    )
    if p.returncode != 0:
        raise SystemExit(f"hook failed: {p.stderr}\n{p.stdout}")
    return json.loads(p.stdout)


def main() -> None:
    root = find_repo_root(ROOT)
    save_gate(dict(DEFAULT_GATE), root)
    assert can_write_code(load_gate(root)) and can_commit(load_gate(root))
    print("PASS off")

    g = dict(DEFAULT_GATE)
    g.update(
        {
            "enabled": True,
            "plan_approved": True,
            "step": "explore",
            "allow_commit": False,
        }
    )
    save_gate(g, root)
    out = hook(
        ".cursor/hooks/gate-check.sh",
        {
            "hook_event_name": "preToolUse",
            "tool_name": "Write",
            "tool_input": {"path": "src/x.ts"},
        },
    )
    assert out["permission"] == "deny", out
    print("PASS deny explore write")

    g["step"] = "implement"
    save_gate(g, root)
    out = hook(
        ".cursor/hooks/gate-check.sh",
        {
            "hook_event_name": "preToolUse",
            "tool_name": "Write",
            "tool_input": {"path": "src/x.ts"},
        },
    )
    assert out["permission"] == "allow", out
    print("PASS allow implement write")

    out = hook(
        ".cursor/hooks/gate-check.sh",
        {
            "hook_event_name": "beforeShellExecution",
            "tool_input": {"command": "git commit -m t"},
        },
    )
    assert out["permission"] == "deny", out
    print("PASS deny commit")

    # ./scripts/gate.sh is allowed after human chat choice; direct gate.json edits denied.
    cmd = "./scripts/" + "gate" + ".sh " + "approve" + "-plan"
    out = hook(
        ".cursor/hooks/gate-check.sh",
        {"hook_event_name": "beforeShellExecution", "tool_input": {"command": cmd}},
    )
    assert out["permission"] == "allow", out
    print("PASS allow gate.sh approve-plan")

    out = hook(
        ".cursor/hooks/gate-check.sh",
        {
            "hook_event_name": "beforeShellExecution",
            "tool_input": {"command": "echo x > .cursor/gate.json"},
        },
    )
    assert out["permission"] == "deny", out
    print("PASS deny direct gate.json redirect")

    sys.path.insert(0, str(ROOT / ".cursor" / "hooks"))
    import protect_gate as protect_gate_mod  # noqa: E402

    # Exercise protect_gate module with stdin simulation
    old_stdin = sys.stdin
    try:
        import io

        sys.stdin = io.StringIO(
            json.dumps(
                {
                    "tool_name": "Write",
                    "tool_input": {"path": ".cursor/gate.json"},
                }
            )
        )
        from io import StringIO
        from contextlib import redirect_stdout

        buf = StringIO()
        with redirect_stdout(buf):
            protect_gate_mod.main()
        out = json.loads(buf.getvalue())
    finally:
        sys.stdin = old_stdin
    assert out["permission"] == "deny", out
    print("PASS protect gate file")

    save_gate(dict(DEFAULT_GATE), root)
    assert subprocess.call([str(ROOT / "scripts/phase-gate-check.sh")]) == 0
    g = dict(DEFAULT_GATE)
    g.update({"enabled": True, "allow_commit": False})
    save_gate(g, root)
    assert subprocess.call([str(ROOT / "scripts/phase-gate-check.sh")]) == 1
    g["allow_commit"] = True
    save_gate(g, root)
    assert subprocess.call([str(ROOT / "scripts/phase-gate-check.sh")]) == 0
    save_gate(dict(DEFAULT_GATE), root)
    print("ALL PASSED")
    print(json.dumps(load_gate(root), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
