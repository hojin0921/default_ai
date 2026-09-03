#!/usr/bin/env python3
"""Local verification for phase gate (gate CLI allowed; direct gate.json shell edits denied)."""

from __future__ import annotations

import io
import json
import os
import subprocess
import sys
import tempfile
from contextlib import redirect_stdout
from io import StringIO
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
    shell_uses_gate_cli,
)
from lib.python_exec import resolve_python_argv  # noqa: E402


def hook(name: str, payload: dict) -> dict:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT / "scripts")
    py = resolve_python_argv()
    p = subprocess.run(
        [*py, str(ROOT / "scripts" / "cursor_hook.py"), name],
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
    py = resolve_python_argv()
    return subprocess.run(
        [*py, str(ROOT / "scripts" / "_gate_cli.py"), *args],
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
        "gate_check",
        {
            "hook_event_name": "preToolUse",
            "tool_name": "Write",
            "tool_input": {"path": "src/x.ts"},
        },
    )
    assert out["permission"] == "deny", out
    print("PASS deny explore write")

    g["step"] = "implement"
    g["plan_body_approved"] = True
    save_gate(g, root)
    out = hook(
        "gate_check",
        {
            "hook_event_name": "preToolUse",
            "tool_name": "Write",
            "tool_input": {"path": "src/x.ts"},
        },
    )
    assert out["permission"] == "allow", out
    print("PASS allow implement write")

    out = hook(
        "gate_check",
        {
            "hook_event_name": "beforeShellExecution",
            "tool_input": {"command": "git commit -m t"},
        },
    )
    assert out["permission"] == "deny", out
    print("PASS deny commit")

    for cmd in (
        "./scripts/gate.sh approve-plan",
        "python scripts/_gate_cli.py approve-plan",
        r".\scripts\gate.cmd approve-plan",
    ):
        out = hook(
            "gate_check",
            {"hook_event_name": "beforeShellExecution", "tool_input": {"command": cmd}},
        )
        assert out["permission"] == "allow", (cmd, out)
    print("PASS allow gate CLI approve-plan")

    out = hook(
        "gate_check",
        {
            "hook_event_name": "beforeShellExecution",
            "tool_input": {"command": "echo x > .cursor/gate.json"},
        },
    )
    assert out["permission"] == "deny", out
    print("PASS deny direct gate.json redirect")

    assert shell_uses_gate_cli("python scripts/_gate_cli.py status")
    assert shell_uses_gate_cli(r".\scripts\gate.cmd status")
    print("PASS shell_uses_gate_cli")

    sys.path.insert(0, str(ROOT / ".cursor" / "hooks"))
    import protect_gate as protect_gate_mod  # noqa: E402

    old_stdin = sys.stdin
    try:
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

    g_open = load_gate(root)
    g_open["allow_commit"] = True
    g_open["phase"] = 1
    g_open["step"] = "review"
    save_gate(g_open, root)
    p = gate_cmd("next-phase")
    assert p.returncode == 0, p.stderr
    after_next = load_gate(root)
    assert after_next["phase"] == 2
    assert after_next["step"] == "explore"
    assert after_next["allow_commit"] is True
    print("PASS next-phase keeps allow_commit")

    g_closed = load_gate(root)
    g_closed["allow_commit"] = False
    g_closed["phase"] = 2
    g_closed["step"] = "review"
    save_gate(g_closed, root)
    p = gate_cmd("next-phase")
    assert p.returncode == 0, p.stderr
    after_closed = load_gate(root)
    assert after_closed["phase"] == 3
    assert after_closed["allow_commit"] is False
    print("PASS next-phase does not force-open commit")

    handoff_file = root / ".cursor" / "handoff.md"
    assert handoff_file.is_file(), "next-phase should write .cursor/handoff.md"
    text = handoff_file.read_text(encoding="utf-8")
    assert "Phase 3" in text and "Explore" in text
    assert "cursor://anysphere.cursor-deeplink/prompt" in text
    p_url = gate_cmd("handoff-url")
    assert p_url.returncode == 0, p_url.stderr
    assert p_url.stdout.strip().startswith("cursor://")
    print("PASS handoff.md and handoff-url")

    ss = hook("session_start", {"session_id": "test", "is_background_agent": False})
    assert "additional_context" in ss
    assert "handoff" in ss["additional_context"].lower() or "Phase" in ss["additional_context"]
    print("PASS session_start hook injects context")

    p_claude = subprocess.run(
        [*resolve_python_argv(), str(ROOT / "scripts" / "handoff_session_context.py"), "--format", "claude-json"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        env={**os.environ, "PYTHONPATH": str(ROOT / "scripts")},
    )
    assert p_claude.returncode == 0, p_claude.stderr
    cj = json.loads(p_claude.stdout)
    assert cj["hookSpecificOutput"]["hookEventName"] == "SessionStart"
    print("PASS claude-json handoff context")

    g_open2 = load_gate(root)
    g_open2["allow_commit"] = True
    g_open2["explore_approved"] = True
    save_gate(g_open2, root)
    p = gate_cmd("advance", "document")
    assert p.returncode == 0, p.stderr
    assert load_gate(root)["allow_commit"] is True
    print("PASS advance document keeps allow_commit")

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
    (tmp / ".cursor" / "gate.json").write_text(json.dumps(legacy), encoding="utf-8")
    lg = load_gate(tmp)
    assert lg["design_approved"] is True
    assert lg["kickoff_step"] == "done"
    print("PASS legacy gate.json infer fields")

    py = resolve_python_argv()
    save_gate(dict(DEFAULT_GATE), root)
    assert (
        subprocess.call([*py, str(ROOT / "scripts" / "_phase_gate_check.py")], cwd=str(ROOT))
        == 0
    )
    g = dict(DEFAULT_GATE)
    g.update({"enabled": True, "allow_commit": False})
    save_gate(g, root)
    assert (
        subprocess.call([*py, str(ROOT / "scripts" / "_phase_gate_check.py")], cwd=str(ROOT))
        == 1
    )
    g["allow_commit"] = True
    g["verify_approved"] = True
    save_gate(g, root)
    assert (
        subprocess.call([*py, str(ROOT / "scripts" / "_phase_gate_check.py")], cwd=str(ROOT))
        == 0
    )
    print("ALL PASSED")
    print(json.dumps(load_gate(root), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
