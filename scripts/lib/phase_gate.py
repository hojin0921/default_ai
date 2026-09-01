#!/usr/bin/env python3
"""Phase gate helpers. .cursor/gate.json is the source of truth (chat choice → gate.sh)."""

from __future__ import annotations

import json
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
    "explore_approved": False,
    "document_approved": False,
    "plan_body_approved": False,
    "phase_has_ui": False,
    "design_spec_approved": False,
    "verify_approved": False,
    "phase": 1,
    "step": "explore",
    "kickoff_step": "done",
    "allow_commit": False,
    "note": "사람 결정으로만 전진. 채팅 선택→Agent가 gate CLI 대행 (macOS/Linux: ./scripts/gate.sh, Windows: .\\scripts\\gate.cmd 또는 python scripts/_gate_cli.py), 또는 사람이 동일 명령 실행. Agent는 이 파일을 직접 수정하지 않는다.",
}

_PHASE_DELIVERY_FLAG_KEYS = (
    "explore_approved",
    "document_approved",
    "plan_body_approved",
    "phase_has_ui",
    "design_spec_approved",
    "verify_approved",
)


def reset_phase_delivery_flags(gate: dict[str, Any]) -> None:
    """Reset per-Phase specialist approval flags (Delivery Phase boundary)."""
    gate["explore_approved"] = False
    gate["document_approved"] = False
    gate["plan_body_approved"] = False
    gate["phase_has_ui"] = False
    gate["design_spec_approved"] = False
    gate["verify_approved"] = False
    gate["allow_commit"] = False


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
    for key in _PHASE_DELIVERY_FLAG_KEYS:
        if key not in data:
            out[key] = False
    return out


def save_gate(data: dict[str, Any], root: Path | None = None) -> None:
    path = gate_path(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    ordered = {
        "enabled": bool(data.get("enabled", False)),
        "plan_approved": bool(data.get("plan_approved", False)),
        "design_approved": bool(data.get("design_approved", False)),
        "explore_approved": bool(data.get("explore_approved", False)),
        "document_approved": bool(data.get("document_approved", False)),
        "plan_body_approved": bool(data.get("plan_body_approved", False)),
        "phase_has_ui": bool(data.get("phase_has_ui", False)),
        "design_spec_approved": bool(data.get("design_spec_approved", False)),
        "verify_approved": bool(data.get("verify_approved", False)),
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
    step = gate.get("step")
    if step not in ("implement", "verify", "review"):
        return False
    if step == "implement":
        if not gate.get("plan_body_approved"):
            return False
        if gate.get("phase_has_ui") and not gate.get("design_spec_approved"):
            return False
    return True


def can_advance_to(gate: dict[str, Any], target_step: str) -> tuple[bool, str]:
    """Return (ok, error_message) for advance <target_step>."""
    current = gate.get("step")

    if target_step == "document":
        if not gate.get("explore_approved"):
            return (
                False,
                "advance document blocked: explore_approved=false. "
                "Launch senior-architect in Explore, then "
                "./scripts/gate.sh approve-explore when the human approves.",
            )
        return True, ""

    if target_step == "plan":
        if not gate.get("document_approved"):
            return (
                False,
                "advance plan blocked: document_approved=false. "
                "Launch senior-architect or senior-pm in Document, then "
                "./scripts/gate.sh approve-document when the human approves.",
            )
        return True, ""

    if target_step == "implement":
        if current in ("explore", "document"):
            return (
                False,
                "advance implement blocked: complete Plan first "
                "(Explore→Document→Plan). Launch senior-pm; if UI, senior-design.",
            )
        if not gate.get("plan_body_approved"):
            return (
                False,
                "advance implement blocked: plan_body_approved=false. "
                "Launch senior-pm in Plan, then ./scripts/gate.sh approve-plan-body "
                "when the human approves the Plan body.",
            )
        if gate.get("phase_has_ui") and not gate.get("design_spec_approved"):
            return (
                False,
                "advance implement blocked: phase_has_ui=true but "
                "design_spec_approved=false. Launch senior-design in Plan, then "
                "./scripts/gate.sh approve-design-spec when the human approves.",
            )
        return True, ""

    if target_step == "verify":
        if current in ("explore", "document", "plan"):
            return (
                False,
                "advance verify blocked: complete Implement first (senior-dev).",
            )
        return True, ""

    if target_step == "review":
        if not gate.get("verify_approved"):
            return (
                False,
                "advance review blocked: verify_approved=false. "
                "Launch senior-qa in Verify (tests + 직접 확인 가이드), then "
                "./scripts/gate.sh approve-verify when the human approves.",
            )
        return True, ""

    if target_step == "human_verify":
        if current not in ("review", "human_verify"):
            return (
                False,
                "advance human_verify blocked: complete Review first "
                "(senior-qa then senior-architect).",
            )
        return True, ""

    return True, ""


def can_advance_to_implement(gate: dict[str, Any]) -> tuple[bool, str]:
    """Backward-compatible alias."""
    return can_advance_to(gate, "implement")


def code_write_block_hint(gate: dict[str, Any]) -> str:
    if not gate.get("plan_approved"):
        return "Whole Phase Plan not approved (approve-plan)."
    step = gate.get("step")
    if step not in ("implement", "verify", "review"):
        return f"step={step}; code only in implement|verify|review."
    if step == "implement" and not gate.get("plan_body_approved"):
        return "plan_body_approved=false; senior-pm Plan + approve-plan-body first."
    if gate.get("phase_has_ui") and not gate.get("design_spec_approved"):
        return "design_spec_approved=false; senior-design spec + approve-design-spec first."
    return ""


def can_commit(gate: dict[str, Any]) -> bool:
    if not gate.get("enabled"):
        return True
    if not gate.get("allow_commit"):
        return False
    if not gate.get("verify_approved"):
        return False
    return True


def extract_tool_path(tool_input: dict[str, Any] | None) -> str | None:
    if not tool_input:
        return None
    for key in ("path", "file_path", "target_file", "filePath"):
        val = tool_input.get(key)
        if isinstance(val, str) and val:
            return val
    return None


def gate_cli_hint() -> str:
    """Human-facing gate CLI examples for error messages."""
    if sys.platform == "win32":
        return r".\scripts\gate.cmd or python scripts/_gate_cli.py"
    return "./scripts/gate.sh or python scripts/_gate_cli.py"


def shell_uses_gate_cli(command: str) -> bool:
    """True when shell invokes the supported gate CLI (not a direct gate.json edit)."""
    c = command.strip()
    if not c:
        return False
    patterns = (
        r"scripts[/\\]gate(?:\.sh|\.cmd|\.ps1)?\b",
        r"scripts[/\\]_gate_cli\.py\b",
        r"scripts[/\\]gate\.py\b",
        r"\bpython(?:3)?\s+[^\s;|&]*[/\\]_gate_cli\.py\b",
    )
    return any(re.search(p, c, re.I) for p in patterns)


def shell_mutates_gate(command: str) -> bool:
    """True when shell rewrites gate.json directly (not via gate CLI)."""
    c = command.strip()
    if not c:
        return False
    if shell_uses_gate_cli(c):
        return False
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
