#!/usr/bin/env python3
"""Phase gate helpers. .cursor/gate.json is the source of truth (chat choice → gate.sh)."""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path
from typing import Any

VALID_STEPS = (
    "explore",
    "document",
    "plan",
    "implement",
    "verify",
    "review",
    "human_verify",
)

VALID_KICKOFF_STEPS = (
    "discover",
    "design",
    "docs",
    "phase_plan",
    "done",
)

# Relative path prefixes treated as application code (blocked before implement).
CODE_PREFIXES = (
    "src/",
    "apps/",
    "packages/",
    "lib/",
    "app/",
    "backend/",
    "frontend/",
    "server/",
    "client/",
    "web/",
    "tests/",
    "test/",
    "__tests__/",
)

GATE_REL = ".cursor/gate.json"

DEFAULT_GATE: dict[str, Any] = {
    "enabled": False,
    "plan_approved": False,
    "design_approved": False,
    "phase": 1,
    "step": "explore",
    "kickoff_step": "done",
    "allow_commit": False,
    "note": "사람 결정으로만 전진. 채널: 채팅 선택→Agent가 ./scripts/gate.sh 대행, 또는 사람이 동일 명령 실행. Agent는 이 파일을 직접 수정하지 않는다.",
}


def find_repo_root(start: Path | None = None) -> Path:
    cur = (start or Path.cwd()).resolve()
    for p in [cur, *cur.parents]:
        if (p / ".cursor").is_dir() or (p / ".git").exists():
            return p
    return cur


def gate_path(root: Path | None = None) -> Path:
    return (root or find_repo_root()) / GATE_REL


def load_gate(root: Path | None = None) -> dict[str, Any]:
    path = gate_path(root)
    if not path.is_file():
        return dict(DEFAULT_GATE)
    with path.open(encoding="utf-8") as f:
        data = json.load(f)
    out = dict(DEFAULT_GATE)
    out.update(data)
    if "kickoff_step" not in data:
        out["kickoff_step"] = "done" if data.get("plan_approved") else "discover"
    if "design_approved" not in data:
        out["design_approved"] = bool(data.get("plan_approved"))
    return out


def save_gate(data: dict[str, Any], root: Path | None = None) -> None:
    path = gate_path(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    # Keep stable key order
    ordered = {
        "enabled": bool(data.get("enabled", False)),
        "plan_approved": bool(data.get("plan_approved", False)),
        "design_approved": bool(data.get("design_approved", False)),
        "phase": int(data.get("phase", 1)),
        "step": str(data.get("step", "explore")),
        "kickoff_step": str(data.get("kickoff_step", "done")),
        "allow_commit": bool(data.get("allow_commit", False)),
        "note": data.get("note", DEFAULT_GATE["note"]),
    }
    if ordered["step"] not in VALID_STEPS:
        raise SystemExit(f"invalid step: {ordered['step']}. valid: {', '.join(VALID_STEPS)}")
    if ordered["kickoff_step"] not in VALID_KICKOFF_STEPS:
        raise SystemExit(
            f"invalid kickoff_step: {ordered['kickoff_step']}. "
            f"valid: {', '.join(VALID_KICKOFF_STEPS)}"
        )
    with path.open("w", encoding="utf-8") as f:
        json.dump(ordered, f, ensure_ascii=False, indent=2)
        f.write("\n")


def normalize_rel(path: str, root: Path | None = None) -> str:
    root = root or find_repo_root()
    p = Path(path)
    if p.is_absolute():
        try:
            rel = p.resolve().relative_to(root.resolve())
        except ValueError:
            text = path.replace("\\", "/")
            return text[2:] if text.startswith("./") else text
        return str(rel).replace("\\", "/")
    text = path.replace("\\", "/")
    return text[2:] if text.startswith("./") else text


def is_gate_file(path: str, root: Path | None = None) -> bool:
    return normalize_rel(path, root) == GATE_REL


def is_code_path(path: str, root: Path | None = None) -> bool:
    rel = normalize_rel(path, root)
    if rel in ("src", "apps", "packages", "lib", "app"):
        return True
    return any(rel == p.rstrip("/") or rel.startswith(p) for p in CODE_PREFIXES)


def can_write_code(gate: dict[str, Any]) -> bool:
    if not gate.get("enabled"):
        return True
    if not gate.get("plan_approved"):
        return False
    return gate.get("step") in ("implement", "verify", "review")


def can_commit(gate: dict[str, Any]) -> bool:
    if not gate.get("enabled"):
        return True
    return bool(gate.get("allow_commit"))


def extract_tool_path(tool_input: dict[str, Any] | None) -> str | None:
    if not tool_input:
        return None
    for key in ("path", "file_path", "target_file", "filePath"):
        val = tool_input.get(key)
        if isinstance(val, str) and val:
            return val
    return None


def shell_mutates_gate(command: str) -> bool:
    """True when shell rewrites gate.json directly (not via ./scripts/gate.sh)."""
    c = command.strip()
    if not c:
        return False
    # ./scripts/gate.sh is the approved channel (human chat choice → Agent CLI).
    if re.search(r"gate\.json", c):
        if re.search(
            r"(>|>>)\s*\S*gate\.json|tee\s+\S*gate\.json|"
            r"\b(cp|mv|rm|sed|perl)\b.*gate\.json",
            c,
            re.I,
        ):
            return True
    return False


def shell_is_git_commit(command: str) -> bool:
    # Match git commit but not git commit-tree documentation greps lightly
    return bool(
        re.search(r"(?:^|[;&|]\s*)git(?:\s+-C\s+\S+)?\s+commit\b", command)
    )


def deny(msg: str) -> dict[str, str]:
    return {
        "permission": "deny",
        "user_message": msg,
        "agent_message": msg,
    }


def allow() -> dict[str, str]:
    return {"permission": "allow"}


def emit(obj: dict[str, Any]) -> None:
    sys.stdout.write(json.dumps(obj, ensure_ascii=False))
    sys.stdout.flush()


def read_stdin_json() -> dict[str, Any]:
    raw = sys.stdin.read()
    if not raw.strip():
        return {}
    return json.loads(raw)
