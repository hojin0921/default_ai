---
name: delivery-phase
description: >-
  Runs one Delivery Phase using the fixed 6 steps Explore→Document→Plan→
  Implement→Verify→Review with User Test Guide. Use when the user approves a
  plan, asks to start or continue a Phase, advance a step, or says explore /
  document / plan / implement / verify / review for the current Phase.
---

# Delivery Phase (6 steps)

## Instructions

Work **only the current Phase** and **only the current step**. Do not start the next Phase until Human Verify.

At the start of each reply for this Phase work, state the active role line, e.g.
`역할: 시니어 설계`. Read and follow the matching **role Skill** under `.cursor/skills/`.

### Role map (primary → Skill)

| Step | Primary | Optional | Skill(s) |
|------|---------|----------|----------|
| 1 Explore | 설계 (+ 기획) | — | `senior-architect`, `senior-pm` |
| 2 Document | 설계 / 기획 | 디자인 if UX docs | `senior-architect` / `senior-pm` (+ `senior-design`) |
| 3 Plan | 기획 + 설계 | 디자인 if UI; 개발 for feasibility | `senior-pm`, `senior-architect` (+ …) |
| 4 Implement | 개발 | 디자인 if UI | `senior-dev` (+ `senior-design`) |
| 5 Verify | QA | 개발 for fixes | `senior-qa` (+ `senior-dev`) |
| 6 Review | QA + 설계 | 기획 for requirement gaps | `senior-qa`, `senior-architect` (+ `senior-pm`) |

### Explicit role override

If the user names a senior role this turn (e.g. `시니어 QA로만`, `시니어 디자인 관점으로`), that role **wins over** the Role map for the reply. Follow only that `senior-*` skill; skip other senior stances unless they asked for a sequence (e.g. 설계 후 QA). Still honor Phase step limits (no Implement during Explore) and phase-gate rules. See `guide.md` §2-3.

### Step order (required)

1. **Explore** — No code changes. Summarize requirements, related code, patterns, blast radius.
2. **Document** — Update relevant `docs/` / README from evidence only. Phase 1: foundation docs; later Phases: deltas only.
3. **Plan** — Detail this Phase (files, order, tests, User Test Guide draft). Wait for human approval before Implement.
4. **Implement** — Minimal changes for this Phase only.
5. **Verify** — Run related tests → typecheck/lint → build if needed. Never delete/weaken tests to pass. Then output **User Test Guide**:
   - Setup / Run
   - What to check
   - Expected result
   - What to report if it fails
6. **Review** — Short self-review (gaps, bugs, security, scope creep). Stop for Human Verify.

### After each step

Every reply for this Phase work must include the line `역할: 시니어 ○○` (Role map, or the user-overridden role).  
Report: what changed, and a **decision UI** for the next human choice when the gate is enabled (or when approval is required). Prefer **`AskQuestion`** with Korean options from `guide.md` §4; if unavailable, use numbered Korean text. Do not advance the gate without an explicit choice this turn.

### Gate (when `.cursor/gate.json` enabled)

- Source of truth is `gate.json`, not plan Status markdown.
- Never edit `gate.json` directly.
- After an explicit human chat choice, run the matching `./scripts/gate.sh` command; otherwise re-offer the menu (terminal CLI is equivalent).
- Code writes require `plan_approved` and step in `implement|verify|review`.
