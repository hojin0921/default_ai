#!/usr/bin/env python3
"""Local verification for phase gate (gate.sh allowed; direct gate.json shell edits denied)."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from lib.phase_gate import (  # noqa: E402
    DEFAULT_GATE,
    can_commit,
    can_write_code,
    find_repo_root,
    gate_path,
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


def gate_cmd(*args: str) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT / "scripts")
    return subprocess.run(
        ["bash", str(ROOT / "scripts" / "gate.sh"), *args],
        text=True,
        capture_output=True,
        cwd=str(ROOT),
        env=env,
    )


def snapshot_gate(root: Path) -> str | None:
    path = gate_path(root)
    if not path.is_file():
        return None
    return path.read_text(encoding="utf-8")


def restore_gate(root: Path, raw: str | None) -> None:
    path = gate_path(root)
    if raw is None:
        if path.is_file():
            path.unlink()
        return
    path.write_text(raw, encoding="utf-8")


def main() -> None:
    root = find_repo_root(ROOT)
    prior = snapshot_gate(root)
    try:
        _run(root)
    finally:
        restore_gate(root, prior)


def _run(root: Path) -> None:
    save_gate(dict(DEFAULT_GATE), root)
    assert can_write_code(load_gate(root)) and can_commit(load_gate(root))
    print("PASS off")

    g = dict(DEFAULT_GATE)
    g.update(
        {
            "enabled": True,
            "plan_approved": True,
            "design_approved": True,
            "kickoff_step": "done",
            "step": "explore",
            "allow_commit": False,
        }
    )
    save_gate(g, root)
    loaded = load_gate(root)
    assert loaded.get("design_approved") is True
    assert loaded.get("kickoff_step") == "done"
    print("PASS save_gate keeps kickoff fields")

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

    old_stdin = sys.stdin
    try:
        import io
        from contextlib import redirect_stdout
        from io import StringIO

        sys.stdin = io.StringIO(
            json.dumps(
                {
                    "tool_name": "Write",
                    "tool_input": {"path": ".cursor/gate.json"},
                }
            )
        )
        buf = StringIO()
        with redirect_stdout(buf):
            protect_gate_mod.main()
        out = json.loads(buf.getvalue())
    finally:
        sys.stdin = old_stdin
    assert out["permission"] == "deny", out
    print("PASS protect gate file")

    p = gate_cmd("on")
    assert p.returncode == 0, p.stderr
    p = gate_cmd("approve-plan")
    assert p.returncode != 0
    assert "design_approved" in p.stderr
    print("PASS deny approve-plan without design")

    p = gate_cmd("approve-design")
    assert p.returncode == 0, p.stderr
    p = gate_cmd("kickoff", "phase_plan")
    assert p.returncode == 0, p.stderr
    p = gate_cmd("approve-plan")
    assert p.returncode == 0, p.stderr
    g2 = load_gate(root)
    assert g2["plan_approved"] is True
    assert g2["kickoff_step"] == "done"
    assert g2["step"] == "explore"
    print("PASS approve-design then approve-plan")

    tmp = Path(tempfile.mkdtemp())
    (tmp / ".cursor").mkdir()
    legacy = {
        "enabled": True,
        "plan_approved": True,
        "phase": 1,
        "step": "explore",
        "allow_commit": False,
        "note": "legacy",
    }
    (tmp / ".cursor" / "gate.json").write_text(
        json.dumps(legacy), encoding="utf-8"
    )
    lg = load_gate(tmp)
    assert lg["design_approved"] is True
    assert lg["kickoff_step"] == "done"
    print("PASS legacy gate.json infer fields")

    save_gate(dict(DEFAULT_GATE), root)
    assert subprocess.call([str(ROOT / "scripts/phase-gate-check.sh")]) == 0
    g = dict(DEFAULT_GATE)
    g.update({"enabled": True, "allow_commit": False})
    save_gate(g, root)
    assert subprocess.call([str(ROOT / "scripts/phase-gate-check.sh")]) == 1
    g["allow_commit"] = True
    save_gate(g, root)
    assert subprocess.call([str(ROOT / "scripts/phase-gate-check.sh")]) == 0
    print("ALL PASSED")
    print(json.dumps(load_gate(root), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
