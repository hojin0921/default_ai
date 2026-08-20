# Plan: 역할별 시니어 에이전트 (Skills)

## Goal

프로그램(제품) 만들 때 Phase·6단계마다 **역할이 다른 시니어 에이전트 Skill**을 쓰게 한다.  
사람은 한 Cursor Agent 채팅을 쓰되, 단계에 맞는 Skill이 자동/명시로 적용되어 관점·산출물이 갈라지게 한다.

## Scope

- In:
  - 역할 Skill 추가 (시니어 설계 / 기획 / 디자인 / 개발 / QA)
  - 기존 `delivery-phase` · `project-kickoff` · `phase-gate`와 **매핑**
  - `guide.md` / rules / skills README에 “어느 단계에 어느 역할” 표기
  - 선택 UI·게이트 흐름은 **유지** (채팅 선택 → `gate.sh`)
- Out:
  - Cursor Marketplace 다중 봇 / 별도 프로세스 오케스트레이터
  - 앱 `src/` 제품 기능 구현
  - 모델(Grok vs Claude) 강제 고정
  - 역할마다 완전히 다른 git 워크트리 강제

## Task Size

**Large**

## Must-have Features

| Feature | Phase | Notes |
|---------|-------|-------|
| 역할 Skill 5종 (설계·기획·디자인·개발·QA) | 1 | 각 SKILL.md에 관점·산출물·금지사항 |
| 6단계 ↔ 역할 매핑 | 1 | Explore~Review에 primary(+optional) |
| kickoff / delivery-phase가 역할 Skill을 호출·전환 안내 | 2 | “지금은 OO 시니어 관점으로” |
| guide·workflow·README에 사람용 설명 | 2 | 언제 어떤 역할인지 |
| (선택) Small/Medium에서도 역할 명시 요청 가능 | 3 | 예: “디자인 시니어로 리뷰해” |

## 역할 정의 (초안)

| 역할 Skill | 한글 | 주 관점 | 주 산출물 |
|------------|------|---------|-----------|
| `senior-architect` | 시니어 설계 | 아키텍처·경계·데이터·보안·확장 | 구조 메모, ADR 초안, 영향 범위 |
| `senior-pm` | 시니어 기획 | 요구·우선순위·범위·수락 기준 | Phase 목표, In/Out, User Story 수준 |
| `senior-design` | 시니어 디자인 | UX/UI·정보구조·카피·접근성 | 화면 흐름, UI 가이드, 카피 톤 |
| `senior-dev` | 시니어 개발 | 구현·패턴·최소 변경·테스트 가능성 | 코드, 구현 Plan 상세 |
| `senior-qa` | 시니어 QA | 검증·회귀·User Test Guide·리스크 | 테스트 계획, UTG, 버그 리포트 |

## 6단계 ↔ 역할 매핑 (초안)

| Delivery 단계 | Primary | Optional |
|---------------|---------|----------|
| 1 Explore | 설계 (+ 기획) | — |
| 2 Document | 설계 / 기획 (문서 성격에 따라) | 디자인(UX 문서 시) |
| 3 Plan | 기획 + 설계 (+ 디자인 if UI) | 개발(실현 가능성) |
| 4 Implement | 개발 | 디자인(UI 구현 시) |
| 5 Verify | QA (+ 개발 수정) | — |
| 6 Review | QA + 설계 (품질·범위) | 기획(요구 누락) |

킥오프 전체 Plan: **기획 + 설계** 주도로 Draft → 사람 승인.

## Delivery Phases

### Phase 1 — 역할 Skill 골격 + 매핑

- Goal: 5개 역할 Skill 추가, 단계↔역할 표를 rules/delivery-phase에 연결
- In: `.cursor/skills/senior-*/SKILL.md`, skills README, `01-agent-workflow.mdc` 매핑 절
- Out: guide 전면 개편, 오케스트레이터 스크립트
- 6-step status:
  - [x] 1 Explore
  - [x] 2 Document
  - [x] 3 Plan (상세) → Human approve
  - [x] 4 Implement
  - [x] 5 Verify (AI + User Test Guide)
  - [x] 6 Review → Human Verify
- Docs to update: `docs/ai/agent-workflow.md` (역할 표만 · Document에서 완료), `.cursor/skills/README.md` (Document에서 초안 · Implement 시 “구현 전” 문구 제거)

#### Phase 1 상세 Plan (Implement 순서)

**공통 Skill 본문 골격** (5개 동일 구조, 내용만 역할별):

```text
---
name: senior-…
description: (영문·트리거 좁게 · max 1024)
---
# 시니어 ○○
## When
## Stance (관점)
## Outputs (산출물)
## Do / Don't
## With delivery-phase
- 응답 첫 줄: `역할: 시니어 ○○`
- 게이트·6단계 절차는 delivery-phase / phase-gate에 맡김
```

`disable-model-invocation`은 **넣지 않음** (기존 워크플로 Skill과 동일, 자동 선택 가능).

| # | 파일 | 작업 | 비고 |
|---|------|------|------|
| 1 | `senior-architect/SKILL.md` | 신규 | Explore·구조·보안·blast radius |
| 2 | `senior-pm/SKILL.md` | 신규 | 범위·우선순위·수락 기준 |
| 3 | `senior-design/SKILL.md` | 신규 | UX/UI·카피·접근성 · Figma MCP는 선택 |
| 4 | `senior-dev/SKILL.md` | 신규 | 최소 변경·기존 패턴·테스트 가능 구현 |
| 5 | `senior-qa/SKILL.md` | 신규 | Verify·UTG·회귀·리스크 |
| 6 | `delivery-phase/SKILL.md` | 수정 | 단계→primary/optional 표 + “해당 Skill 읽고 따르라” + 역할 한 줄 고지 |
| 7 | `project-kickoff/SKILL.md` | 수정 | 기획+설계 primary · senior-pm/architect 참조 |
| 8 | `01-agent-workflow.mdc` | 수정 | 「역할 Skill」절 + Skills 목록에 senior-* |
| 9 | `AGENTS.md` | 수정 | Skills 한 줄에 역할 Skill 언급 |
| 10 | `.cursor/skills/README.md` | 수정 | “Implement 전 없을 수 있음” 문구 제거·경로 확인 |

**하지 않음 (Phase 1):** `guide.md` 전면, TEMPLATE 대개정, gate/hooks 변경, `src/`, Phase 2·3.

**description 작성 원칙:**  
- 언제 쓸지(단계·키워드)를 넣고  
- 워크플로 Skill과 겹치지 않게 (“gate.sh 실행”은 phase-gate 전용)  
- 한글 트리거 예: “시니어 설계”, “아키텍처 리뷰” 등 description에 포함 가능

**AI Verify (Implement 후):**

- [ ] 5개 `SKILL.md` 존재, frontmatter `name` 일치  
- [ ] `delivery-phase`에 6단계 매핑 표 있음  
- [ ] `project-kickoff`에 기획+설계 명시  
- [ ] rules/AGENTS에 역할 언급  
- [ ] README에 역할 5종 경로 표기  

**User Test Guide (초안):**

- Setup: 이 템플릿 폴더 · Agent Chat · (가능하면 Composer/Claude로 AskQuestion)  
- Check: `코드 작성하지 말고 Phase Explore만. 시니어 설계 관점으로`  
- Expected: 응답 첫 줄 근처에 `역할: 시니어 설계`, 구조/영향 범위 중심, 코드 변경 없음  
- If fails: 역할 표기 유무, 적용된 Skill 이름, 응답이 개발/구현으로 새는지  

- Human Verify: [x] 통과

### Phase 2 — 가이드·전환 UX

- Goal: 사람이 읽기 쉽게 guide에 역할 설명, 단계 전환 시 “지금 역할” 고지 + 선택 UI 유지
- In / Out: guide·TEMPLATE·agent-workflow 갱신 / 새 게이트 필드 추가 금지
- 6-step status:
  - [x] 1 Explore
  - [x] 2 Document
  - [x] 3 Plan (상세) → Human approve
  - [x] 4 Implement
  - [x] 5 Verify (AI + User Test Guide)
  - [x] 6 Review → Human Verify
- Docs: `guide.md`, `TEMPLATE.md`, `docs/ai/agent-workflow.md` (**Document에서 대부분 완료**)
- Human Verify: [x] 통과

#### Phase 2 상세 Plan (Implement 순서)

Document에서 사람용 역할 설명은 이미 들어갔다. Implement는 **남은 연결·일관성**만 최소로 한다.

| # | 파일 | 작업 | 비고 |
|---|------|------|------|
| 1 | `.cursor/skills/delivery-phase/SKILL.md` | `After each step`에 “보고에 `역할: 시니어 ○○` 포함”을 **한 줄 더 명시** | Role map·시작 고지는 이미 있음 |
| 2 | `README.md` | 하단 HTML 주석에 `guide.md` §2-2 · `senior-*` 언급 | 템플릿 복사용 힌트 |
| 3 | `CLAUDE.md` | Skills 줄에 `senior-*` 한 줄 | AGENTS와 정합 |
| 4 | `docs/README.md` | Skills 축에 역할 Skill 한 줄(있으면) | 최소 |
| 5 | `.cursor/plans/senior-role-agents.md` | Phase 2 체크·Status만 갱신 | 구현 산출 아님 |

**하지 않음**
- `guide.md` / `TEMPLATE.md` 재작성 (Document 완료분 유지, 오타만 고침)
- 게이트/훅 변경, 역할 Skill 본문 재작성, Phase 3 FAQ
- `_verify_phase_gate.py` 리셋 문제 수정 (별도 Small/Phase 3 후보로 남김)

**AI Verify**
- [ ] `guide.md` §2-2에 5역할 + 6단계 표 존재
- [ ] `TEMPLATE.md`에 `senior-*` 언급
- [ ] `delivery-phase` After each step에 역할 고지
- [ ] README/CLAUDE에 senior 힌트
- [ ] §4 선택 UI 문구와 역할 절이 충돌하지 않음

**User Test Guide (초안)**
- Setup: `guide.md`만 열고 읽기 · (선택) 새 Agent Chat
- Check: §2-2에서 시니어 5종·6단계 주 역할을 찾을 수 있는지 · Explore 요청 시 `역할: 시니어 설계`가 보이는지
- Expected: guide만으로 “한 Agent + 역할 Skill”을 이해 가능
- If fails: 어느 절이 빠졌는지 / 역할 표기 유무

### Phase 3 — 명시 호출·Small/Medium 확장 (선택)

- Goal: “시니어 QA로만 리뷰해” 같은 명시 요청 지원, 불필요 역할 스킵 규칙
- In: skill When/description 보강, delivery-phase 오버라이드 절, guide FAQ(§2-3 · Document 완료), rules/AGENTS 한 줄
- Out: 자동 multi-agent 병렬, 게이트 스키마 변경, `_verify_phase_gate.py` 리셋 수정
- 6-step status:
  - [x] 1 Explore
  - [x] 2 Document
  - [x] 3 Plan (상세) → Human approve
  - [x] 4 Implement
  - [x] 5 Verify (AI + User Test Guide)
  - [x] 6 Review → Human Verify
- Docs: `guide.md` §2-3, `docs/ai/agent-workflow.md`, skills README (**Document 완료**)
- Human Verify: [x] 통과

#### Phase 3 상세 Plan (Implement 순서)

Document에서 사람용 §2-3·FAQ는 이미 반영됨. Implement는 **Agent가 따르게** 규칙·Skill만 맞춘다.

| # | 파일 | 작업 |
|---|------|------|
| 1 | `delivery-phase/SKILL.md` | 「Explicit role override」: 사용자 명시 역할 > Role map; 지정 역할만; `역할:` 한 줄; Large 절차·게이트는 유지 |
| 2 | `senior-architect/SKILL.md` | When에 “명시 호출 시 이 역할만 / 타 역할 스킵” + description에 트리거 유지·보강 |
| 3 | `senior-pm/SKILL.md` | 동일 |
| 4 | `senior-design/SKILL.md` | 동일 |
| 5 | `senior-dev/SKILL.md` | 동일 |
| 6 | `senior-qa/SKILL.md` | 동일 (“시니어 QA로만 리뷰” 명시) |
| 7 | `01-agent-workflow.mdc` | 역할 절에 “사용자 명시 호출 우선” 한 줄 |
| 8 | `AGENTS.md` | 동일 한 줄 |
| 9 | `project-kickoff/SKILL.md` | (최소) 명시 호출 시 해당 역할 우선 — 킥오프 기본은 기획+설계 유지 |

**공통 문구 (각 senior Skill When에 추가):**

```text
If the user explicitly names this role (e.g. "시니어 ○○로만"), follow only this
skill for that turn and skip other senior role stances unless they ask for a sequence.
```

**하지 않음:** guide 재작성, 훅/게이트, verify 스크립트 리셋 수정, 새 Skill 추가.

**AI Verify**
- [ ] delivery-phase에 override 절
- [ ] senior-* 5개 When에 명시 호출 문장
- [ ] rules + AGENTS에 우선 규칙
- [ ] guide §2-3과 모순 없음

**User Test Guide (초안)**
- Setup: 게이트 `off` 또는 아무 Chat
- Check: `시니어 QA로만 리뷰해. 구현하지 마. guide.md §2-3만 기준으로 짧게.`
- Expected: `역할: 시니어 QA`, 구현/설계 장황함 없음
- If fails: 역할 표기 · 다른 역할로 새는지 · 모델명

## Changes (전체 요약)

| File | Change | Why | Phase |
|------|--------|-----|-------|
| `.cursor/skills/senior-*/SKILL.md` ×5 | 역할 Skill 신규 | 파트별 관점 | 1 |
| `delivery-phase` / `project-kickoff` | 단계별 역할 전환 | 한 Agent·여러 역할 | 1–2 |
| `01-agent-workflow.mdc` / `AGENTS.md` | 매핑·최소 규칙 | Agent가 따르게 | 1 |
| `guide.md` 등 | 사람용 설명 | 사용법 | 2 |

## Steps

1. 전체 Plan 승인
2. Phase 1: 역할 Skill + 매핑
3. Phase 2: guide·보고 UX
4. (선택) Phase 3: 명시 호출·Small 확장
5. 전체 마무리 Review

## Verification

- [ ] Phase마다 6단계 완료
- [ ] 관련 Skill이 Cursor에 보이고 description이 단계와 맞음
- [ ] User Test Guide 제공 (Phase마다)
- [ ] docs / guide 갱신

## Risks

- Skill이 너무 많으면 Agent가 잘못된 Skill을 고를 수 있음 → description·delivery-phase의 **명시적 primary**로 완화
- “여러 에이전트”처럼 보여도 실제로는 **한 채팅 + Skill 전환**임을 가이드에 명확히 써야 함
- 디자인 Skill이 Figma MCP 등과 겹칠 수 있음 → UI는 텍스트/구조 우선, MCP는 선택

## Human Review

- [ ] 요구사항·범위·Must-have ↔ Phase 매핑 확인
- [ ] 보안·데이터·마이그레이션 위험 확인 (해당 시)
- [ ] 전체 Plan 승인 (Approved 전에 Agent는 Phase 구현 금지)
- [ ] 각 Phase: 상세 Plan 승인 + Human Verify (다음 Phase 전)

## Status

**Done** · Phase 1–3 Human Verify 통과 · allow_commit=true (커밋은 요청 시)

<!-- 강제 검사 진실 원천은 Status가 아니라 .cursor/gate.json (채팅 선택→./scripts/gate.sh) -->
