---
name: phase-gate
description: >-
  Explains and respects the human-owned phase gate (.cursor/gate.json and
  scripts/gate.sh). Use when the user mentions gate, approve-plan, allow-commit,
  phase enforcement, or commit blocked by phase-gate.
---

# Phase Gate

## Model

Human-owned file: `.cursor/gate.json`

| Field | Meaning |
|-------|---------|
| `enabled` | Large enforcement on/off (Small → off) |
| `plan_approved` | Whole plan approved |
| `phase` | Current Delivery Phase number |
| `step` | explore\|document\|plan\|implement\|verify\|review\|human_verify |
| `allow_commit` | git commit allowed |

## Human commands

```bash
./scripts/install-hooks.sh          # once per clone
./scripts/gate.sh status
./scripts/gate.sh on                # start Large
./scripts/gate.sh approve-plan      # after reviewing Draft plan
./scripts/gate.sh advance implement # after approving Phase detail plan
./scripts/gate.sh allow-commit      # after Verify / user test
./scripts/gate.sh next-phase
./scripts/gate.sh off               # Small work
```

## Agent rules

- Never edit `.cursor/gate.json`.
- Never run mutating `gate.sh` (on/off/approve-plan/advance/allow-commit/deny-commit/next-phase).
- `gate.sh status` is OK.
- If blocked by hooks, tell the human which `gate.sh` command to run.
