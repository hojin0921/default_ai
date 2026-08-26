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

### Quality

The primary `senior-*` skill’s **Quality bar** is mandatory. Generic adjectives, empty Out, “구현 완료” with no paths, or a 직접 확인 가이드 a stranger cannot follow all fail—**rewrite before** the human choice UI. Do not skip Self-check.

**그림 누락 금지:** Explore / Document / Plan (and kickoff K1 이해·K2/K3/K4) replies that ask the human to look at a 한눈 그림 must include, in **this same message**, a mermaid code fence **and** a one-line `글 흐름: A → B → C`. Asking “바로 위 그림을 보세요” with no diagram in the reply is a fail—draw it, then AskQuestion.

### Step order (required)

1. **Explore** — No code changes. Summarize requirements, related code, patterns, blast radius.  
   In **this same reply**, before AskQuestion: heading `## 한눈 그림`, a mermaid `flowchart LR` fence (fill with this Phase), and `글 흐름: 입력 → 이 Phase 핵심 → 결과`.  
   **지금 볼 곳**: 그림은 선택 버튼 바로 위(이 답변). 파일이 없으면 파일을 찾으라고 하지 말 것.  
   AskQuestion: `바로 위 한눈 그림(이 답변에 그린 Mermaid와 글 흐름)을 보신 뒤, 다음으로 어떻게 할까요?`
2. **Document** — Update relevant `docs/` / README from evidence only. Foundation product/architecture docs are kickoff **K3**. Phase 1+ Document is **deltas only**.  
   Show the Explore mermaid again (or the updated one if the flow changed) in chat; put it in the docs you touch if the journey/system changed.
3. **Plan** — Detail this Phase (files, order, tests, User Test Guide draft). Wait for human approval before Implement.  
   Before the approve/implement choice, show:
   - **한눈 그림**: Mermaid of **this Phase only** (작업 순서: 무엇 → 무엇). Not the whole 1→N kickoff diagram unless reminding context in one line.
   - **지금 볼 곳**: every path this Phase will change, plus how to open in Cursor (`Cmd+P`).
   AskQuestion prompt: `바로 위 한눈 그림(이 답변에 그린 Mermaid)과, Cursor에서 <Plan 경로> 를 연 뒤 어떻게 할까요?`

   예시:
   ```mermaid
   flowchart LR
     A["1 스키마"] --> B["2 API"]
     B --> C["3 UI"]
     C --> D["4 테스트"]
   ```
   ```
   ## 지금 볼 곳
   - 그림: 선택 버튼 **바로 위**, 이 답변 안의 Mermaid
   - 파일: Cursor에서 `Cmd+P`로 열기
     - `.cursor/plans/<name>.md` — 이 Phase 상세
   ```
4. **Implement** — Minimal changes for this Phase only.  
   If the product is now runnable, put **실행 가이드** in the chat (준비 / 실행 / 접속) and fill `README.md` Setup + `docs/development.md` from evidence (no guessed commands). If there is nothing to run, say so in one line.
5. **Verify** — Run related tests → typecheck/lint → build if needed. Never delete/weaken tests to pass.  
   Then put **직접 확인 가이드** in the chat **before** the decision UI. Do not ask for play-test results without this block. A human who is not the author must be able to follow it.

   If this is the **last** Delivery Phase (no later Phase in the Plan), put **실행 가이드** then **역할 기여** *before* 직접 확인 가이드.  
   실행 가이드 = how to start the finished product.  
   역할 기여 = which 시니어 역할 made what, and how it is used (evidence from Plan/docs/code; unused roles = “해당 없음”).  
   직접 확인 가이드 = how to check this Phase.

   ```
   ## 실행 가이드
   - 준비: (런타임·설치 명령. `.env.example` 이름만, 실제 secret 금지)
   - 실행: (복사해 실행할 명령)
   - 접속: (URL / 열 화면)
   - 상세: `README.md`, `docs/development.md`
   ```

   ```
   ## 역할 기여
   | 역할 | 만든 것 | 어떻게 쓰이는지 |
   | 시니어 기획 | (경로·산출물) | (범위·우선순위 기준으로 어디에 쓰였는지) |
   | 시니어 설계 | | |
   | 시니어 디자인 | 해당 없음 (UI 없음) | |
   | 시니어 개발 | | |
   | 시니어 QA | | |
   ```
   Same table goes into the Phase Plan `## 역할 기여 (전체)`. Kickoff K1–K4도 한 줄씩 넣는다.

   ```
   ## 직접 확인 가이드
   - 실행: (복사해 실행할 명령, 또는 열 화면/URL)
   - 확인: (클릭·입력·볼 화면을 순서대로)
   - 기대: (성공이면 어떻게 보여야 하는지)
   - 실패 시: (에러 문구, 재현 순서, 기대 vs 실제를 채팅에 붙여 주세요)
   ```

   If there is no runnable UI (protocol/docs-only Phase), say so and give file/CLI checks instead of “플레이”.  
   AskQuestion prompt: `Phase N을 직접 플레이해 보신 결과는 어떤가요?`  
   Docs-only: `Phase N을 직접 확인해 보신 결과는 어떤가요?`  
   Option labels must not mention 커밋. Humans `git commit` themselves after picking 통과 (`allow-commit` behind the scenes).
6. **Review** — Short self-review (gaps, bugs, security, scope creep). Stop for Human Verify.  
   Fill this Phase’s **역할 기여** bullets in the Plan (what this role actually produced). On the last Phase, compile the whole-project table in chat and in the Plan.

### After each step

Every reply for this Phase work must include the line `역할: 시니어 ○○` (Role map, or the user-overridden role).  
Report: what changed, and a **decision UI** for the next human choice when the gate is enabled (or when approval is required). Prefer **`AskQuestion`** with Korean options from `guide.md` §4; if unavailable, use numbered Korean text. When the choice is “approve this design/docs/plan”, show a small **Mermaid 한눈 그림**, then **지금 볼 곳** (채팅 안 그림 + Cursor에서 열 실제 경로). After Explore/Document, show the step’s **한눈 그림**. After Implement, show **실행 가이드** if runnable. After Verify, show **직접 확인 가이드** first (and **실행 가이드** then **역할 기여** first if this is the last Phase). Do not advance the gate without an explicit choice this turn.

### Gate (when `.cursor/gate.json` enabled)

- Source of truth is `gate.json`, not plan Status markdown.
- Never edit `gate.json` directly.
- After an explicit human chat choice, run the matching `./scripts/gate.sh` command; otherwise re-offer the menu (terminal CLI is equivalent).
- Code writes require `plan_approved` and step in `implement|verify|review`.
