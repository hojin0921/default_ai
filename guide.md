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
- Large(새 프로젝트)에서는 **터미널보다 채팅 번호 메뉴**로 승인·단계 전진하는 것이 기본이다

---

## 2. 역할

| 사람 | AI |
|------|-----|
| 무엇을 만들지, 필수 기능 확정 | Plan 초안, 구현, 자동 테스트 |
| Plan / 단계 / Phase를 **채팅 메뉴에서 선택·승인** | 선택에 맞춰 `./scripts/gate.sh` 대행 |
| Guide대로 **직접** 테스트·검수 | User Test Guide · 리뷰 초안 |
| (선택) 터미널에서 동일 `gate.sh` 직접 실행 | `gate.json` **직접** 수정 · **선택 없는** 자가 승인 **금지** |

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

### 3-2. Plan 검토 후 채팅에서 선택

1. `.cursor/plans/` 의 Draft를 읽는다  
2. AI가 내는 **한글 번호 메뉴**에서 고른다  
   - 승인 → `1`  
   - 수정 → `2` + 같은 메시지에 고칠 내용  
   - 보류 → `3`  

(터미널을 쓰고 싶다면 §4 동등 명령 참고.)

### 3-3. Phase마다 6단계

**Phase 개수**는 프로젝트마다 다르다 (Phase 1…N).  
**각 Phase 안**에서 아래 6단계를 건너뛰지 않는다.

| # | 단계 | 채팅 예시 | 사람 할 일 |
|---|------|-----------|------------|
| 1 | Explore | `코드 작성하지 말고 이해해` | 결과 확인 |
| 2 | Document | `이해한 내용을 문서화해` | docs 확인 |
| 3 | Plan | `이 기능을 어떻게 구현할지 계획해` | 상세 Plan 확인 후 **메뉴에서 선택** |
| 4 | Implement | (메뉴 `1` 승인 후) 구현 | — |
| 5 | Verify | `테스트하고 검증해. User Test Guide도 줘` | Guide대로 **직접** 테스트 |
| 6 | Review | `다시 리뷰해` | 검수 결과를 **메뉴에서** 선택 |

결정 지점마다 AI는 번호 메뉴를 낸다. 사용자가 고르기 전에 게이트를 전진하거나 구현하지 않는다.

AI Skill: `delivery-phase`.

---

## 4. Phase Gate — 채팅 선택 (기본) / 터미널 (동등)

강제 검사의 진실 원천은 Plan Status가 아니라 **`.cursor/gate.json`** 이다.  
전진 채널: **채팅에서 번호 선택 → AI가 `./scripts/gate.sh` 실행**, 또는 사람이 같은 명령을 터미널에서 실행.

### 4-1. 채팅 메뉴 (한글)

AI는 아래처럼 **쉬운 한글 번호 메뉴**를 낸다.  
화살표(→) 줄은 선택 시 돌아가는 게이트 동작이다.

**① 전체 개발 계획(Draft)을 받은 뒤**

1. 이 전체 계획을 승인하고, Phase 1의 1단계(코드 없이 이해하기)부터 진행해 주세요  
   → 게이트 켜기(`on`) + 계획 승인(`approve-plan`) 후 Explore  
2. 계획 내용을 수정해 주세요 (지금은 승인하지 않음)  
3. 지금은 보류할게요. 나중에 이어갈게요  

**② 이 Phase의 상세 구현 계획을 받은 뒤**

1. 이 상세 계획을 승인하고, 이제 구현해 주세요  
   → `advance implement` 후 구현  
2. 상세 계획을 수정해 주세요 (구현은 아직 하지 않음)  
3. 지금은 보류할게요  

**③ 검증(Verify) / 리뷰(Review) 후, 내가 테스트까지 해본 뒤**

1. 검수 통과예요. 커밋해도 되게 열어 주세요  
   → `allow-commit` (실제 `git commit`은 내가 따로 요청할 때만)  
2. 아직 문제 있어요. 같은 Phase에서 고치고 검증을 다시 해 주세요  
3. 이 Phase는 통과. 다음 Phase로 가고, 지금은 조사(Explore)만 해 주세요  
   → `next-phase` 후 Explore만  

### 4-2. 메뉴에서 수정할 때 (`2` + 프롬프트)

별도 Chat을 새로 열 필요 없다. **`2`와 수정 내용을 같은 메시지에** 쓰면 된다.

```text
2
로그인에 소셜 로그인(Google)도 Phase 1에 넣어줘.
결제 관련은 Phase 3으로 미뤄줘.
```

```text
2
버튼 문구가 "저장"인데 "등록"으로 바꿔줘.
모바일에서 입력창이 가려지는 것도 같이 고쳐줘.
```

```text
2
Phase 2 Verify에서 로그인이 실패해.
에러 메시지: …
기대: 로그인 후 홈으로 이동
```

규칙:

- `2`만 보낸 뒤, 다음 메시지에 수정 내용을 이어서 써도 된다  
- 수정이 끝나면 AI가 **메뉴를 다시** 낸다 (승인 / 추가 수정 / 보류 등)  
- 마음에 들 때만 `1`(승인·통과)을 고른다  
- `2`만으로는 승인·게이트 전진이 아니다  

### 4-3. 동등 터미널 명령 (선택)

채팅 메뉴 대신 직접 실행해도 결과는 같다.

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
- AI가 `gate.json`을 **직접** 쓰는 것 차단 (`gate.sh` 대행은 사람 선택 후 허용)

---

## 5. 작은 수정 (Small)

게이트는 끈 채로 (`off`) 일반적인 수정 요청만 하면 된다.

채팅에서 Small용 해제를 요청하거나:

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
- Plan·단계 **선택/승인 없이** 구현·게이트 전진  
- 사용자 테스트 없이 다음 Phase로 넘어가기  
- AI에게 `gate.json`을 **직접** 고치게 하기  
- `.env` 실제 값을 채팅에 붙이기  

---

## 9. 한 줄 요약

**프로젝트 설명 → 채팅 메뉴로 Plan 승인 → Phase마다 6단계 → AI 검증 + 내가 테스트 → 메뉴로 다음 진행.**  
수정이 필요하면 **`2` + 고칠 내용**을 같은 메시지에 쓰면 된다.
