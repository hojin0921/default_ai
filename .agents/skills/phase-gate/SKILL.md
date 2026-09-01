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
| `explore_approved` | **senior-architect** Explore approved (this Delivery Phase) |
| `document_approved` | Document step approved (this Phase) |
| `plan_body_approved` | **senior-pm** Plan body approved (this Phase) |
| `phase_has_ui` | Current Delivery Phase includes UI (`phase-ui true`) |
| `design_spec_approved` | **senior-design** visual spec approved (UI Phase) |
| `verify_approved` | **senior-qa** Verify approved (this Phase) |
| `phase` | Current Delivery Phase number |
| `step` | explore\|document\|plan\|implement\|verify\|review\|human_verify |
| `kickoff_step` | discover\|design\|docs\|phase_plan\|done |
| `allow_commit` | git commit allowed |

## Gate CLI (OS)

Run the same commands on every OS; only the wrapper differs.

| OS | Wrapper | Example |
|----|---------|---------|
| macOS / Linux / Git Bash | `./scripts/gate.sh` | `./scripts/gate.sh status` |
| Windows CMD / PowerShell | `.\scripts\gate.cmd` | `.\scripts\gate.cmd status` |
| Any (Agent on Windows) | `python scripts/_gate_cli.py` | `python scripts/_gate_cli.py approve-plan` |

**Orchestrator on Windows:** use `python scripts/_gate_cli.py <subcommand>` in Shell (PowerShell does not run `./scripts/gate.sh`). Humans may use `gate.cmd` instead.

## Channel (default: chat)

At decision points, **do not** advance the gate or implement until the human
picks an option in **this** turn.

### How to present the choice

1. **Prefer `AskQuestion`** (or the host equivalent, e.g. Claude Code
   `AskUserQuestion`) when available — one single-select question, Korean
   option labels (same wording as below). This may render as a clickable card.
2. **If unavailable**, fall back to a short Korean numbered `1` / `2` / `3`
   list in chat. Do not invent a fake button UI in markdown.
3. After an unambiguous choice, run the matching gate CLI command(s) for that option (one decision per turn; a menu item may bundle a documented set). Use `./scripts/gate.sh` on macOS/Linux, `.\scripts\gate.cmd` on Windows, or `python scripts/_gate_cli.py` everywhere (required for Agent on Windows). Then run `status` and report briefly.
4. If the choice is unclear, ask again — do not run mutating `gate.sh`.
5. For K1 (after 이해 요약), K2/K3/K4, Phase Explore/Document, and Phase detail Plan: the **same reply** must contain a fenced ```mermaid block and a `글 흐름: … → …` line **above** AskQuestion.  
   Never AskQuestion about a picture that is not in this message.  
   K2/K3/K4 and detail Plan also include **지금 볼 곳**. Files: open the path in the editor (Cursor: `Cmd+P` / `Ctrl+P`).  
   Prompt wording: 바로 위 한눈 그림(이 답변에 그린 Mermaid와 글 흐름). Name the path when there is a file.
6. After Verify, the chat body must include **직접 확인 가이드** before the choice UI. Last Phase: **실행 가이드** then **역할 기여** before that.

Humans may run the same CLI themselves (equivalent).

Spawned specialists (`senior-*` agents) **must not** run mutating `gate.sh`. Only the orchestrator, after an explicit human choice this turn.

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

**After Delivery Explore (Phase N · step explore)**

Must show **senior-architect** output + `역할: 시니어 설계` + 한눈 그림 in this reply.  
AskQuestion: `바로 위 한눈 그림(이 답변에 그린 Mermaid)을 보신 뒤, 다음으로 어떻게 할까요?`

1. Explore를 승인하고 Document(문서화)로 진행해 주세요  
   → `./scripts/gate.sh approve-explore` then `./scripts/gate.sh advance document`  
2. Explore 내용을 수정해 주세요  
3. 지금은 보류할게요  

**After Delivery Document (step document)**

1. Document를 승인하고 Plan(상세 계획)으로 진행해 주세요  
   → `./scripts/gate.sh approve-document` then `./scripts/gate.sh advance plan`  
2. Document를 수정해 주세요  
3. 지금은 보류할게요  

**After Phase detail Plan (step plan)**

Chat must include **senior-pm** Plan + (if UI) **senior-design** spec + 한눈 그림 + **지금 볼 곳**.  
AskQuestion: `바로 위 한눈 그림(이 답변에 그린 Mermaid)과, 에디터에서 <Plan 경로> 를 연 뒤 어떻게 할까요?`

1. 이 상세 계획을 승인하고, 이제 구현해 주세요  
   → `./scripts/gate.sh approve-plan-body`  
   → UI Phase: `./scripts/gate.sh approve-design-spec` (after `phase-ui true` + design spec in reply)  
   → `./scripts/gate.sh advance implement`  
   → **Stack pick** if 미정, then **`senior-dev`** only  
2. 상세 계획을 수정해 주세요 (구현은 아직 하지 않음)  
3. 지금은 보류할게요  

**After Implement (optional advance to Verify)**

When Implement work is done and human agrees to verify:  
→ `./scripts/gate.sh advance verify` then launch **senior-qa**

**After Verify / Review (and human user test)**

Chat must include **직접 확인 가이드** (실행 / 확인 / 기대 / 실패 시) before the menu.  
If this is the **last** Phase in the Plan, also include **실행 가이드** (준비 / 실행 / 접속) and **역할 기여** (역할 / 만든 것 / 어떻게 쓰이는지) *before* 직접 확인 가이드.  
AskQuestion prompt (N = `gate.json` `phase`): `Phase N을 직접 플레이해 보신 결과는 어떤가요?`  
Protocol/docs-only: `Phase N을 직접 확인해 보신 결과는 어떤가요?`

Do **not** put 커밋 / `git commit` / `allow-commit` in option labels. Humans commit themselves.

1. 직접 확인해 보니 통과예요  
   → `./scripts/gate.sh approve-verify` then `./scripts/gate.sh allow-commit` (unlocks hook only; do not `git commit`)  
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

**macOS / Linux / Git Bash**

```bash
./scripts/install-hooks.sh          # once per clone
./scripts/gate.sh status
./scripts/gate.sh on                # Large reset (discover, design not approved)
./scripts/gate.sh approve-design
./scripts/gate.sh kickoff phase_plan
./scripts/gate.sh approve-plan
./scripts/gate.sh approve-explore
./scripts/gate.sh approve-document
./scripts/gate.sh approve-plan-body
./scripts/gate.sh phase-ui true|false
./scripts/gate.sh approve-design-spec
./scripts/gate.sh advance document|plan|implement|verify|review
./scripts/gate.sh approve-verify
./scripts/gate.sh allow-commit
./scripts/gate.sh next-phase
./scripts/gate.sh off
```

**Windows (CMD / PowerShell)** — same subcommands, different wrapper:

```bat
scripts\install-hooks.cmd
scripts\gate.cmd status
scripts\gate.cmd on
REM … (replace gate.sh with gate.cmd)
```

**Cross-platform (Agent on Windows, or any OS)**

```bash
python scripts/_gate_cli.py status
python scripts/_gate_cli.py approve-plan
# … same subcommands as gate.sh
```

## Agent rules

- Never edit `.cursor/gate.json` directly (Write/StrReplace/Delete or shell redirect).
- Mutating `gate.sh` only after explicit human choice this turn (AskQuestion
  answer, numbered reply, or human already ran the CLI).
- Do not advance on vague “proceed / approve somehow” without a clear selection.
- Never offer a chat option whose label is about unlocking or making a git commit.
- If blocked by hooks, re-offer AskQuestion (or text menu) or show the equivalent
  `./scripts/gate.sh` line.
