---
name: phase-gate
description: >-
  Explains the phase gate (.cursor/gate.json and scripts/gate.sh). Prefer
  human chat multiple-choice; Agent may run mutating gate.sh only after an
  explicit choice. Use when the user mentions gate, approve-plan, allow-commit,
  phase enforcement, or commit blocked by phase-gate.
---

# Phase Gate

## Model

Source of truth: `.cursor/gate.json`

| Field | Meaning |
|-------|---------|
| `enabled` | Large enforcement on/off (Small → off) |
| `plan_approved` | Whole plan approved |
| `phase` | Current Delivery Phase number |
| `step` | explore\|document\|plan\|implement\|verify\|review\|human_verify |
| `allow_commit` | git commit allowed |

## Channel (default: chat)

At decision points, present a **numbered menu**. Do not advance the gate or
implement until the human picks an option in **this** turn.

After an unambiguous choice, run the matching `./scripts/gate.sh` command(s)
listed in that menu item (one decision per turn; a menu item may bundle a
documented set such as `on` + `approve-plan`). Then run `./scripts/gate.sh status`
and report briefly.

If the choice is unclear, ask again — do not run mutating `gate.sh`.

Humans may run the same CLI themselves (equivalent).

### Menu examples (present in Korean)

**After whole-plan Draft**

1. 이 전체 계획을 승인하고, Phase 1의 1단계(코드 없이 이해하기)부터 진행해 주세요  
   → `./scripts/gate.sh on` then `approve-plan`, then Phase 1 Explore only  
2. 계획 내용을 수정해 주세요 (지금은 승인하지 않음)  
   — 같은 메시지에 수정할 내용을 이어서 적어도 됨  
3. 지금은 보류할게요. 나중에 이어갈게요  

**After Phase detail Plan**

1. 이 상세 계획을 승인하고, 이제 구현해 주세요  
   → `./scripts/gate.sh advance implement`, then Implement  
2. 상세 계획을 수정해 주세요 (구현은 아직 하지 않음)  
   — 같은 메시지에 수정할 내용을 이어서 적어도 됨  
3. 지금은 보류할게요  

**After Verify / Review (and human user test)**

1. 검수 통과예요. 커밋해도 되게 열어 주세요  
   → `./scripts/gate.sh allow-commit` (commit only if user asks)  
2. 아직 문제 있어요. 같은 Phase에서 고치고 검증을 다시 해 주세요  
   — 같은 메시지에 무엇이 문제인지 / 어떻게 고칠지 이어서 적어도 됨  
3. 이 Phase는 통과. 다음 Phase로 가고, 지금은 조사(Explore)만 해 주세요  
   → `./scripts/gate.sh next-phase`, then Explore only  

When the human picks **2** with extra instructions in the same (or next) message, apply those edits and then re-offer the menu. Do not treat “2” alone as approval.

## Equivalent CLI

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

- Never edit `.cursor/gate.json` directly (Write/StrReplace/Delete or shell redirect).
- Mutating `gate.sh` only after explicit human chat choice this turn (or human already ran it).
- Do not advance on vague “proceed / approve somehow” without a clear menu selection.
- If blocked by hooks, re-offer the chat menu or show the equivalent `./scripts/gate.sh` line.
