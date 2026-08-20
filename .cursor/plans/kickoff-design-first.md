# Plan: 킥오프를 질문 → 전체 설계 합의 → docs → Phase Plan 순으로 바꾸기

## Goal

새 프로젝트(Large) 시작 시 AI가 **바로 Phase 분할 Plan을 쓰지 않고**,  
사람과 묻고 답하며 **전체 설계를 합의**한 뒤, 그 내용을 **docs에 남기고**,  
그다음에야 **Delivery Phase Plan**을 세우도록 템플릿 프로토콜을 바꾼다.

구현(앱 코드)은 이번 작업 범위가 아니다. 대상은 Skills · Rules · Docs · Gate · 사람 가이드다.

## Scope

- In:
  - 킥오프 4단계 절차 (질문 → 설계 합의 → 문서화 → Phase Plan)
  - 사람 승인 지점·선택 UI 문구
  - 관련 Skill / guide / agent-workflow / Plan 템플릿
  - 게이트에 설계 합의 이전 Phase Plan 승인을 막는 **최소 강제**
  - 코드가 없을 때 설계 문서를 채워도 되도록 `documentation.mdc` 예외 명시
- Out:
  - 앱 `src/` 구현
  - Small / Medium 흐름 변경
  - Delivery Phase 6단계 순서 변경 (Explore→Document→Plan→Implement→Verify→Review 유지)
  - Phase 0(bootstrap) 삭제 — 역할만 재정의
  - 별도 봇/멀티에이전트

## Task Size

Small | Medium | **Large**

## Must-have Features

| Feature | Phase | Notes |
|---------|-------|-------|
| 킥오프 질문 라운드 (배치 질문, 바로 Plan 금지) | 1 | Skill이 핵심. 게이트는 “아직 design 전”만 표시 |
| 전체 설계 초안 + 사람 합의 (승인/수정/보류) | 1 | 산출물: `.cursor/plans/<name>-design.md` |
| 합의된 설계를 `docs/`에 문서화 | 1 | `docs/product.md` 신설 + architecture 등 |
| 문서 기준으로 Phase Plan Draft | 1 | 기존 `_template.md` 유지, 작성 시점만 뒤로 |
| 설계 미합의 시 `approve-plan` 불가 | 2 | `design_approved` + `kickoff_step` |
| Phase 1 Document는 기초 docs가 아니라 **변경분** | 1 | 킥오프에서 이미 채웠으므로 |
| 사람 가이드(guide.md 등)와 예시 프롬프트 갱신 | 1–2 | 본문 복붙 없이 흐름만 |

## 권장 목표 흐름 (Large)

```
사용자가 만들고 싶은 프로젝트를 설명
  → K1 질문 라운드     (기획)     코드·Plan·docs 쓰기 금지
  → K2 전체 설계 초안  (기획+설계)  design.md Draft → 사람 합의
  → K3 docs 문서화     (설계/기획) product/architecture 등
  → K4 Phase Plan      (기획+설계) plans/_template.md Draft → 사람 승인
  → Delivery Phase 1…N 기존 6단계 (사람 검수 후 다음 Phase)
```

지금과의 차이: **K1–K3가 생기고**, 지금의 킥오프(바로 Phase Plan)는 **K4로 밀린다**.

## 권장 설계 (이 Plan에서 기본으로 채택)

### 1) 킥오프를 4단계로 쪼갠다 (Delivery 6단계와 이름 섞지 않음)

| 단계 | 역할 | 하는 일 | 하지 않는 일 | 사람 선택 |
|------|------|---------|--------------|-----------|
| **K1 Discover** | 시니어 기획 | 한 번에 3–7개만 질문. 답 듣고 부족하면 한 라운드 더. “모르면 AI 제안” 허용 | Phase Plan, 앱 코드, docs 본문 | 1 이 이해로 전체 설계 초안 작성 / 2 더 질문·수정 / 3 보류 |
| **K2 Design** | 기획 + 설계 (+UI면 디자인) | `.cursor/plans/<short>-design.md` 초안 | Phase 분할 Plan, 앱 코드 | 1 이 전체 설계를 합의하고 문서화로 진행 / 2 설계 수정 / 3 보류 |
| **K3 Docs** | 설계 / 기획 | 합의 내용을 `docs/`에 기록 | Phase Plan, 앱 코드 | 1 문서 확인했고 Phase Plan 초안 작성 / 2 문서 수정 / 3 보류 |
| **K4 Phase Plan** | 기획 + 설계 | 기존과 같이 `.cursor/plans/<short>.md` Draft | 구현 | 1 전체 계획 승인 후 Phase 1 Explore / 2 Plan 수정 / 3 보류 |

질문 체크리스트(한 라운드에 전부 던지지 않음):

- 누구의 어떤 문제를 푸는가
- 꼭 넣을 기능 vs 나중
- 플랫폼·스택·제약
- 로그인/데이터/외부 연동 여부
- 성공 기준(MVP)
- 명시적 Out (하지 말 것)

K2 `*-design.md` 목차(신규 템플릿 `.cursor/plans/_design-template.md`):

- 문제 / 사용자
- Must-have vs Later
- 주요 흐름(저니)
- 시스템 경계·데이터·연동
- UX 개요(화면이 있을 때만)
- 제약·보안·운영
- Out of scope
- 남은 열린 질문

K3에서 채울 docs (코드 없이, **합의된 설계만**):

| 파일 | 내용 |
|------|------|
| `docs/product.md` **(신설)** | 사용자, 문제, 필수 기능, 저니, Out |
| `docs/architecture.md` | 구조·데이터 흐름·경계·연동 (설계 합의분) |
| `docs/security.md` | 모델만. secret 없음 |
| `docs/README.md` | 상태 TODO → 킥오프 반영 |
| 그 외(development/testing/…) | 알 수 없으면 TODO 유지. 추측 금지 |

### 2) 게이트는 최소 강제 (Delivery `step`과 분리)

Delivery `step`(explore…review)은 **Phase 안 6단계 전용**으로 둔다.  
킥오프용 필드를 추가한다.

```json
"kickoff_step": "discover | design | docs | phase_plan | done",
"design_approved": false
```

| 명령 | 의미 |
|------|------|
| `./scripts/gate.sh on` | Large 시작. `kickoff_step=discover`, `design_approved=false`, `plan_approved=false` |
| `./scripts/gate.sh approve-design` **(신규)** | 설계 합의. `design_approved=true`, `kickoff_step=docs` |
| `./scripts/gate.sh kickoff <docs\|phase_plan>` **(신규)** | K3 확인 후 Phase Plan 단계로 |
| `./scripts/gate.sh approve-plan` | **`design_approved`가 true일 때만**. `kickoff_step=done`, Phase 1 `explore` |

강제 범위:

- 앱 코드 쓰기는 지금과 같이 `plan_approved` + implement|verify|review 전 차단
- **docs / `.cursor/plans/` 쓰기는 훅으로 막지 않음** (지금은 이미 허용). 순서는 Skill이 지킴
- `approve-plan`만 설계 합의 전 거절 (에이전트가 K4를 건너뛰는 것 방지)

대안(이번 기본안이 아님):

- A. Skill만 바꾸고 게이트는 그대로 → 구현은 쉽지만, 지금처럼 바로 Plan을 쓸 위험이 큼
- B. 킥오프 4단계를 Delivery `step`에 섞음 → `explore` 의미가 이중이 되어 운영이 어려움

### 3) Phase 0 / Phase 1 Document / documentation 규칙

- **제품 설명으로 시작** → 킥오프 K1…K4. Phase 0으로 가지 않음
- **Phase 0**은 “템플릿만 복사했고 제품 없이 docs/bootstrap만”일 때만
- **Phase 1 Document**: 기초 docs를 처음부터 채우지 않음. 킥오프 K3 이후 **이 Phase로 바뀐 점만**
- `documentation.mdc`: “코드 확인 전에 Docs를 추측으로 채우지 말 것”은 **유지**하되, **킥오프 K3는 합의된 설계를 기록하는 예외**라고 한 줄로만 명시. Rules에 docs 본문을 복사하지 않음

### 4) Small / Medium

변경 없음. 게이트 `off`인 버그 수정·작은 기능은 질문 라운드를 강제하지 않음.

## Delivery Phases

각 Phase 진행 시 6단계(순서 고정):
1 Explore → 2 Document → 3 Plan(상세·승인) → 4 Implement → 5 Verify(+User Test Guide) → 6 Review → Human Verify

### Phase 1 — 킥오프 프로토콜(Skill·가이드·템플릿) 도입

- Goal: 에이전트가 Large에서 K1→K2→K3→K4 순서를 따르고, 사람이 각 합의 지점을 선택할 수 있게 한다. 게이트 필드 추가는 아직 하지 않아도, Skill만으로 순서가 읽히게 한다.
- In / Out:
  - In: `project-kickoff`, `senior-pm`, `senior-architect`, `senior-design`(UI 시), `delivery-phase`(Phase 1 Document가 기초 docs가 아님을 한 줄), `guide.md` §3, `docs/ai/agent-workflow.md` 킥오프·표준 흐름, `TEMPLATE.md`/`README.md`/`AGENTS.md`/`CLAUDE.md`/`01-agent-workflow.mdc`의 **짧은 흐름 줄**, `.cursor/plans/_design-template.md` 신설, `_template.md`에 “K4에서만 작성 / 선행 K1–K3” 주석, `docs/product.md` 스텁, `docs/README.md` 표, `documentation.mdc` 킥오프 예외 한 줄, `.cursor/skills/README.md`
  - Out: `gate.json` 스키마·`gate.sh`/`phase_gate.py` 변경, 훅 동작 변경, 앱 코드
- 6-step status:
  - [x] 1 Explore
  - [x] 2 Document
  - [x] 3 Plan (상세) → Human approve
  - [x] 4 Implement
  - [x] 5 Verify (AI + User Test Guide)
  - [x] 6 Review → Human Verify
- Docs to update: `docs/ai/agent-workflow.md`, `docs/README.md`, `docs/product.md`(스텁), `guide.md`, `TEMPLATE.md`
- Changes (files): 위 In 목록
- AI Verify: 신규/수정 Skill에 K1에서 Plan 작성 금지·K2 산출물 경로·선택 UI 3종이 명시되어 있는지 파일 검색. `documentation.mdc`가 킥오프 예외를 포함하는지.
- User Test Guide:
  - Setup / Run: 이 템플릿 복사본에서 새 Chat. “할 일 앱 만들어줘. 지금은 설계만” 정도로 짧게 요청 (기능 목록을 일부러 덜 줌).
  - Check: (1) 첫 응답이 Phase Plan 파일이 아니라 질문 3–7개인지 (2) 설계 합의 메뉴가 나오기 전에 `.cursor/plans/*.md` Phase Plan을 안 쓰는지 (3) 합의 후 docs가 채워지는지 (4) 그다음 Phase Plan Draft와 승인 메뉴인지
  - Expected: K1→K2→K3→K4 순서. `src/` 변경 없음. 응답 첫 줄 `역할: 시니어 기획` 또는 설계.
  - If fails, report: 어느 단계에서 무엇을 먼저 썼는지, 선택 UI 유무, 생성/수정된 파일 목록
- Human Verify: [x] 통과 (다음 Phase 전 필수)

#### Phase 1 상세 구현 순서 (3단계 Plan · 승인 전 구현 금지)

이미 반영됨 (Document, 다시 쓰지 않음): `docs/decisions/001-kickoff-design-first.md`, `docs/product.md`, `docs/README.md`, `docs/architecture.md` 주석, `docs/ai/agent-workflow.md` 킥오프 흐름.

구현 순서 (Skill → 사람 가이드가 한 턴에 일치하도록):

1. `.cursor/plans/_design-template.md` **신설** — K2 목차만. `_template.md`와 비슷한 짧은 헤더 + Status Draft.
2. `.cursor/plans/_template.md` — 상단에 “K4에서만 작성. 선행 K1–K3” 주석. Steps 1을 `K1→K4 후 전체 Plan 승인`으로.
3. `.cursor/skills/project-kickoff/SKILL.md` — **핵심**. 즉시 Plan 금지. K1–K4 절차·역할·선택 UI 4종. K1에서 plans/docs/src 쓰기 금지. K2는 `_design-template.md` 복사. K3는 합의된 설계만 `docs/product.md`·`architecture.md`(해당 시 security). K4는 기존 Plan Draft + `on`+`approve-plan` 메뉴. description도 “질문→설계→docs→Phase Plan”으로.
4. `.cursor/skills/senior-pm/SKILL.md` — When: K1 primary, K2/K4 co-lead. Outputs에 질문 배치(3–7).
5. `.cursor/skills/senior-architect/SKILL.md` — When: K2/K3. Don’t “kickoff 전체를 혼자”는 유지.
6. `.cursor/skills/senior-design/SKILL.md` — When: K2에 UI가 있을 때 optional.
7. `.cursor/skills/delivery-phase/SKILL.md` — Document 한 줄: Phase 1 Document는 기초 docs가 아니라 **킥오프 K3 이후 변경분**.
8. `.cursor/skills/README.md` — kickoff 한 줄 갱신.
9. `.cursor/rules/documentation.mdc` — 킥오프 K3는 합의된 설계를 코드 없이 기록한다는 예외 **한 줄**. 본문 복사 금지.
10. `.cursor/rules/01-agent-workflow.mdc` — 킥오프 목록을 K1–K4로. Phase 0 조건에서 “제품 설명이면 킥오프”. Phase 1 Document 문구를 델타로.
11. `AGENTS.md` / `CLAUDE.md` — Large 한 줄을 K1–K4 포함으로. docs 본문 복사 금지.
12. `guide.md` §3 — 3-1 질문, 3-2 설계 합의, 3-3 docs, 3-4 Phase Plan, 3-5 Phase 6단계. 예시 프롬프트는 `agent-workflow.md`와 같은 취지. §4 게이트 CLI 신규 명령은 **넣지 않음** (Phase 2).
13. `TEMPLATE.md` 핵심 흐름 블록, `README.md` 하단 A/B 주석, `guide.md` §9 한 줄 요약.

하지 않음: `scripts/**`, `phase-gate` Skill, `gate.json` 스키마, 훅, `src/`.

AI Verify (구현 후):

- `rg "Create \`.cursor/plans" .cursor/skills/project-kickoff` 가 K1 첫 단계가 아님
- `rg "K1 Discover|질문 라운드" .cursor/skills/project-kickoff/SKILL.md guide.md`
- `rg "kickoff K3" .cursor/rules/documentation.mdc .cursor/skills/delivery-phase/SKILL.md`
- `python3 scripts/_verify_phase_gate.py` — **기존과 동일하게 통과** (Phase 1에서 게이트 코드 안 건드림)

User Test Guide (구현 후, 이 레포 Chat에서):

- Setup: 새 Agent Chat. `할 일 앱 만들어줘. 필수 기능은 아직 잘 모르겠어. 코드 쓰지 마.`
- Check: 첫 응답이 질문 3–7개. `.cursor/plans/`에 Phase Plan이 아직 없음. `src/` 변경 없음.
- Expected: 질문 끝에 K1 선택 UI. 역할 줄 `시니어 기획`.
- If fails: 첫 응답 전문, 생성된 파일 목록, `git status`.

### Phase 2 — 게이트로 설계 합의 이전 Plan 승인 차단

- Goal: `design_approved` 없이 `approve-plan`이 실패하고, `on` 시 `kickoff_step=discover`가 되게 한다. 기존 Small(`off`)·이미 `plan_approved`인 상태는 깨지지 않게 한다.
- In / Out:
  - In: `scripts/lib/phase_gate.py` (DEFAULT_GATE, save_gate 키 유지), `scripts/_gate_cli.py`, `scripts/gate.sh` usage, `scripts/_verify_phase_gate.py`, `phase-gate` Skill, `guide.md` §4 메뉴·동등 CLI, `docs/ai/agent-workflow.md` 게이트 표, `project-kickoff`의 gate.sh 매핑 (K2→`approve-design`, K3→`kickoff phase_plan`, K4→`approve-plan`)
  - Out: 앱 코드. docs 쓰기 훅 차단. Delivery 6 `step` 이름 변경
- 6-step status:
  - [x] 1 Explore
  - [x] 2 Document (변경분만)
  - [x] 3 Plan (상세) → Human approve
  - [x] 4 Implement
  - [x] 5 Verify (AI + User Test Guide)
  - [x] 6 Review → Human Verify
- Docs to update: `docs/ai/agent-workflow.md`, `guide.md` §4, `docs/development.md` 게이트 한 줄
- Changes (files): 위 In
- AI Verify: `python3 scripts/_verify_phase_gate.py` 통과. 추가 케이스: `on` 후 `approve-plan` 거부, `approve-design` 후 `approve-plan` 허용, `off` 시 코드/커밋 기존과 동일, `save_gate`가 `kickoff_step`/`design_approved`를 버리지 않음. 구 `gate.json`(필드 없음)은 로드 시 기본값으로 호환.
- User Test Guide:
  - Setup / Run: `./scripts/install-hooks.sh` 후 `./scripts/gate.sh on` → `status` → `approve-plan` 시도 → `approve-design` → `kickoff phase_plan` → `approve-plan` → `status`
  - Check: 설계 승인 전 `approve-plan` 실패 메시지. 승인 후 `kickoff_step=done`, `step=explore`. 채팅 메뉴 문구가 CLI와 1:1인지.
  - Expected: 위 순서만 성공. `src/` 쓰기 여전히 plan 승인 전 차단.
  - If fails, report: `gate.sh status` JSON, 실패한 명령, stderr
- Human Verify: [x] 통과 (다음 Phase 전 필수)

#### Phase 2 상세 구현 순서 (3단계 Plan · 승인 전 구현 금지)

이미 반영됨 (Document): ADR-001 게이트 고정점, `docs/ai/agent-workflow.md` 메뉴·CLI 표, `docs/development.md` 한 줄.  
`guide.md` §4는 **구현과 같은 턴**에 맞춰, 명령이 실제로 생긴 뒤에 고친다.

구현 순서:

1. `scripts/lib/phase_gate.py`
   - `DEFAULT_GATE`에 `kickoff_step: "done"`, `design_approved: false`
   - `VALID_KICKOFF_STEPS = discover|design|docs|phase_plan|done`
   - `save_gate` ordered 키에 두 필드 포함. 없으면 `SystemExit`
   - `load_gate`: 파일에 필드가 없을 때 `plan_approved`이면 `design_approved=true` + `kickoff_step=done`, 아니면 `discover` + `false`
   - Delivery `VALID_STEPS`는 그대로. 훅의 `can_write_code` / docs 쓰기는 변경하지 않음
2. `scripts/_gate_cli.py` + `scripts/gate.sh` usage
   - `on`: `enabled=true`, `plan_approved=false`, `design_approved=false`, `kickoff_step=discover`, `step=explore`, `allow_commit=false`, **phase 유지**
   - `approve-design`: 필요 시 `enabled=true`, `design_approved=true`, `kickoff_step=docs`, `plan_approved=false`, `allow_commit=false`
   - `kickoff <step>`: `VALID_KICKOFF_STEPS`만. K3는 `kickoff phase_plan`
   - `approve-plan`: `design_approved`가 아니면 stderr + exit 1. 성공 시 `plan_approved=true`, `kickoff_step=done`, `step=explore`, `allow_commit=false` (기존처럼 미enabled면 enable)
   - `next-phase` / `off`: kickoff 필드는 유지 (`done`을 건드리지 않음)
3. `scripts/_verify_phase_gate.py`
   - **시작 시 `gate.json` 스냅샷, `finally`에서 복구** (테스트가 작업 중 게이트를 DEFAULT로 덮어쓰지 않게)
   - 기존 케이스 유지
   - 추가: `on` 후 `approve-plan` 실패; `approve-design` 후 `approve-plan` 성공 + `kickoff_step=done`; `save_gate`가 새 키를 유지; 필드 없는 JSON 로드 호환; `off` 시 코드/커밋 허용은 기존과 동일
4. `.cursor/skills/project-kickoff/SKILL.md` — K2 선택 1 → `approve-design`; K3 선택 1 → `kickoff phase_plan`; K4 선택 1 → **`approve-plan`만** (`on`과 묶지 않음). “K1–K3 CLI 없음” 문구 삭제
5. `.cursor/skills/phase-gate/SKILL.md` — 필드 표 + K2/K3/K4 메뉴 화살표 + Equivalent CLI. K4 Draft 메뉴에서 `on` + `approve-plan` 제거
6. `guide.md` §4-2 ①을 K4 `approve-plan`만으로. K2/K3 메뉴와 `approve-design` / `kickoff`를 §4-2·§4-4 표에 추가. `01-agent-workflow.mdc` mutating 명령 목록에 `approve-design`·`kickoff` 추가 (한 줄)

하지 않음: `src/`, docs 쓰기 훅 차단, Delivery `step` 이름 변경, `on`이 phase를 1로 리셋.

AI Verify:

- `python3 scripts/_verify_phase_gate.py` 전부 PASS, 종료 후 `./scripts/gate.sh status`가 테스트 전과 동일
- `./scripts/gate.sh on` → `approve-plan` → non-zero
- `./scripts/gate.sh approve-design` → `kickoff phase_plan` → `approve-plan` → `kickoff_step=done`
- `rg "on\` then \`approve-plan|on` \\+ \`approve-plan" .cursor/skills/project-kickoff/SKILL.md` 매치 없음

User Test Guide (구현 후):

- Setup: `./scripts/gate.sh status`를 먼저 기록. 그다음 `on` → `approve-plan`(실패) → `approve-design` → `kickoff phase_plan` → `approve-plan` → `status`
- Check: 실패 stderr에 `design_approved` 언급. 성공 후 `kickoff_step=done`, `step=explore`. `guide.md` §4 화살표와 명령이 같음
- Expected: 위만 성공. `src/`는 plan 승인 전 여전히 차단
- If fails: status JSON, 명령, stderr. 테스트 후 status를 기록값과 비교

## Changes (전체 요약)

| File | Change | Why | Phase |
|------|--------|-----|-------|
| `.cursor/skills/project-kickoff/SKILL.md` | 즉시 Plan → K1–K4 + 선택 UI 4종 | 핵심 행동 변경 | 1–2 |
| `.cursor/skills/senior-pm/SKILL.md` | 킥오프 primary를 Discover/Design/Phase Plan으로 | 질문·범위 합의 | 1 |
| `.cursor/skills/senior-architect/SKILL.md` | K2/K3 설계 문서 관점 추가 | 전체 설계 | 1 |
| `.cursor/skills/delivery-phase/SKILL.md` | Phase 1 Document = 기초가 아니라 델타 | 중복 문서화 방지 | 1 |
| `.cursor/skills/phase-gate/SKILL.md` | 신규 CLI·메뉴 | 게이트 운영 | 2 |
| `.cursor/plans/_design-template.md` | 전체 설계 초안 템플릿 | K2 산출물 | 1 |
| `.cursor/plans/_template.md` | K4에서만 작성한다고 명시 | 혼선 방지 | 1 |
| `docs/product.md` | 제품 설계 스텁 | K3 목적지 | 1 |
| `guide.md`, `docs/ai/agent-workflow.md`, `TEMPLATE.md`, `README.md` | 권장 순서·프롬프트 | 사람/에이전트 정렬 | 1–2 |
| `AGENTS.md`, `CLAUDE.md`, `01-agent-workflow.mdc` | 한 줄 흐름만 | Rules에 docs 본문 복사 금지 | 1 |
| `.cursor/rules/documentation.mdc` | 킥오프 K3 예외 한 줄 | 코드 전 문서화 허용 | 1 |
| `scripts/lib/phase_gate.py`, `_gate_cli.py`, `gate.sh`, `_verify_phase_gate.py` | 필드·명령·테스트 | 건너뛰기 방지 | 2 |

## Steps

1. 전체 Plan 승인
2. Phase 1: Explore → Document → Plan → (승인) Implement → Verify → Review → 사람 검수
3. 승인 후 Phase 2도 동일 6단계 …
4. 전체 마무리 Review

## Verification

- [ ] Phase마다 6단계 완료
- [ ] 관련 테스트: `python3 scripts/_verify_phase_gate.py` (Phase 2)
- [ ] User Test Guide 제공 (Phase마다)
- [ ] docs 갱신 (Phase 2 Document)

## Risks

- 질문 라운드가 길어지면 킥오프가 무거워짐 → **3–7개 배치, 2라운드 권장 상한**, 사용자가 “제안해”면 진행
- 게이트를 과하게 넣으면 Small 마찰·구 `gate.json` 깨짐 → 필드 기본값 호환, `off` 동작 유지, docs 쓰기는 훅으로 안 막음
- K3와 Phase 1 Document 중복 → Phase 1 Document를 델타로 재정의
- `documentation.mdc`와 충돌 → 킥오프 K3만 예외
- 설계 파일을 plans와 docs에 두 벌 → K2는 합의용 Draft, K3 이후 **docs가 진실 원천**. design.md는 합의 스냅샷으로 두거나 Status에 “문서화됨”만 표시

## Human Review

- [ ] 킥오프를 K1–K4로 늘리는 것 수용 (바로 Phase Plan 폐지)
- [ ] 설계 산출물을 `*-design.md`에 두고, 합의 후 `docs/`로 옮기는 것 수용
- [ ] 게이트는 `design_approved` + `kickoff_step` 최소 강제 (Skill-only / step 섞기 아님)
- [ ] Delivery 6단계 순서는 그대로 두는 것 수용
- [ ] 전체 Plan 승인 (Approved 전에 Agent는 Phase 구현 금지)
- [ ] 각 Phase: 상세 Plan 승인 + Human Verify (다음 Phase 전)

## Status

Draft | **Approved** | In Progress | **Done (Phase 1–2 Human Verify 통과 · allow_commit)**

<!-- 강제 검사 진실 원천은 Status가 아니라 .cursor/gate.json (채팅 선택→./scripts/gate.sh) -->
