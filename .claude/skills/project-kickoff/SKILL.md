---
name: project-kickoff
description: >-
  Large kickoff: question round, then overall design agreement, then docs,
  then Delivery Phase Plan. Never implement. Use when the user describes a
  project to build, lists must-have features, or starts a new product.
---

# Project Kickoff

## Roles

| Step | Launch (sequential if several) | Skill Quality bar |
|------|--------------------------------|-------------------|
| K1 Discover | `senior-pm` | `senior-pm` |
| K2 Design | `senior-pm` then `senior-architect` then (`senior-design` if UI) | matching |
| K3 Docs | `senior-pm` (`docs/product.md`) then `senior-architect` | matching |
| K4 Phase Plan | `senior-pm` then `senior-architect` | matching |

You are the **orchestrator**. Do **not** write K2/K3/K4 specialist bodies yourself. Launch per `delivery-phase` **Specialist launch** (host adapter + Isolation Pass). Input package: K1 answers, paths, previous artifacts. No `.env` secrets.

Start orchestrator replies by naming whom you launched, e.g. `역할: 시니어 기획` after `senior-pm` returns.  
If the user explicitly names one role for the turn, launch **only** that agent (`delivery-phase` / `guide.md` §2-3).  
The launched agent must meet that role skill’s **Quality bar**.

## Instructions

Treat the request as **Large / kickoff**. Do **not** implement app code.  
Do **not** skip to K4. Do **not** write a Phase Plan during K1.

**First K1 reply:** show a short friendly **시작 가이드** (`guide.md` §3-0). If they already described the product, use it—do not make them paste the template. Then ask **exactly one** question (AskQuestion). Tone: kind, short, Korean.

Decision UI after each step: prefer **`AskQuestion`** (or host equivalent); else numbered `1` / `2` / `3`.  
**한 메시지에 질문 하나.** K1에서 확인 질문 6개를 한 번에 나열하지 않는다.  
Do not run mutating `gate.sh` until they pick an option this turn.

### 한눈 그림 (같은 답변에 반드시)

If you will ask the human to look at a picture, **draw it in this reply first**.  
A prompt like “바로 위 한눈 그림” with no diagram in the same message is a fail.

Order in the message: `역할:` → 짧은 설명 → **한눈 그림 블록** → 지금 볼 곳(해당 시) → AskQuestion.

Required block (copy and fill; do not omit). Use a mermaid fence in the **user-facing** reply, not only in a plan file:

- Heading `## 한눈 그림`
- A `mermaid` code block with `flowchart LR` and 5–12 Korean node labels
- A line `글 흐름: 사람 → 하는 일 → 결과` (always visible if Mermaid does not render)

Never say only “아래 그림과 파일을 확인하세요”. People do not know where “아래” is.

Before the choice UI, always put this block **after** the Mermaid:

```
## 지금 볼 곳
- 그림: 선택 버튼 **바로 위**, 이 답변 안에 그린 Mermaid입니다. 다른 폴더·탭을 찾지 마세요.
- 파일: (파일이 있을 때만) 에디터에서 아래 경로를 여세요. Cursor는 왼쪽 트리 또는 `Cmd+P`(Windows `Ctrl+P`).
  - `.cursor/plans/<실제-파일>.md` — (한 줄: 무엇을 보는지)
```

AskQuestion `prompt` must say the picture is **바로 위**, and name the real path when there is a file, e.g.  
`바로 위 한눈 그림(이 답변에 그린 Mermaid)과, 에디터에서 .cursor/plans/<name>-design.md 를 연 뒤 어떻게 할까요?`

Before every K1 (after 이해 요약), K2/K3/K4, and Phase Explore/Document/Plan choice:
1. Put the **한눈 그림 블록** in **this reply** (Mermaid fence + 글 흐름). Do not AskQuestion about a picture that is missing from this message.
2. For K2/K3/K4 and Delivery Plan, also put **지금 볼 곳**.

K1 diagram: current understanding (who → does what → result). Unknown = a node `미정`.  
K2 diagram: user journey and/or system (who → what → where). Same figure goes into `*-design.md`.  
K4 diagram: Phase 1→N left-to-right (or top-down) with short titles. Same figure goes into the Phase Plan.  
K3: reuse the agreed K2 diagram in chat; do not invent a new architecture.

K2 option 1 → `./scripts/gate.sh approve-design` then K3.  
K3 option 1 → `./scripts/gate.sh kickoff phase_plan` then K4.  
K4 option 1 → `./scripts/gate.sh approve-plan` then Phase 1 Explore only. Do **not** run `on` together with `approve-plan` (`on` clears `design_approved`).

### K1 Discover

1. Start with the **시작 가이드** (`guide.md` §3-0 bullets). Optional short Explore of existing repo patterns; do not read all of `docs/`.
2. Ask **one question per turn** with AskQuestion or host equivalent (or one numbered question if unavailable).  
   - Do **not** paste a list titled “확인이 필요한 질문 (6개)” or similar. Never dump the checklist as one questionnaire.  
   - Every question includes **「제안해」** (and **「잘 모르겠음」** when useful).  
   - Skip a topic only if the first prompt already answered it **specifically** (not “편하게”, “그냥 웹”).  
   - After each answer: one line of what you now assume, then the **next single** question.  
   - **Follow-up (required when thin):** if the answer is vague, adjective-only, or “다 / 모두 / 잘 됐으면”, ask **one deeper question on the same topic** before moving on. Max **two** follow-ups per topic, then propose a default and continue.  
   - **Cover this checklist** (order may follow the last answer; do not skip a hole to rush K2):
     1. Who it is for (concrete user, not “everyone”)
     2. Primary job / success (what they do → what “done” looks like)
     3. Must-have now vs later (cut)
     4. Surface (web / app / both / CLI)
     5. If UI: key flow screen-by-screen (entry → success). If no UI: say so and skip 6.
     6. If UI: empty / error / fail (what they see)
     7. Login / stored data / none (what is saved, who can see it)
     8. Constraints (deadline, **platform** — web/iOS/Android/CLI/API-only/deploy, must-not) and **Out** (explicitly not building)
     9. Only if it is a game: win/lose and what is fun. Only if visual tone is still unknown and there is UI: look-and-feel in one question (not a brand book)
   - Typical total **8–14** questions including follow-ups. Cap **16**. First-prompt answers that are specific still skip that topic.  
   - Do **not** ask frontend/backend/DB languages here. That is **구현 직전** (`delivery-phase` Stack pick — **contextual** options from design). If they already named a stack in the first prompt, record it; otherwise leave Stack as **미정**.  
3. Do **not** write `.cursor/plans/` Phase Plan, `docs/` body, or `src/`.
4. Go to the 이해 요약 only when every checklist item has a specific answer **or** a stated default. Do not end K1 after 4–7 broad questions if holes remain.  
   Then summarize, then the **한눈 그림 블록** (Mermaid + 글 흐름) in this reply, then:

   AskQuestion prompt: `바로 위 한눈 그림(이 답변에 그린 Mermaid)을 보신 뒤, 전체 설계 초안으로 갈까요?`

   1. 이 이해로 전체 설계 초안을 작성해 주세요 → K2 only  
   2. 더 질문하거나 이해를 수정해 주세요  
   3. 지금은 보류할게요  

   If still ambiguous after the cap or ~2 “제안해” loops on the same hole, propose defaults for the rest and ask to proceed to K2.

### K2 Design

1. Create `.cursor/plans/<short-name>-design.md` from `.cursor/plans/_design-template.md`.
2. Fill from K1 answers only; mark remaining gaps as Open questions. Status **Draft**. Include a **한눈 그림** (Mermaid) in the file and in chat.  
   **Stack:** if K1 already named languages, copy them. Otherwise **미정** (구현 직전 사람 선택). Do not invent Next.js/Postgres here.
3. Do **not** write Phase Plan (`_template.md`) or fill `docs/` yet.
4. End with the **한눈 그림**, then **지금 볼 곳** (path + how to open), then:

   AskQuestion prompt: `바로 위 한눈 그림(이 답변에 그린 Mermaid)과, 에디터에서 .cursor/plans/<short-name>-design.md 를 연 뒤 어떻게 할까요?`

   1. 이 전체 설계를 합의하고, 이제 문서화해 주세요  
      → `./scripts/gate.sh approve-design`, then K3 only  
   2. 설계 내용을 수정해 주세요 (문서화는 아직 하지 않음)  
   3. 지금은 보류할게요  

### K3 Docs

1. Write agreed design into `docs/` (no guesswork beyond the design file):
   - `docs/product.md` (users, must-have, journeys, Out)
   - `docs/architecture.md` (structure, data, boundaries, integrations, Stack if already chosen else **미정**; include the K2 mermaid)
   - `docs/security.md` if security decisions exist (no secrets)
   - `docs/README.md` status
   Leave development/testing/deployment TODO if unknown.
2. Mark `*-design.md` Status **Documented** (optional).
3. Do **not** write Phase Plan yet.
4. End with the agreed K2 **한눈 그림** (do not invent a new one), then **지금 볼 곳** of every docs path written this step, then:

   AskQuestion prompt: `바로 위 한눈 그림(이 답변에 그린 Mermaid)과, 에디터에서 docs/product.md (및 안내한 경로)를 연 뒤 어떻게 할까요?`

   1. 문서를 확인했습니다. Phase Plan 초안을 작성해 주세요  
      → `./scripts/gate.sh kickoff phase_plan`, then K4 only  
   2. 문서를 수정해 주세요  
   3. 지금은 보류할게요  

### K4 Phase Plan

1. Create `.cursor/plans/<short-name>.md` from `.cursor/plans/_template.md`.
2. Map every must-have feature to Delivery **Phase 1…N** (dependency, risk, demoable slices).
3. For each Phase, fill Goal, In/Out, AI Verify, User Test Guide draft, 실행 가이드 draft (or “실행 대상 없음”), and the 6-step checklist. Leave **역할 기여** rows empty until Review / last Phase.
4. Add a **한눈 그림** (Mermaid flowchart Phase 1→N, short titles, arrows = 순서·의존). Put it in the plan file and in chat.
5. Set Status to **Draft**. Ask the human to approve before any Delivery Phase work.
6. End with the Phase **한눈 그림**, then **지금 볼 곳**, then:

   AskQuestion prompt: `바로 위 한눈 그림(이 답변에 그린 Mermaid)과, 에디터에서 .cursor/plans/<short-name>.md 를 연 뒤 어떻게 할까요?`

   1. 이 전체 계획을 승인하고, Phase 1의 1단계(코드 없이 이해하기)부터 진행해 주세요  
      → `./scripts/gate.sh approve-plan`, then Phase 1 Explore only  
   2. 계획 내용을 수정해 주세요 (지금은 승인하지 않음)  
   3. 지금은 보류할게요. 나중에 이어갈게요  

## Out of scope

- Writing application code under `src/` (or equivalent)
- Skipping K1–K3
- Skipping to Implement
- Editing `.cursor/gate.json` directly, or advancing the gate without an explicit human chat choice
