---
name: project-kickoff
description: >-
  Large kickoff: question round, then overall design agreement, then docs,
  then Delivery Phase Plan. Never implement. Use when the user describes a
  project to build, lists must-have features, or starts a new product.
---

# Project Kickoff

## Roles

| Step | Primary | Skill(s) |
|------|---------|----------|
| K1 Discover | 시니어 기획 | `senior-pm` |
| K2 Design | 기획 + 설계 | `senior-pm`, `senior-architect` (+ `senior-design` if UI) |
| K3 Docs | 설계 / 기획 | `senior-architect` / `senior-pm` |
| K4 Phase Plan | 기획 + 설계 | `senior-pm`, `senior-architect` |

Start replies with `역할: 시니어 ○○`.  
If the user explicitly names one role for the turn, that override wins (`delivery-phase` / `guide.md` §2-3).

## Instructions

Treat the request as **Large / kickoff**. Do **not** implement app code.  
Do **not** skip to K4. Do **not** write a Phase Plan during K1.

Decision UI after each step: prefer **`AskQuestion`** (Korean options); else numbered `1` / `2` / `3`.  
Do not run mutating `gate.sh` until they pick an option this turn.

K2 option 1 → `./scripts/gate.sh approve-design` then K3.  
K3 option 1 → `./scripts/gate.sh kickoff phase_plan` then K4.  
K4 option 1 → `./scripts/gate.sh approve-plan` then Phase 1 Explore only. Do **not** run `on` together with `approve-plan` (`on` clears `design_approved`).

### K1 Discover

1. Optional short Explore of existing repo patterns; do not read all of `docs/`.
2. Ask **3–7 questions** in one batch (not 20). Topics as needed: users/problem, must-have vs later, platform/stack, auth/data/integrations, success/MVP, explicit Out. User may answer “모르겠어, 제안해”.
3. Do **not** write `.cursor/plans/` Phase Plan, `docs/` body, or `src/`.
4. Summarize understanding. End with:

   1. 이 이해로 전체 설계 초안을 작성해 주세요 → K2 only  
   2. 더 질문하거나 이해를 수정해 주세요  
   3. 지금은 보류할게요  

   If still ambiguous after ~2 rounds, propose defaults and ask to proceed to K2.

### K2 Design

1. Create `.cursor/plans/<short-name>-design.md` from `.cursor/plans/_design-template.md`.
2. Fill from K1 answers only; mark remaining gaps as Open questions. Status **Draft**.
3. Do **not** write Phase Plan (`_template.md`) or fill `docs/` yet.
4. End with:

   1. 이 전체 설계를 합의하고, 이제 문서화해 주세요  
      → `./scripts/gate.sh approve-design`, then K3 only  
   2. 설계 내용을 수정해 주세요 (문서화는 아직 하지 않음)  
   3. 지금은 보류할게요  

### K3 Docs

1. Write agreed design into `docs/` (no guesswork beyond the design file):
   - `docs/product.md` (users, must-have, journeys, Out)
   - `docs/architecture.md` (structure, data, boundaries, integrations)
   - `docs/security.md` if security decisions exist (no secrets)
   - `docs/README.md` status
   Leave development/testing/deployment TODO if unknown.
2. Mark `*-design.md` Status **Documented** (optional).
3. Do **not** write Phase Plan yet.
4. End with:

   1. 문서를 확인했습니다. Phase Plan 초안을 작성해 주세요  
      → `./scripts/gate.sh kickoff phase_plan`, then K4 only  
   2. 문서를 수정해 주세요  
   3. 지금은 보류할게요  

### K4 Phase Plan

1. Create `.cursor/plans/<short-name>.md` from `.cursor/plans/_template.md`.
2. Map every must-have feature to Delivery **Phase 1…N** (dependency, risk, demoable slices).
3. For each Phase, fill Goal, In/Out, AI Verify, User Test Guide draft, and the 6-step checklist.
4. Set Status to **Draft**. Ask the human to approve before any Delivery Phase work.
5. End with:

   1. 이 전체 계획을 승인하고, Phase 1의 1단계(코드 없이 이해하기)부터 진행해 주세요  
      → `./scripts/gate.sh approve-plan`, then Phase 1 Explore only  
   2. 계획 내용을 수정해 주세요 (지금은 승인하지 않음)  
   3. 지금은 보류할게요. 나중에 이어갈게요  

## Out of scope

- Writing application code under `src/` (or equivalent)
- Skipping K1–K3
- Skipping to Implement
- Editing `.cursor/gate.json` directly, or advancing the gate without an explicit human chat choice
