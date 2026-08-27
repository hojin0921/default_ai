---
name: phase-gate
description: >-
  Explains the phase gate (.cursor/gate.json and scripts/gate.sh). Prefer
  AskQuestion (or host equivalent) when available; else Korean numbered text.
  Agent may run mutating gate.sh only after an explicit choice. Use when the
  user mentions gate, approve-plan, approve-design, kickoff, allow-commit,
  phase enforcement, or commit blocked by phase-gate.
---

# Phase Gate

## Model

Source of truth: `.cursor/gate.json`

| Field | Meaning |
|-------|---------|
| `enabled` | Large enforcement on/off (Small → off) |
| `plan_approved` | Whole Phase Plan approved |
| `design_approved` | Kickoff overall design agreed |
| `phase` | Current Delivery Phase number |
| `step` | explore\|document\|plan\|implement\|verify\|review\|human_verify |
| `kickoff_step` | discover\|design\|docs\|phase_plan\|done |
| `allow_commit` | git commit allowed |

## Channel (default: chat)

At decision points, **do not** advance the gate or implement until the human
picks an option in **this** turn.

### How to present the choice

1. **Prefer `AskQuestion`** (or the host equivalent, e.g. Claude Code
   `AskUserQuestion`) when available — one single-select question, Korean
   option labels (same wording as below). This may render as a clickable card.
2. **If unavailable**, fall back to a short Korean numbered `1` / `2` / `3`
   list in chat. Do not invent a fake button UI in markdown.
3. After an unambiguous choice, run the matching `./scripts/gate.sh`
   command(s) for that option (one decision per turn; a menu item may bundle
   a documented set). Then `./scripts/gate.sh status`
   and report briefly.
4. If the choice is unclear, ask again — do not run mutating `gate.sh`.
5. For K1 (after 이해 요약), K2/K3/K4, Phase Explore/Document, and Phase detail Plan: the **same reply** must contain a fenced ```mermaid block and a `글 흐름: … → …` line **above** AskQuestion.  
   Never AskQuestion about a picture that is not in this message.  
   K2/K3/K4 and detail Plan also include **지금 볼 곳**. Files: open the path in the editor (Cursor: `Cmd+P` / `Ctrl+P`).  
   Prompt wording: 바로 위 한눈 그림(이 답변에 그린 Mermaid와 글 흐름). Name the path when there is a file.
6. After Verify, the chat body must include **직접 확인 가이드** before the choice UI. Last Phase: **실행 가이드** then **역할 기여** before that.

Humans may run the same CLI themselves (equivalent).

### Menu options (Korean — AskQuestion labels or text numbers)

**After K1 이해 요약** (한눈 그림 필수)

1. 이 이해로 전체 설계 초안을 작성해 주세요  
2. 더 질문하거나 이해를 수정해 주세요  
3. 지금은 보류할게요  

**After K2 overall design Draft**

1. 이 전체 설계를 합의하고, 이제 문서화해 주세요  
   → `./scripts/gate.sh approve-design`, then K3 only  
2. 설계 내용을 수정해 주세요 (문서화는 아직 하지 않음)  
3. 지금은 보류할게요  

**After K3 docs**

1. 문서를 확인했습니다. Phase Plan 초안을 작성해 주세요  
   → `./scripts/gate.sh kickoff phase_plan`, then K4 only  
2. 문서를 수정해 주세요  
3. 지금은 보류할게요  

**After whole-plan Draft (K4)**

1. 이 전체 계획을 승인하고, Phase 1의 1단계(코드 없이 이해하기)부터 진행해 주세요  
   → `./scripts/gate.sh approve-plan`, then Phase 1 Explore only  
   Do **not** run `on` with `approve-plan` (`on` clears `design_approved`).  
2. 계획 내용을 수정해 주세요 (지금은 승인하지 않음)  
   — same/next message may include edit details  
3. 지금은 보류할게요. 나중에 이어갈게요  

**After Phase detail Plan**

Chat must include a **한눈 그림** (this Phase work order) and **지금 볼 곳** (path + how to open in the editor).  
AskQuestion prompt: `바로 위 한눈 그림(이 답변에 그린 Mermaid)과, 에디터에서 <Plan 경로> 를 연 뒤 어떻게 할까요?`

1. 이 상세 계획을 승인하고, 이제 구현해 주세요  
   → `./scripts/gate.sh advance implement`, then Implement  
2. 상세 계획을 수정해 주세요 (구현은 아직 하지 않음)  
   — same/next message may include edit details  
3. 지금은 보류할게요  

**After Verify / Review (and human user test)**

Chat must include **직접 확인 가이드** (실행 / 확인 / 기대 / 실패 시) before the menu.  
If this is the **last** Phase in the Plan, also include **실행 가이드** (준비 / 실행 / 접속) and **역할 기여** (역할 / 만든 것 / 어떻게 쓰이는지) *before* 직접 확인 가이드.  
AskQuestion prompt (N = `gate.json` `phase`): `Phase N을 직접 플레이해 보신 결과는 어떤가요?`  
Protocol/docs-only: `Phase N을 직접 확인해 보신 결과는 어떤가요?`

Do **not** put 커밋 / `git commit` / `allow-commit` in option labels. Humans commit themselves.

1. 직접 확인해 보니 통과예요  
   → `./scripts/gate.sh allow-commit` (unlocks hook only; do not `git commit`)  
2. 아직 문제 있어요. 같은 Phase에서 고치고 검증을 다시 해 주세요  
   — same/next message may include what’s wrong / how to fix  
3. (다음 Phase가 있으면) 이 Phase는 통과. 다음 Phase로 가고, 지금은 조사(Explore)만 해 주세요  
   → `./scripts/gate.sh next-phase`, then Explore only  
   (`next-phase` does not change `allow_commit`. If already unlocked, it stays open.)  
3. (마지막 Phase이면) 이 Phase는 통과. 전체 개발을 마무리해 주세요  
   → do **not** run `next-phase`. Keep **실행 가이드** and **역할 기여** in the reply (or repeat them).  

When the human picks the **edit** option with extra instructions in the same
or next message, apply those edits and then re-offer the choice UI. Do not
treat “edit” alone as approval.

## Equivalent CLI

```bash
./scripts/install-hooks.sh          # once per clone
./scripts/gate.sh status
./scripts/gate.sh on                # Large reset (discover, design not approved)
./scripts/gate.sh approve-design    # after agreeing overall design
./scripts/gate.sh kickoff phase_plan
./scripts/gate.sh approve-plan      # requires design_approved
./scripts/gate.sh advance implement # after approving Phase detail plan
./scripts/gate.sh allow-commit      # after human picks 통과 (not a chat menu label)
./scripts/gate.sh next-phase
./scripts/gate.sh off               # Small work
```

## Agent rules

- Never edit `.cursor/gate.json` directly (Write/StrReplace/Delete or shell redirect).
- Mutating `gate.sh` only after explicit human choice this turn (AskQuestion
  answer, numbered reply, or human already ran the CLI).
- Do not advance on vague “proceed / approve somehow” without a clear selection.
- Never offer a chat option whose label is about unlocking or making a git commit.
- If blocked by hooks, re-offer AskQuestion (or text menu) or show the equivalent
  `./scripts/gate.sh` line.
