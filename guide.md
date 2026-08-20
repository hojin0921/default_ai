# 템플릿 사용 가이드

이 저장소는 **앱 스캐폴드가 아니라** Cursor에서 AI와 같이 개발하기 위한 **프로토콜 템플릿**이다.  
Rules · Skills · Hooks · Plans · Gate가 레포에 들어 있다.

상세 프롬프트 모음: [`docs/ai/agent-workflow.md`](docs/ai/agent-workflow.md)  
구조 설명: [`TEMPLATE.md`](TEMPLATE.md)

---

## 1. 준비 (복사/클론 후 한 번)

폴더를 통째로 복사하면 **`.git`까지 같이 가서** 원래 원격(origin)에 연결된 채로 복제된다.  
새 프로젝트로 쓰려면 **git 이력을 끊고** 새로 시작하는 것이 맞다.

### 권장: `.git` 없이 복사한 뒤 새 저장소

```bash
# 예: 템플릿 → 새 프로젝트 폴더 (macOS)
rsync -a --exclude='.git' /path/to/default_ai/ /path/to/my-new-project/
cd /path/to/my-new-project
git init
./scripts/install-hooks.sh
./scripts/gate.sh status
```

이미 `.git`이 포함된 채로 복사했다면:

```bash
cd /path/to/my-new-project
rm -rf .git
git init
# 필요하면: git remote add origin <새-원격-URL>
./scripts/install-hooks.sh
./scripts/gate.sh status
```

- `enabled: false` → 작은 작업은 게이트 없이 진행 가능  
- Cursor로 **새 프로젝트 폴더**를 열고 **Agent** 채팅을 사용한다  
- Large(새 프로젝트)에서는 **터미널보다 채팅 선택 UI**로 승인·단계 전진하는 것이 기본이다

### 선택 UI가 버튼으로 안 보일 때

결정 메뉴는 가능하면 Cursor **`AskQuestion`(클릭 선택 카드)** 로 낸다.  
일부 모델(예: Grok)에서는 이 도구가 없어 **한글 번호 텍스트**로 대체된다.

버튼 UI를 쓰려면 Agent 모델을 **Composer / Claude / GPT** 등으로 바꾸면 된다. (Auto가 Grok으로 가면 다시 텍스트가 될 수 있음.)

---

## 2. 역할

### 2-1. 사람 ↔ AI

| 사람 | AI |
|------|-----|
| 무엇을 만들지, 필수 기능 확정 | Plan 초안, 구현, 자동 테스트 |
| Plan / 단계 / Phase를 **채팅에서 선택·승인** (버튼 또는 번호) | 선택에 맞춰 `./scripts/gate.sh` 대행 |
| Guide대로 **직접** 테스트·검수 | User Test Guide · 리뷰 초안 |
| (선택) 터미널에서 동일 `gate.sh` 직접 실행 | `gate.json` **직접** 수정 · **선택 없는** 자가 승인 **금지** |

### 2-2. 시니어 역할 Skill (한 Agent · 관점만 교체)

별도 봇을 여러 개 띄우는 것이 아니다. **같은 Agent Chat**에서 단계에 맞는 Skill이 관점을 바꾼다.  
AI 응답 첫 줄에 `역할: 시니어 ○○`이 붙는 것이 정상이다.  
각 역할 Skill의 **Quality bar**를 충족해야 한다. 피상적인 요약·형용사만 있는 산출물은 시니어 작업이 아니다.

| Skill | 한글 | 언제 주로 |
|-------|------|-----------|
| `senior-architect` | 시니어 설계 | Explore, 구조·보안 |
| `senior-pm` | 시니어 기획 | 킥오프·Plan, 범위 |
| `senior-design` | 시니어 디자인 | UI/UX·카피 |
| `senior-dev` | 시니어 개발 | Implement |
| `senior-qa` | 시니어 QA | Verify·Review |

| 6단계 | 주 역할 |
|--------|---------|
| Explore | 설계 (+ 기획) |
| Document | 설계 / 기획 |
| Plan | 기획 + 설계 (+ 디자인 if UI) |
| Implement | 개발 |
| Verify | QA |
| Review | QA + 설계 |

상세 표·산출물: [`docs/ai/agent-workflow.md`](docs/ai/agent-workflow.md) 「역할 Skill」.  
Skill 목록: [`.cursor/skills/README.md`](.cursor/skills/README.md).

### 2-3. 역할 명시 호출 (Large / Medium / Small)

사용자가 채팅에서 역할을 **직접 지정**하면, 기본 6단계 매핑보다 **그 지정이 우선**이다.  
지정하지 않으면 Large는 §2-2·`delivery-phase` Role map을 따른다.

예시:

```text
시니어 QA로만 리뷰해. 구현은 하지 마.
```

```text
시니어 디자인 관점으로 온보딩 화면 카피만 다듬어줘.
```

```text
시니어 설계로 이 변경의 영향 범위만 짧게 정리해. 코드 작성 금지.
```

FAQ:

- **Q. 역할을 안 쓰면?** → Large Phase면 단계 기본 역할. Small이면 보통 개발 중심으로 처리.  
- **Q. 여러 역할을 한 번에?** → 가능하면 하나만. 필요하면 “설계 후 QA”처럼 **순서**를 적는다.  
- **Q. Small인데 게이트는?** → 보통 `off`. 역할 지정과 게이트는 별개다.  
- **Q. 응답에 역할이 안 보이면?** → `역할: 시니어 ○○`이 없으면 다시 요청하거나 모델/Skills를 확인한다.

---

## 3. 새 프로젝트 (Large) — 권장 순서

바로 Phase Plan을 받지 않는다. **질문 → 전체 설계 합의 → docs → Phase Plan** 순이다.  
AI Skill: `project-kickoff` (자동 또는 명시).

### 3-1. 질문 라운드 (K1)

새 Chat에서. 기능이 비어 있어도 된다.

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
<!-- 스택, 플랫폼, 기한 등. 없으면 생략 -->
```

AI가 질문 3–7개를 한 번에 한다. 모르면 “제안해”라고 답해도 된다.  
선택 UI: 이 이해로 설계 초안 / 더 질문·수정 / 보류.

### 3-2. 전체 설계 합의 (K2)

채팅의 **한눈 그림**(Mermaid)과 **확인할 파일**을 본다 (보통 `.cursor/plans/<이름>-design.md`).  
읽은 뒤 선택 UI: 합의하고 문서화 / 설계 수정 / 보류.

### 3-3. docs 문서화 (K3)

같은 그림과 **확인할 파일** (`docs/product.md`, `docs/architecture.md` 등)을 연다.  
읽은 뒤 선택 UI: Phase Plan 초안 작성 / 문서 수정 / 보류.

### 3-4. Phase Plan 검토 후 채팅에서 선택 (K4)

1. 채팅의 **Phase 한눈 그림**(1→N)과 **확인할 파일**의 Plan Draft를 본다 (`.cursor/plans/<이름>.md`)  
2. AI가 내는 **선택 UI**에서 고른다  
   - **버튼 카드**가 보이면 해당 항목을 클릭  
   - 텍스트 번호만 보이면 `1` / `2` / `3`  
   - 수정(`2`)이면 같은 메시지(또는 다음 메시지)에 고칠 내용을 적는다  

(터미널을 쓰고 싶다면 §4-3 동등 명령 참고.)

### 3-5. Phase마다 6단계

**Phase 개수**는 프로젝트마다 다르다 (Phase 1…N).  
**각 Phase 안**에서 아래 6단계를 건너뛰지 않는다.

| # | 단계 | 주 역할 | 채팅 예시 | 사람 할 일 |
|---|------|---------|-----------|------------|
| 1 | Explore | 설계 | `코드 작성하지 말고 이해해` | 결과 확인 · `역할: 시니어 설계` 확인 |
| 2 | Document | 설계/기획 | `이해한 내용을 문서화해` | docs 확인 |
| 3 | Plan | 기획+설계 | `이 기능을 어떻게 구현할지 계획해` | **한눈 그림**+파일 확인 후 **메뉴에서 선택** |
| 4 | Implement | 개발 | (승인 선택 후) 구현 | 실행 가능하면 **실행 가이드**로 켜 보기 |
| 5 | Verify | QA | `테스트하고 검증해. 직접 확인 가이드도 줘` | **직접 확인 가이드**대로 실행·확인 후 **메뉴에서 선택** |
| 6 | Review | QA+설계 | `다시 리뷰해` | 검수 결과를 **메뉴에서** 선택 |

마지막 Phase면 Verify 채팅 순서는 **실행 가이드** → **역할 기여** → **직접 확인 가이드**.

결정 지점마다 AI는 선택 UI(가능하면 버튼)를 낸다. 사용자가 고르기 전에 게이트를 전진하거나 구현하지 않는다.  
응답에 **지금 역할**(`역할: 시니어 ○○`)이 보여야 한다.

AI Skill: `delivery-phase` (+ 단계별 `senior-*`).

### 3-6. 실행 가이드 (개발이 끝난 뒤)

검수 시나리오와 별개다. **결과물을 어떻게 켜고 접속하는지**를 남긴다.

구현이 실행 가능한 산출물을 만들었으면 AI는 채팅과 `README.md` / `docs/development.md`에 실제 명령을 적는다 (추측 금지, secret 금지).

```
## 실행 가이드
- 준비: (런타임, 설치)
- 실행: (복사해 붙일 명령)
- 접속: (URL / 화면)
```

실행할 앱이 없는 Phase는 “이 Phase는 실행 대상 없음” 한 줄이면 된다.

### 3-7. 역할 기여 (개발이 끝난 뒤)

마지막 Phase에서 AI는 **어느 시니어 역할이 무엇을 만들었고, 그게 어디에 쓰이는지**를 채팅과 Phase Plan에 남긴다. 추측 금지. 안 쓴 역할은 “해당 없음”.

```
## 역할 기여
| 역할 | 만든 것 | 어떻게 쓰이는지 |
| 시니어 기획 | | |
| 시니어 설계 | | |
| 시니어 디자인 | | |
| 시니어 개발 | | |
| 시니어 QA | | |
```

킥오프(질문·설계·docs·Phase Plan)도 한 줄씩 포함한다.

---

## 4. Phase Gate — 채팅 선택 (기본) / 터미널 (동등)

강제 검사의 진실 원천은 Plan Status가 아니라 **`.cursor/gate.json`** 이다.  
전진 채널: **채팅에서 명시 선택 → AI가 `./scripts/gate.sh` 실행**, 또는 사람이 같은 명령을 터미널에서 실행.

### 4-1. 선택 UI 우선순위 (Agent)

1. **`AskQuestion` 사용 가능** → 한글 옵션으로 **클릭 가능한 선택 카드(버튼)** 제시 (한 메시지에 질문 하나)  
2. **불가** → 아래와 같은 **한글 번호 텍스트 메뉴**로 대체  
3. 선택 전에는 게이트 전진·구현 금지. 선택 후 해당 `gate.sh`만 실행하고 `status`로 짧게 보고  

### 4-2. 메뉴 문구 (한글 · 버튼/번호 공통)

화살표(→) 줄은 선택 시 돌아가는 게이트 동작이다.  
버튼 라벨도 **같은 한글 문장**을 쓴다.

**① 킥오프 K2 — 전체 설계 초안 후**

1. 이 전체 설계를 합의하고, 이제 문서화해 주세요  
   → `approve-design` 후 문서화  
2. 설계 내용을 수정해 주세요 (문서화는 아직 하지 않음)  
3. 지금은 보류할게요  

**② 킥오프 K3 — docs 문서화 후**

1. 문서를 확인했습니다. Phase Plan 초안을 작성해 주세요  
   → `kickoff phase_plan` 후 Phase Plan  
2. 문서를 수정해 주세요  
3. 지금은 보류할게요  

**③ 킥오프 K4 — 전체 개발 계획(Draft)을 받은 뒤**

1. 이 전체 계획을 승인하고, Phase 1의 1단계(코드 없이 이해하기)부터 진행해 주세요  
   → `approve-plan` 후 Explore (`on`과 묶지 않음)  
2. 계획 내용을 수정해 주세요 (지금은 승인하지 않음)  
3. 지금은 보류할게요. 나중에 이어갈게요  

**④ 이 Phase의 상세 구현 계획을 받은 뒤**

채팅의 **이 Phase 한눈 그림**(작업 순서)과 **확인할 파일**을 본다.  
AskQuestion: `아래 이 Phase 그림과 상세 Plan을 확인한 뒤, 어떻게 할까요?`

1. 이 상세 계획을 승인하고, 이제 구현해 주세요  
   → `advance implement` 후 구현  
2. 상세 계획을 수정해 주세요 (구현은 아직 하지 않음)  
3. 지금은 보류할게요  

**⑤ 검증(Verify) / 리뷰(Review) 후, 내가 테스트까지 해본 뒤**

채팅의 **직접 확인 가이드**(실행·확인·기대)대로 직접 해본다.  
마지막 Phase면 그 위에 **실행 가이드**(준비·실행·접속)와 **역할 기여**(누가 무엇을·어디에 쓰이는지)가 있어야 한다.  
AskQuestion: `Phase N을 직접 플레이해 보신 결과는 어떤가요?`  
(화면이 없는 Phase는 `직접 확인해 보신 결과는 어떤가요?`)

채팅 메뉴에는 **커밋 항목이 없다.** `git commit`은 내가 직접 한다.

1. 직접 확인해 보니 통과예요  
2. 아직 문제 있어요. 같은 Phase에서 고치고 검증을 다시 해 주세요  
3. 이 Phase는 통과. 다음 Phase로 가고, 지금은 조사(Explore)만 해 주세요  
   (마지막 Phase이면: 이 Phase는 통과. 전체 개발을 마무리해 주세요)

1번을 고르면 커밋 잠금만 풀린다 (`allow-commit`). `git commit`은 내가 직접 한다.  
3번(다음 Phase)은 `next-phase` 후 Explore만. 이미 연 커밋 잠금은 다음 Phase로 가도 유지된다.  
마지막 Phase 3번은 `next-phase`를 하지 않는다.  

### 4-3. 메뉴에서 수정할 때 (수정 선택 + 프롬프트)

별도 Chat을 새로 열 필요 없다.

- **버튼 UI**: “수정해 주세요”를 고른 뒤, 이어지는 메시지에 고칠 내용을 적는다  
- **번호 텍스트**: **`2`와 수정 내용을 같은 메시지에** 써도 된다  

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
- 수정이 끝나면 AI가 **선택 UI를 다시** 낸다 (승인 / 추가 수정 / 보류 등)  
- 마음에 들 때만 승인·통과를 고른다  
- 수정 선택만으로는 승인·게이트 전진이 아니다  

### 4-4. 동등 터미널 명령 (선택)

채팅 선택 대신 직접 실행해도 결과는 같다.

| 상황 | 명령 |
|------|------|
| 현재 상태 | `./scripts/gate.sh status` |
| Large 리셋 (설계 미합의) | `./scripts/gate.sh on` |
| 전체 설계 합의 | `./scripts/gate.sh approve-design` |
| Phase Plan 단계로 | `./scripts/gate.sh kickoff phase_plan` |
| 전체 Plan 승인 | `./scripts/gate.sh approve-plan` |
| 단계 설정 | `./scripts/gate.sh advance explore\|document\|plan\|implement\|verify\|review\|human_verify` |
| 커밋 잠금 해제 (채팅 메뉴에는 없음. 1번 통과 시 대행되거나 여기서 직접) | `./scripts/gate.sh allow-commit` |
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
역할을 붙이려면 §2-3처럼 `시니어 개발로 …` / `시니어 QA로만 …`을 앞에 쓴다.

---

## 6. 중간 크기 (Medium)

Explore → 짧은 Plan → Implement → Verify.  
긴 Phase 분할·게이트는 필수가 아니다. 필요할 때만 `on` 한다.  
단계마다 역할을 바꾸거나, §2-3처럼 한 역할만 명시해도 된다.

---

## 7. 템플릿에 들어 있는 것

| 종류 | 위치 |
|------|------|
| Rules | `.cursor/rules/`, `AGENTS.md` |
| Skills | `.cursor/skills/` (`project-kickoff`, `delivery-phase`, `phase-gate` + `senior-*`) |
| Hooks | `.cursor/hooks.json` |
| Plans | `.cursor/plans/_template.md` |
| Gate | `.cursor/gate.json`, `scripts/gate.sh` |
| Git hook | `.githooks/pre-commit` ← `install-hooks.sh`로 연결 |
| 사람용 상세 | `docs/ai/agent-workflow.md` |

다른 프로젝트에 쓸 때: **이 레포를 복사**하면 Skills·Hooks·Rules가 함께 간다.

---

## 8. 하지 말 것

- “로그인/결제 전부 만들어줘”만으로 전 Phase 한 번에 구현 시키기  
- 질문·전체 설계 합의 없이 바로 Phase Plan  
- Plan·단계 **선택/승인 없이** 구현·게이트 전진  
- 사용자 테스트 없이 다음 Phase로 넘어가기  
- AI에게 `gate.json`을 **직접** 고치게 하기  
- `.env` 실제 값을 채팅에 붙이기  

---

## 9. 한 줄 요약

**프로젝트 설명 → 질문 → 전체 설계 합의 → docs → 채팅 선택(버튼 우선)으로 Phase Plan 승인 → Phase마다 6단계(역할 Skill) → AI 검증 + 내가 테스트 → 선택으로 다음 진행.**  
수정이 필요하면 **수정 선택 + 고칠 내용**을 쓰면 된다. 버튼이 안 보이면 모델을 Composer/Claude/GPT로 바꾸거나, 번호 `1`/`2`/`3`으로 고른다.
