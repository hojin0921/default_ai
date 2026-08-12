# 템플릿 사용 가이드

이 저장소는 **앱 스캐폴드가 아니라** Cursor에서 AI와 같이 개발하기 위한 **프로토콜 템플릿**이다.  
Rules · Skills · Hooks · Plans · Gate가 레포에 들어 있다.

상세 프롬프트 모음: [`docs/ai/agent-workflow.md`](docs/ai/agent-workflow.md)  
구조 설명: [`TEMPLATE.md`](TEMPLATE.md)

---

## 1. 준비 (복사/클론 후 한 번)

```bash
./scripts/install-hooks.sh
./scripts/gate.sh status
```

- `enabled: false` → 작은 작업은 게이트 없이 진행 가능  
- Cursor로 이 폴더를 열고 **Agent** 채팅을 사용한다

---

## 2. 역할

| 사람 | AI |
|------|-----|
| 무엇을 만들지, 필수 기능 확정 | Plan 초안, 구현, 자동 테스트 |
| Plan / 단계 / Phase 승인 | User Test Guide 작성 |
| Guide대로 **직접** 테스트·검수 | 리뷰 초안 |
| `./scripts/gate.sh`로만 게이트 전진 | `gate.json` 수정·자가 승인 **금지** |

---

## 3. 새 프로젝트 (Large) — 권장 순서

### 3-1. 전체 Plan만 받기 (구현 금지)

새 Chat에서:

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
<!-- 스택, 플랫폼, 기한 등. 없으면 생략 -->
```

AI Skill: `project-kickoff` (자동 또는 명시).

### 3-2. Plan 검토 후 승인 + 게이트

1. `.cursor/plans/` 의 Draft를 읽는다  
2. 터미널:

```bash
./scripts/gate.sh on
./scripts/gate.sh approve-plan
```

### 3-3. Phase마다 6단계

**Phase 개수**는 프로젝트마다 다르다 (Phase 1…N).  
**각 Phase 안**에서 아래 6단계를 건너뛰지 않는다.

| # | 채팅 예시 | 사람 할 일 |
|---|-----------|------------|
| 1 | `코드 작성하지 말고 이해해` (Explore) | 결과 확인 |
| 2 | `이해한 내용을 문서화해` (Document) | docs 확인 |
| 3 | `이 기능을 어떻게 구현할지 계획해` (Plan) | 상세 Plan 승인 후 아래 명령 |
| 4 | `좋아. 이 계획대로 구현해` (Implement) | — |
| 5 | `테스트하고 검증해. User Test Guide도 줘` (Verify) | Guide대로 **직접** 테스트 |
| 6 | `다시 리뷰해` (Review) | 검수 통과 여부 판단 |

3번 승인 후 구현 전에:

```bash
./scripts/gate.sh advance implement
```

5~6번 후 커밋이 필요하면:

```bash
./scripts/gate.sh allow-commit
```

Phase 통과 후 다음 Phase:

```text
Phase 1 검수 통과. Phase 2를 6단계로 시작해. 지금은 Explore만.
```

```bash
./scripts/gate.sh next-phase
```

문제 있으면:

```text
Phase N / 단계에서 문제: …
같은 Phase에서 고치고 Verify·User Test Guide를 다시 줘.
```

AI Skill: `delivery-phase`.

---

## 4. Phase Gate 명령 요약

강제 검사의 진실 원천은 Plan Status가 아니라 **`.cursor/gate.json`** 이다.  
사람은 **`./scripts/gate.sh`만** 사용한다.

| 상황 | 명령 |
|------|------|
| 현재 상태 | `./scripts/gate.sh status` |
| Large 시작 | `./scripts/gate.sh on` |
| 전체 Plan 승인 | `./scripts/gate.sh approve-plan` |
| 단계 설정 | `./scripts/gate.sh advance explore\|document\|plan\|implement\|verify\|review\|human_verify` |
| 커밋 허용 | `./scripts/gate.sh allow-commit` |
| 커밋 다시 잠금 | `./scripts/gate.sh deny-commit` |
| 다음 Phase | `./scripts/gate.sh next-phase` |
| Small용 해제 | `./scripts/gate.sh off` |

게이트가 켜져 있으면 (`enabled: true`):

- Plan 미승인 또는 Implement 전 단계 → `src/` 등 코드 쓰기 차단  
- `allow_commit: false` → `git commit` 차단  
- AI가 `gate.json` / mutating `gate.sh`를 쓰는 것 차단  

---

## 5. 작은 수정 (Small)

게이트는 끈 채로 (`off`) 일반적인 수정 요청만 하면 된다.

```bash
./scripts/gate.sh off
```

예: `이 버그 고쳐줘`, `문구만 바꿔줘`.

---

## 6. 중간 크기 (Medium)

Explore → 짧은 Plan → Implement → Verify.  
긴 Phase 분할·게이트는 필수가 아니다. 필요할 때만 `on` 한다.

---

## 7. 템플릿에 들어 있는 것

| 종류 | 위치 |
|------|------|
| Rules | `.cursor/rules/`, `AGENTS.md` |
| Skills | `.cursor/skills/` (`project-kickoff`, `delivery-phase`, `phase-gate`) |
| Hooks | `.cursor/hooks.json` |
| Plans | `.cursor/plans/_template.md` |
| Gate | `.cursor/gate.json`, `scripts/gate.sh` |
| Git hook | `.githooks/pre-commit` ← `install-hooks.sh`로 연결 |
| 사람용 상세 | `docs/ai/agent-workflow.md` |

다른 프로젝트에 쓸 때: **이 레포를 복사**하면 Skills·Hooks·Rules가 함께 간다.

---

## 8. 하지 말 것

- “로그인/결제 전부 만들어줘”만으로 전 Phase 한 번에 구현 시키기  
- Plan·단계 승인 전에 구현 진행  
- 사용자 테스트 없이 다음 Phase로 넘어가기  
- AI에게 `gate.json`을 고치거나 `approve-plan`을 시키기기  
- `.env` 실제 값을 채팅에 붙이기  

---

## 9. 한 줄 요약

**프로젝트 설명 → Plan 승인 → Phase마다 6단계 → AI 검증 + 내가 테스트 → 다음 Phase.**
