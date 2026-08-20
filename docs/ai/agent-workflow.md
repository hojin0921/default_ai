# AI Agent Workflow Guide

**사람용** 운영 가이드. AI 강제 규칙은 `AGENTS.md` / `.cursor/rules/`.
템플릿 구조는 `TEMPLATE.md`.

목표는 Agent를 많이 쓰는 것이 아니라,
**AI가 잘하는 일 ↔ 사람이 판단할 일**을 나누는 것이다.

## 6축

| 축 | 목적 |
|----|------|
| Rules | AI가 지킬 원칙 (`.cursor/rules/`) |
| Skills | 킥오프·Phase·gate 절차 (`.cursor/skills/`) |
| Hooks | 구현/커밋 차단 (`.cursor/hooks.json` + gate) |
| Docs | 프로젝트 지식 |
| Plans | 전체 Plan + Phase 상세 계획 |
| Tests | AI 검증 + 사용자 테스트 |
| Human Review | Plan/단계 승인·사용자 검수 |

## 역할 분담

| AI | 사람 |
|----|------|
| 탐색·문서 초안·계획·구현·자동 테스트·리뷰 초안 | 제품 방향·필수 기능·단계 승인 |
| User Test Guide 작성 · (선택 후) `gate.sh` 대행 | Guide대로 직접 테스트·검수 |
| 결정 지점 선택 UI 제시 (`AskQuestion` 우선, 없으면 번호 텍스트) | 채팅에서 선택 (또는 동등 터미널 명령) |

## 역할 Skill (시니어 관점)

한 Cursor Agent 채팅을 쓰되, Phase·6단계에 맞는 **역할 Skill**로 관점·산출물을 나눈다.  
별도 봇 프로세스나 Marketplace 다중 에이전트가 아니다. 워크플로 Skill(`project-kickoff` / `delivery-phase` / `phase-gate`)이 오케스트레이션하고, 역할 Skill은 관점만 담당한다.

| Skill | 한글 | 주 관점 | 주 산출물 |
|-------|------|---------|-----------|
| `senior-architect` | 시니어 설계 | 아키텍처·경계·데이터·보안·확장 | 구조 메모, ADR 초안, 영향 범위 |
| `senior-pm` | 시니어 기획 | 요구·우선순위·범위·수락 기준 | Phase 목표, In/Out, 수락 기준 |
| `senior-design` | 시니어 디자인 | UX/UI·정보구조·카피·접근성 | 화면 흐름, UI 가이드, 카피 톤 |
| `senior-dev` | 시니어 개발 | 구현·패턴·최소 변경·테스트 가능성 | 코드, 구현 상세 Plan |
| `senior-qa` | 시니어 QA | 검증·회귀·User Test Guide·리스크 | 테스트 계획, UTG, 버그 리포트 |

### Delivery 6단계 ↔ primary 역할

| 단계 | Primary | Optional |
|------|---------|----------|
| 1 Explore | 설계 (+ 기획) | — |
| 2 Document | 설계 / 기획 (문서 성격에 따라) | 디자인(UX 문서 시) |
| 3 Plan | 기획 + 설계 (+ 디자인 if UI) | 개발(실현 가능성) |
| 4 Implement | 개발 | 디자인(UI 구현 시) |
| 5 Verify | QA (+ 개발 수정) | — |
| 6 Review | QA + 설계 | 기획(요구 누락) |

킥오프 전체 Plan Draft는 **기획 + 설계** 주도.  
응답 시작에 `역할: 시니어 ○○`을 한 줄로 밝힌다.

### 명시 호출 우선

사용자가 “시니어 QA로만 …”, “시니어 디자인 관점으로 …”처럼 **역할을 지정**하면 그 Skill이 우선이고, 지정하지 않은 역할 관점은 스킵한다.  
지정이 없으면 Delivery Role map(위 표) / kickoff 기본(기획+설계)을 쓴다. Small·Medium에도 동일.  
사람용 예시·FAQ: [`guide.md`](../../guide.md) §2-3.

목록·트리거: `.cursor/skills/README.md`. 사람용 요약: [`guide.md`](../../guide.md) §2-2. 전체 Plan: `.cursor/plans/senior-role-agents.md`.

## 두 겹의 계획

| 계획 | 내용 |
|------|------|
| 전체 Plan | 필수 기능을 Delivery Phase 1…N으로 분할 (구현 전 Draft) |
| Phase 상세 Plan | 해당 Phase를 **어떻게** 구현할지 (6단계 중 3번) |

## 표준 흐름

```
킥오프: 전체 Plan(Phases) → Human Review
  → Phase N:
      1 Explore → 2 Document → 3 Plan → (승인)
      → 4 Implement → 5 Verify(+User Test Guide) → 6 Review
      → Human Verify
  → 다음 Phase …
```

| 크기 | 흐름 |
|------|------|
| Small | Implement → Verify |
| Medium | Explore → 짧은 Plan → Implement → Verify |
| Large / 킥오프 | 전체 Plan 승인 후, **Phase마다 6단계** |

### Phase 0 vs Delivery Phase

| 이름 | 의미 |
|------|------|
| Phase 0 | bootstrap / 초기 문서화 요청 시 |
| Phase 1…N | 기능 단위 Delivery. 진행 시 6단계 필수 |

## Phase Gate (채팅 선택 기본 / 터미널 동등)

클론 후 한 번:

```bash
./scripts/install-hooks.sh
```

전진 채널: **채팅 선택(`AskQuestion` 버튼 우선, 없으면 한글 번호) → AI가 `./scripts/gate.sh` 대행**, 또는 사람이 같은 명령을 터미널에서 실행.  
`gate.json` 직접 수정은 금지. 선택 없이 게이트를 전진시키지 않는다.

버튼 UI가 안 보이면 Agent 모델을 Composer / Claude / GPT 등으로 바꾸거나, 번호 `1`/`2`/`3`으로 고른다.

### 채팅 메뉴 예 (한글 · AskQuestion 라벨 / 번호 공통)

**전체 개발 계획(Draft) 후**

1. 이 전체 계획을 승인하고, Phase 1의 1단계(코드 없이 이해하기)부터 진행해 주세요 (`on` + `approve-plan`)  
2. 계획 내용을 수정해 주세요 (지금은 승인하지 않음)  
3. 지금은 보류할게요. 나중에 이어갈게요  

**이 Phase 상세 구현 계획 후**

1. 이 상세 계획을 승인하고, 이제 구현해 주세요 (`advance implement`)  
2. 상세 계획을 수정해 주세요 (구현은 아직 하지 않음)  
3. 지금은 보류할게요  

**검증·리뷰 후 (사용자 테스트까지 한 뒤)**

1. 검수 통과예요. 커밋해도 되게 열어 주세요 (`allow-commit`)  
2. 아직 문제 있어요. 같은 Phase에서 고치고 검증을 다시 해 주세요 (같은 메시지에 수정 내용을 이어서 적어도 됨)  
3. 이 Phase는 통과. 다음 Phase로 가고, 지금은 조사만 해 주세요 (`next-phase`)

메뉴에서 수정을 고를 때는 선택 후(또는 번호 `2`와 함께) 수정 프롬프트를 적는다. 수정 후 AI는 선택 UI를 다시 낸다.

### 동등 터미널

| 상황 | 명령 |
|------|------|
| Large 시작 | `./scripts/gate.sh on` |
| 전체 Plan 승인 | `./scripts/gate.sh approve-plan` |
| 단계 전진 | `./scripts/gate.sh advance implement` (등) |
| 커밋 허용 | `./scripts/gate.sh allow-commit` |
| 다음 Phase | `./scripts/gate.sh next-phase` |
| Small로 해제 | `./scripts/gate.sh off` |

강제 검사 원천은 Plan Status가 아니라 `.cursor/gate.json`.

## 프로젝트 킥오프

Agent Skill: `project-kickoff` (자동 또는 명시).

```text
코드 작성하지 말고, 아래 프로젝트의 전체 개발 Plan만 세워줘.
.cursor/plans/에 _template.md 형식으로 Draft.
필수 기능을 Delivery Phase로 나누고, 각 Phase는 6단계
(Explore→Document→Plan→Implement→Verify→Review)로 진행한다고 명시해.
지금은 구현하지 마.

## 프로젝트
<!-- 무엇을 만드는지 -->

## 꼭 들어가야 할 기능
- 
- 

## 있으면 좋은 기능 (나중 Phase 가능)
- 

## 제약
<!-- 스택, 기한, 플랫폼 등. 없으면 생략 -->
```

전체 Plan 승인 후 **Phase 1을 6단계로** (한 번에 구현 시키지 말 것).  
채팅에서 메뉴 `1`(승인)을 고르거나:

```text
전체 Plan 승인. Phase 1부터 6단계로 진행해.
지금은 1단계만: 코드 작성하지 말고 프로젝트를(이 Phase 범위를) 이해해.
```

```text
2단계: 이해한 내용을 문서화해.
```

```text
3단계: 이 Phase 기능을 어떻게 구현할지 상세 계획해. 승인 전 구현 금지.
```

```text
좋아. 이 계획대로 구현해. (4단계)
```

```text
테스트하고 검증해. User Test Guide도 줘. (5단계)
```

```text
다시 리뷰해. (6단계)
```

사용자가 Guide로 직접 테스트한 뒤:

```text
Phase 1 검수 통과. Phase 2를 6단계로 시작해. 지금은 Explore만.
```

문제 시:

```text
Phase N / 단계에서 문제: …
같은 Phase에서 고치고 Verify·User Test Guide·필요 시 Review를 다시 해줘.
```

## Phase 6단계 프롬프트

**1. Explore**

```text
코드 작성하지 말고 프로젝트를 이해해.
(또는: 이 Phase 관련 코드·요구만 조사해. docs 전체는 읽지 마.)
```

**2. Document**

```text
이해한 내용을 문서화해. 관련 docs/README만. 추측으로 TODO 채우지 마.
```

**3. Plan**

```text
이 기능을 어떻게 구현할지 계획해.
변경 파일·순서·AI Verify·User Test Guide 초안. 승인 전 구현 금지.
```

**4. Implement**

```text
좋아. 이 계획대로 구현해. 이 Phase 범위 밖·다음 Phase 금지.
```

**5. Verify**

```text
테스트하고 검증해. 결과와 내가 따라 할 User Test Guide를 줘.
```

**6. Review**

```text
다시 리뷰해. 요구 누락, 버그, 보안, 불필요 변경을 찾아줘.
```

## Context

- ❌ 프로젝트 전체 / docs 전부 읽기
- ✅ 현재 Phase·현재 단계 관련만
- Phase 단위가 끝나면 새 Chat을 고려

## Phase 0 (조건부)

bootstrap 요청, 또는 Docs 비어 있음 + 초기/문서화일 때만.
일반 Small은 Docs TODO로 막지 않는다. Delivery Phase의 Document(2단계)와 혼동하지 않는다.

```text
Phase 0부터. 코드 수정 금지.
docs 초안 + README 개요. 필요 시 전용 rules. 첫 Large면 전체 plan Draft.
```

## Anti-patterns

- 전체 Plan만 승인받고 Phase 1에서 Explore/Document/Plan 없이 바로 구현
- Phase 6단계 중 일부를 건너뜀
- 사용자 검수 전 다음 Phase Explore 시작
- User Test Guide 없이 “테스트해달라”만 요청
- 테스트 삭제로 통과
- `.env` 실제 값을 채팅에 첨부
