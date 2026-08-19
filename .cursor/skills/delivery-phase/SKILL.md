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

Report: what changed, and a **numbered Korean chat menu** for the next human decision when the gate is enabled (or when approval is required). Use the phrasing in `guide.md` §4. Do not advance the gate without an explicit choice this turn.

### Gate (when `.cursor/gate.json` enabled)

- Source of truth is `gate.json`, not plan Status markdown.
- Never edit `gate.json` directly.
- After an explicit human chat choice, run the matching `./scripts/gate.sh` command; otherwise re-offer the menu (terminal CLI is equivalent).
- Code writes require `plan_approved` and step in `implement|verify|review`.
