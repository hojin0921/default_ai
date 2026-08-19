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
7. End with a **numbered Korean menu**, for example:
   1. 이 전체 계획을 승인하고, Phase 1의 1단계(코드 없이 이해하기)부터 진행해 주세요  
      → run `./scripts/gate.sh on` then `approve-plan`, then Phase 1 Explore only  
   2. 계획 내용을 수정해 주세요 (지금은 승인하지 않음)  
   3. 지금은 보류할게요. 나중에 이어갈게요  
   Do not run mutating `gate.sh` until they pick an option this turn. (They may run the same CLI in the terminal instead.)

## Out of scope

- Writing application code under `src/` (or equivalent)
- Skipping to Implement
- Editing `.cursor/gate.json` directly, or advancing the gate without an explicit human chat choice
