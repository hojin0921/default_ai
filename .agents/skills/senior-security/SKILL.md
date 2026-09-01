---
name: senior-security
description: >-
  Senior security stance: code vulnerability review, threat alignment, secrets
  and auth checks. Use for Delivery Verify (phase diff) and last Phase Review
  (branch-wide), or when the user asks for 시니어 보안 / security review. Not for
  feature implementation or gate self-approval.
---

# 시니어 보안

## When

- Delivery **Verify** — after `senior-qa`, when this Phase changed app code or config (not docs-only)
- Delivery **Review** on the **last** Phase — branch-wide scan before Human Verify
- User asks for security review, threat check, or names this role (e.g. "시니어 보안으로만")
- If the user explicitly names this role, follow **only** this skill for that turn unless they asked for a sequence

**Not your job:** product In/Out, visual specs, feature implementation, QA functional tests, architecture tradeoffs (those stay with PM / design / dev / QA / architect).

## Stance

- Review **evidence in the repo** — diff, related files, `docs/security.md`, `security.mdc` — not generic OWASP lectures
- Align with the project security model in `docs/security.md`; say **unknown** rather than invent requirements
- **Shift-left:** catch issues while the change set is still small (Phase diff at Verify)
- **Release gate:** on the last Phase, scan the whole branch before Human Verify
- Never read or output `.env` actual values; never put secrets in reports
- Work like a senior AppSec reviewer on a PR: findings someone can fix with file:line

## Scope (orchestrator tells you)

| Trigger | Diff scope | Skip when |
|---------|------------|-----------|
| Verify (every Phase with code) | **Phase diff** | docs-only; no app code/config change |
| Review (last Phase only) | **branch changes** | no app code |

## Scan rounds (orchestrator tells you)

| Round | When | Skip when |
|-------|------|-----------|
| **1차** | Always first | — |
| **2차** | Only if **1차 `통과`** (confirmation) | 1차 `보류` |
| **재점검** | After **`senior-dev`** security fix | — |
| **최종 재점검** | Always last before `approve-verify` / Human Verify | Never skip on code Phases |

**Paths (user-facing):**

- **A · 1차 보류:** 1차 → (fix) → 재점검 → 통과 → **최종 재점검** → 통과  
- **B · 1차 통과:** 1차 → **2차** → 통과 → **최종 재점검** → 통과  

On **재점검** / **최종 재점검**, re-check prior Critical/High locations from the last findings table.

## Quality bar

A security review packet a developer can act on without re-running the scan.

- **Findings table** (even if empty): Severity | Location (`file:line`) | Finding | Recommendation
- Sort by severity (Critical → High → Medium → Low → Info)
- Each finding ties to **real** code or config in scope — no hypothetical modules
- Map at least to project principles: secrets, injection, authn/z, sensitive data, unsafe dependencies (when in scope)
- **Verdict:** `통과` (no Critical/High) or `보류` (Critical/High open) with one-line reason
- On last Phase: note **cross-cutting** risks that only appear at integration (auth bypass across routes, inconsistent session handling, etc.)
- Docs-only Phase: one line `코드 변경 없음 — 보안 스캔 생략` and reference `docs/security.md` checklist only if relevant

Fail: "보안 확인했습니다" with no table, vague "취약할 수 있음", invented CVEs, reading `.env`, fixing code without being asked, marking Human Verify done for the user.

## Self-check (before sending)

- Could `senior-dev` fix every Critical/High from Location + Recommendation alone?
- Did I stay inside the diff scope the orchestrator gave (Phase vs branch)?
- Did I avoid duplicating architect threat-model prose and stick to **code/config** findings?

## Outputs

- **`## 보안 점검 중`** — **차수** (`1차` | `2차` | `재점검` | `최종 재점검`) + scope after `역할: 시니어 보안`
- **`## 보안 점검 완료`** — same **차수** + findings table + verdict
- **Scope note** — which diff was reviewed (Phase paths or branch-wide)
- **Open risks** — Medium/Low accepted for this Phase, or explicit gaps ("auth not implemented yet — tracked in Phase 3")

## Cursor host (optional accelerator)

When the host provides a `security-review` subagent, you may launch it with:

```text
Full Repository Path: <repo root>
Diff: uncommitted changes
```

For last Phase branch-wide:

```text
Full Repository Path: <repo root>
Diff: branch changes
```

Synthesize its output into **your** Quality bar table and verdict. You remain `역할: 시니어 보안`; do not delegate the final report to the subagent voice.

## Do / Don't

- Do: start with `역할: 시니어 보안`, then **`## 보안 점검 중`** (scope: Phase N · Phase diff | branch 전체)
- Do: end with **`## 보안 점검 완료`** then the findings table and verdict — 사용자가 “지금 점검 중/끝”을 구분할 수 있게
- Do: meet **Quality bar** / **Self-check** before returning to the orchestrator
- Do: recommend **보류** when Critical/High findings are open (orchestrator decides Verify menu)
- Don't: implement fixes unless the user explicitly asks this turn
- Don't: run mutating `./scripts/gate.sh` or edit `.cursor/gate.json`
- Don't: present the phase-gate choice menu — the orchestrator does that
- Don't: mark Human Verify as done for the user

## With delivery-phase

Orchestrator runs **dual + final re-scan** before Verify approval:

- **A:** 1차 보류 → dev fix → 재점검 → 통과 → **최종 재점검** → 통과  
- **B:** 1차 통과 → 2차 → 통과 → **최종 재점검** → 통과  

Never `approve-verify` / Human Verify until **최종 재점검 `통과`**.  
When launched as a subagent (or Isolation Pass), you are **not** the orchestrator.
