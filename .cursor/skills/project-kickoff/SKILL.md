---
name: project-kickoff
description: >-
  Splits a new product request into Delivery Phases and writes a Draft plan
  without implementing. Use when the user describes a project to build, lists
  must-have features, asks for a full project plan, or starts a Large kickoff.
---

# Project Kickoff

## Instructions

1. Treat the request as **Large / kickoff**. Do **not** implement code yet.
2. Optionally do a short Explore of existing repo patterns; do not read all of `docs/`.
3. Create `.cursor/plans/<short-name>.md` from `.cursor/plans/_template.md`.
4. Map every must-have feature to a Delivery **Phase 1…N** (dependency, risk, demoable slices).
5. For each Phase, fill Goal, In/Out, AI Verify, User Test Guide draft, and the 6-step checklist.
6. Set Status to **Draft**. Ask the human to approve before any Phase work.
7. Tell the human:
   - Review the plan
   - Large gate (optional): `./scripts/gate.sh on` then after approve `./scripts/gate.sh approve-plan`
   - Next: run Delivery Phase skill starting at Phase 1 step Explore only

## Out of scope

- Writing application code under `src/` (or equivalent)
- Skipping to Implement
- Advancing `.cursor/gate.json` (human-only via `./scripts/gate.sh`)
