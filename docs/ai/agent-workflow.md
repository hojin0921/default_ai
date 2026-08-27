# AI Agent Workflow Guide

**사람용** 운영 가이드. AI 강제 규칙은 `AGENTS.md` / `.cursor/rules/`.
템플릿 구조는 `TEMPLATE.md`.

목표는 Agent를 많이 쓰는 것이 아니라,
**AI가 잘하는 일 ↔ 사람이 판단할 일**을 나누는 것이다.

## 6축

| 축 | 목적 |
|----|------|
| Rules | AI가 지킬 원칙 (`.cursor/rules/`) |
| Skills | 킥오프·Phase·gate 절차 (`.cursor/skills/` · `.claude/skills/` · `.agents/skills/`) |
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
| 결정 지점 선택 UI 제시 (`AskQuestion` 등 가능하면, 없으면 번호 텍스트) | 채팅에서 선택 (또는 동등 터미널 명령) |

## 역할 Skill (시니어 관점)

한 **채팅**을 쓰되, 단계가 되면 오케스트레이터(`project-kickoff` / `delivery-phase` / `phase-gate`)가 해당 **전문 에이전트**를 띄운다.  
역할 Skill(`senior-*`)은 Quality bar다. 기획·디자인·개발·QA **본문은 그 에이전트가 쓴다**. 오케스트레이터가 Skill만 바꿔 본문을 쓰는 것은 실패. Marketplace 다중 봇은 아니다. 합의: `.cursor/plans/specialist-agents-design.md`.

| Skill | 한글 | 주 관점 | 주 산출물 |
|-------|------|---------|-----------|
| `senior-architect` | 시니어 설계 | 아키텍처·경계·데이터·보안·확장 | 구조 메모, ADR 초안, 영향 범위 |
| `senior-pm` | 시니어 기획 | 요구·우선순위·범위·수락 기준 | Phase 목표, In/Out, 수락 기준 |
| `senior-design` | 시니어 디자인 | 시각·레이아웃·UX·카피·접근성 | 시각 스펙(Figma 또는 레이아웃·타이포·색), 화면 흐름, 카피 |
| `senior-dev` | 시니어 개발 | 구현·패턴·최소 변경·테스트 가능성 | 코드, 구현 상세 Plan |
| `senior-qa` | 시니어 QA | 검증·회귀·User Test Guide·리스크 | 테스트 계획, UTG, 버그 리포트 |

### Delivery 6단계 ↔ 띄울 에이전트

| 단계 | 전문 에이전트 |
|------|----------------|
| 1 Explore | 설계 |
| 2 Document | 설계 또는 기획 (문서 성격) |
| 3 Plan | 기획 → (UI면) 디자인 |
| 4 Implement | 개발 (디자인 스펙 준수) |
| 5 Verify | QA |
| 6 Review | QA → 설계 |

킥오프: K1 **기획**, K2 **기획 → 설계 → (UI면) 디자인**, K3 **기획 → 설계**, K4 **기획 → 설계**.  
오케스트레이터 응답에 지금 단계·띄운 에이전트를 밝힌다. 전문 에이전트는 `역할: 시니어 ○○`과 해당 Skill **Quality bar**를 충족한다.

### 명시 호출 우선

사용자가 “시니어 QA로만 …”, “시니어 디자인 관점으로 …”처럼 **역할을 지정**하면 오케스트레이터는 **그 전문 에이전트만** 띄운다.  
지정이 없으면 위 표 / 킥오프 매핑을 쓴다. Small·Medium에도 동일.  
사람용 예시·FAQ: [`guide.md`](../../guide.md) §2-3 (프로토콜 파일은 Implement에서 맞춤).

목록·트리거: `.cursor/skills/README.md`. 합의된 설계: `.cursor/plans/specialist-agents-design.md`.

## 계획의 층

| 층 | 내용 | 시점 |
|----|------|------|
| 전체 설계 | 문제·사용자·범위·구조 (`*-design.md` → 합의 후 docs) | 킥오프 K2–K3 |
| Phase Plan | 필수 기능을 Delivery Phase 1…N으로 분할 | 킥오프 K4 |
| Phase 상세 Plan | 해당 Phase를 **어떻게** 구현할지 (6단계 중 3번) | 각 Phase |

결정: [`docs/decisions/001-kickoff-design-first.md`](../decisions/001-kickoff-design-first.md).

## 표준 흐름

```
킥오프:
  K1 질문 라운드 → K2 전체 설계 초안·합의 → K3 docs 문서화
  → K4 Phase Plan Draft → Human Review
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
| Large / 킥오프 | K1–K4 후 Phase Plan 승인, **Phase마다 6단계** |

### Phase 0 vs Delivery Phase vs 킥오프

| 이름 | 의미 |
|------|------|
| 킥오프 K1–K4 | 제품을 만들겠다는 설명으로 시작. 질문·설계 합의·docs·Phase Plan |
| Phase 0 | 제품 없이 bootstrap / 템플릿 docs만 요청할 때 |
| Phase 1…N | 기능 단위 Delivery. 진행 시 6단계 필수. Phase 1 Document는 K3 이후 **변경분** |

## Phase Gate (채팅 선택 기본 / 터미널 동등)

클론 후 한 번:

```bash
./scripts/install-hooks.sh
```

전진 채널: **채팅 선택(구조화 질문 UI가 있으면 카드, 없으면 한글 번호) → AI가 `./scripts/gate.sh` 대행**, 또는 사람이 같은 명령을 터미널에서 실행.  
`gate.json` 직접 수정은 금지. 선택 없이 게이트를 전진시키지 않는다.

버튼 UI가 안 보이면 Agent 모델을 Composer / Claude / GPT 등으로 바꾸거나, 번호 `1`/`2`/`3`으로 고른다.

### 채팅 메뉴 예 (한글 · AskQuestion 라벨 / 번호 공통)

**K1 질문**

한 메시지에 질문 **하나**. 「제안해」 옵션. 답을 받은 뒤 다음 질문. 목록 덤프 금지.  
흐린 답은 같은 주제로 후속(최대 2). 체크리스트(누구 / 성공 / 지금·나중 / 화면 / 빈·에러 / 데이터 / Out)를 메운 뒤에만 이해 요약.  
프론트·백·DB 언어는 여기가 아니라 **구현 직전** 번호 선택.

**K1 질문 라운드 후 (이해 요약)**

채팅 **안의** 한눈 그림.  
AskQuestion: `바로 위 한눈 그림(이 답변에 그린 Mermaid)을 보신 뒤, 전체 설계 초안으로 갈까요?`

1. 이 이해로 전체 설계 초안을 작성해 주세요  
2. 더 질문하거나 이해를 수정해 주세요  
3. 지금은 보류할게요  

**K2 전체 설계 초안 후**

채팅 안 한눈 그림 + **지금 볼 곳** (에디터에서 `.cursor/plans/<이름>-design.md` 열기, Cursor는 `Cmd+P`).  
AskQuestion: `바로 위 한눈 그림(이 답변에 그린 Mermaid)과, 에디터에서 .cursor/plans/<이름>-design.md 를 연 뒤 어떻게 할까요?`

1. 이 전체 설계를 합의하고, 이제 문서화해 주세요 (`approve-design`)  
2. 설계 내용을 수정해 주세요 (문서화는 아직 하지 않음)  
3. 지금은 보류할게요  

**K3 docs 문서화 후**

합의된 K2 그림(채팅 안)과 **지금 볼 곳** (`docs/product.md` 등, 에디터에서 열기).  
AskQuestion: `바로 위 한눈 그림(이 답변에 그린 Mermaid)과, 에디터에서 docs/product.md 를 연 뒤 어떻게 할까요?`

1. 문서를 확인했습니다. Phase Plan 초안을 작성해 주세요 (`kickoff phase_plan`)  
2. 문서를 수정해 주세요  
3. 지금은 보류할게요  

**K4 전체 개발 계획(Draft) 후**

채팅 **안**의 **Phase 한눈 그림**과 **지금 볼 곳** (`.cursor/plans/<이름>.md`, Cursor `Cmd+P`).  
AskQuestion: `바로 위 한눈 그림(이 답변에 그린 Mermaid)과, 에디터에서 .cursor/plans/<이름>.md 를 연 뒤 어떻게 할까요?`

1. 이 전체 계획을 승인하고, Phase 1의 1단계(코드 없이 이해하기)부터 진행해 주세요 (`approve-plan`)  
2. 계획 내용을 수정해 주세요 (지금은 승인하지 않음)  
3. 지금은 보류할게요. 나중에 이어갈게요  

**이 Phase 상세 구현 계획 후**

채팅 **안**의 **이 Phase 한눈 그림**과 **지금 볼 곳**.  
AskQuestion: `바로 위 한눈 그림(이 답변에 그린 Mermaid)과, 에디터에서 <Plan 경로> 를 연 뒤 어떻게 할까요?`

1. 이 상세 계획을 승인하고, 이제 구현해 주세요 (`advance implement`)  
   Stack이 미정이면 코드를 쓰기 전에 프론트 → 백엔드 → DB를 **설계·Constraints에 맞는 후보 목록**으로 하나씩 고른다.  
2. 상세 계획을 수정해 주세요 (구현은 아직 하지 않음)  
3. 지금은 보류할게요  

**검증·리뷰 후 (사용자 테스트까지 한 뒤)**

채팅에 **직접 확인 가이드**(실행 / 확인 / 기대 / 실패 시)를 먼저 넣는다.  
마지막 Phase면 **실행 가이드**(준비 / 실행 / 접속)와 **역할 기여**(역할 / 만든 것 / 어떻게 쓰이는지)를 그 앞에 넣는다.  
AskQuestion: `Phase N을 직접 플레이해 보신 결과는 어떤가요?`  
(화면이 없으면 `직접 확인해 보신 결과는 어떤가요?`)

메뉴 라벨에 커밋을 넣지 않는다. `git commit`은 사람이 직접 한다.

1. 직접 확인해 보니 통과예요  
2. 아직 문제 있어요. 같은 Phase에서 고치고 검증을 다시 해 주세요 (같은 메시지에 수정 내용을 이어서 적어도 됨)  
3. 이 Phase는 통과. 다음 Phase로 가고, 지금은 조사만 해 주세요  
   (마지막 Phase: 이 Phase는 통과. 전체 개발을 마무리해 주세요)

1번 → `allow-commit`(잠금만). 3번 → `next-phase`(이미 연 잠금은 유지). 마지막 Phase 3번은 `next-phase` 없음. 메뉴 라벨에는 커밋을 쓰지 않는다.

메뉴에서 수정을 고를 때는 선택 후(또는 번호 `2`와 함께) 수정 프롬프트를 적는다. 수정 후 AI는 선택 UI를 다시 낸다.

### 동등 터미널

| 상황 | 명령 |
|------|------|
| Large 리셋 (설계 미합의) | `./scripts/gate.sh on` |
| 전체 설계 합의 | `./scripts/gate.sh approve-design` |
| Phase Plan 단계로 | `./scripts/gate.sh kickoff phase_plan` |
| 전체 Plan 승인 (`design_approved` 필요) | `./scripts/gate.sh approve-plan` |
| 단계 전진 | `./scripts/gate.sh advance implement` (등) |
| 커밋 잠금 해제 (채팅 메뉴 라벨 없음) | `./scripts/gate.sh allow-commit` |
| 다음 Phase | `./scripts/gate.sh next-phase` |
| Small로 해제 | `./scripts/gate.sh off` |

강제 검사 원천은 Plan Status가 아니라 `.cursor/gate.json`.

## 프로젝트 킥오프

Agent Skill: `project-kickoff` (자동 또는 명시).  
바로 Phase Plan을 쓰지 않는다. K1 질문 → K2 설계 합의 → K3 docs → K4 Phase Plan.  
K1 첫 응답에 `guide.md` §3-0 시작 가이드. 설계·기획 단계마다 한눈 그림.

```text
코드 작성하지 말고, 아래 프로젝트 킥오프를 K1부터 진행해.
지금은 질문만. Phase Plan·docs 본문·구현은 하지 마.

## 프로젝트
<!-- 무엇을 만드는지. 비어 있으면 질문으로 채움 -->

## 꼭 들어가야 할 기능
-

## 있으면 좋은 기능 (나중 Phase 가능)
-

## 제약
<!-- 스택, 기한, 플랫폼 등. 없으면 생략 -->
```

K4 Phase Plan 승인 후 **Phase 1을 6단계로** (한 번에 구현 시키지 말 것).  
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
이해한 내용을 한눈 그림(Mermaid)으로도 보여 줘.
```

**2. Document**

```text
이해한 내용을 문서화해. 관련 docs/README만. 추측으로 TODO 채우지 마.
흐름이 바뀌었으면 한눈 그림도 문서와 채팅에 넣어 줘.
```

**3. Plan**

```text
이 기능을 어떻게 구현할지 계획해.
변경 파일·순서·AI Verify·User Test Guide 초안.
이 Phase 작업 순서 한눈 그림(Mermaid)과 지금 볼 곳(경로·에디터에서 여는 법)을 채팅에 넣고, 승인 전 구현 금지.
```

**4. Implement**

```text
좋아. 이 계획대로 구현해. 이 Phase 범위 밖·다음 Phase 금지.
실행 가능하면 실행 가이드(준비·실행·접속)도 줘.
```

**5. Verify**

```text
테스트하고 검증해. AI 결과와 내가 따라 할 직접 확인 가이드(실행·확인·기대)를 줘.
마지막 Phase면 실행 가이드(어떻게 켜는지)와 역할 기여(누가 무엇을·어디에 쓰이는지)도 앞에 줘.
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

제품 설명 없이 bootstrap / 템플릿 docs만 요청할 때만.
제품을 만들겠다고 하면 킥오프 K1부터 (Phase 0으로 가지 않음).
일반 Small은 Docs TODO로 막지 않는다. 킥오프 K3·Delivery Document(2단계)와 혼동하지 않는다.

```text
Phase 0부터. 코드 수정 금지.
docs 초안 + README 개요. 필요 시 전용 rules.
제품 아이디어가 있으면 킥오프 K1(질문)부터.
```

## Anti-patterns

- 프로젝트 설명만 받고 질문·설계 합의 없이 바로 Phase Plan
- 전체 Plan만 승인받고 Phase 1에서 Explore/Document/Plan 없이 바로 구현
- Phase 6단계 중 일부를 건너뜀
- 사용자 검수 전 다음 Phase Explore 시작
- 직접 확인 가이드 없이 “직접 플레이해 보세요 / 테스트해달라”만 요청
- 실행 가능한데 실행 가이드(켜는 법) 없이 “구현 완료”만 보고
- 마지막 Phase인데 역할 기여(누가 무엇을) 없이 마무리
- 시니어 역할인데 Quality bar를 무시하고 형용사·한 줄 요약으로 단계를 끝냄
- 설계·기획 단계(K1–K4, Explore/Document/Plan)인데 한눈 그림 없이 승인·다음을 요청
- K1에서 질문 여러 개를 한 메시지에 나열
- 한눈 그림을 보라고 하면서 그 답변에 Mermaid(또는 글 흐름)를 안 그림
- 테스트 삭제로 통과
- `.env` 실제 값을 채팅에 첨부
