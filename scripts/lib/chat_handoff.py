#!/usr/bin/env python3
"""Chat handoff: gate snapshot + continuation prompt for a fresh Composer session."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import quote

HANDOFF_REL = ".cursor/handoff.md"

_STEP_LABELS = {
    "explore": "Explore",
    "document": "Document",
    "plan": "Plan",
    "implement": "Implement",
    "verify": "Verify",
    "review": "Review",
    "human_verify": "Human Verify",
}


def handoff_path(root: Path) -> Path:
    return root / HANDOFF_REL


def find_phase_plan(root: Path) -> str | None:
    """Newest non-template Phase Plan under .cursor/plans/."""
    plans_dir = root / ".cursor" / "plans"
    if not plans_dir.is_dir():
        return None
    candidates: list[Path] = []
    for path in plans_dir.glob("*.md"):
        name = path.name
        if name.startswith("_"):
            continue
        if name.endswith("-design.md"):
            continue
        candidates.append(path)
    if not candidates:
        return None
    candidates.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    rel = candidates[0].relative_to(root)
    return str(rel).replace("\\", "/")


def default_read_paths(root: Path, plan_rel: str | None) -> list[str]:
    paths = [".cursor/gate.json", HANDOFF_REL]
    if plan_rel:
        paths.insert(1, plan_rel)
    for doc in ("docs/product.md", "docs/architecture.md"):
        if (root / doc).is_file():
            paths.append(doc)
    return paths


def build_start_prompt(gate: dict[str, Any], plan_rel: str | None) -> str:
    phase = int(gate.get("phase") or 1)
    step = str(gate.get("step") or "explore")
    step_label = _STEP_LABELS.get(step, step)
    lines = [
        f"Phase {phase} {step_label}부터 delivery-phase Skill대로 진행해줘.",
        "- `.cursor/gate.json`과 Phase Plan·관련 docs만 읽어. 이전 채팅 기록은 없다고 가정.",
        "- Explore→Document→Plan→Implement→Verify→Review 6단계·게이트·전문 에이전트 규칙을 지켜.",
    ]
    if plan_rel:
        lines.append(f"- Phase Plan: `{plan_rel}`")
    return "\n".join(lines)


def build_deeplink(prompt: str) -> str:
    encoded = quote(prompt, safe="")
    return f"cursor://anysphere.cursor-deeplink/prompt?text={encoded}"


def build_web_deeplink(prompt: str) -> str:
    encoded = quote(prompt, safe="")
    return f"https://cursor.com/link/prompt?text={encoded}"


def _gate_snapshot_lines(gate: dict[str, Any]) -> list[str]:
    phase = int(gate.get("phase") or 1)
    step = str(gate.get("step") or "explore")
    return [
        f"- Phase: **{phase}**",
        f"- Step: **{step}** (`{_STEP_LABELS.get(step, step)}`)",
        f"- enabled: {gate.get('enabled')}",
        f"- plan_approved: {gate.get('plan_approved')}",
        f"- allow_commit: {gate.get('allow_commit')}",
    ]


def render_handoff_markdown(
    root: Path,
    gate: dict[str, Any],
    *,
    plan_rel: str | None,
    reason: str,
    prev_phase: int | None = None,
) -> str:
    read_paths = default_read_paths(root, plan_rel)
    start_prompt = build_start_prompt(gate, plan_rel)
    deeplink = build_deeplink(start_prompt)
    web_link = build_web_deeplink(start_prompt)
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    reason_line = {
        "next_phase": f"Phase {prev_phase} Human Verify 통과 후 `next-phase`",
        "approve_plan": "킥오프 K4 Plan 승인 후 `approve-plan`",
        "manual": "`handoff` 명령으로 재생성",
    }.get(reason, reason)

    read_block = "\n".join(f"- `{p}`" for p in read_paths)

    return f"""# Chat handoff

> {reason_line}. **새 Agent/Chat 세션**을 연 뒤 아래 **Start prompt**를 보내거나, 도구별 handoff(§0-5)를 따르세요.  
> **Cursor** · **Claude Code**: `sessionStart` / `SessionStart` 훅이 요약을 주입합니다. **Codex / Antigravity**: Start prompt 붙여넣기 + `AGENTS.md` 규칙.

_Updated: {ts}_

## Gate snapshot

{chr(10).join(_gate_snapshot_lines(gate))}

## Read first

{read_block}

## Start prompt

```text
{start_prompt}
```

## Deeplink (Cursor · 새 Chat · 프롬프트 미리 채움 · 전송 전 확인)

- Cursor: [{deeplink}]({deeplink})
- Web: [{web_link}]({web_link})

**Claude Code / Codex / Antigravity:** Deeplink 없음 → **Start prompt** 복사·붙여넣기. Claude Code는 `/clear` 또는 새 세션 시 `SessionStart` 훅이 요약 주입.

## Same-chat fallback

새 Chat 없이 이어갈 때는 위 Start prompt를 **현재 채팅**에 붙여넣어도 됩니다 (토큰은 계속 쌓입니다).
"""


def write_handoff(
    root: Path,
    gate: dict[str, Any],
    *,
    reason: str = "manual",
    prev_phase: int | None = None,
) -> Path:
    plan_rel = find_phase_plan(root)
    body = render_handoff_markdown(
        root, gate, plan_rel=plan_rel, reason=reason, prev_phase=prev_phase
    )
    path = handoff_path(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")
    return path


def read_handoff_for_session(root: Path, gate: dict[str, Any]) -> str | None:
    """Compact context for sessionStart hook."""
    path = handoff_path(root)
    if path.is_file():
        text = path.read_text(encoding="utf-8")
        # Keep hook payload small: snapshot + start prompt block
        parts: list[str] = [
            "## Chat handoff (auto-injected at session start)",
            "",
            "A previous chat ended or advanced Phase. Continue from files, not prior messages.",
            "",
        ]
        for header in ("## Gate snapshot", "## Start prompt"):
            if header in text:
                chunk = text.split(header, 1)[1]
                chunk = chunk.split("\n## ", 1)[0].strip()
                parts.append(header.replace("## ", "### "))
                parts.append(chunk)
                parts.append("")
        parts.append("Full handoff: `@.cursor/handoff.md` · gate: `@.cursor/gate.json`")
        return "\n".join(parts).strip()

    if gate.get("enabled") and gate.get("plan_approved"):
        phase = int(gate.get("phase") or 1)
        step = str(gate.get("step") or "explore")
        return (
            f"Phase gate active: phase={phase}, step={step}. "
            f"No `.cursor/handoff.md` yet — run `./scripts/gate.sh handoff` after next-phase if needed."
        )
    return None
