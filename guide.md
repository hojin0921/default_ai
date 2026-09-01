# 템플릿 사용 가이드

이 저장소는 **앱 스캐폴드가 아니라** AI와 같이 개발하기 위한 **프로토콜 템플릿**이다.  
Cursor, Claude Code, Codex, Antigravity에서 같은 킥오프·6단계·게이트로 일한다.  
Rules · Skills · Hooks · Plans · Gate가 레포에 들어 있다.

상세 프롬프트 모음: [`docs/ai/agent-workflow.md`](docs/ai/agent-workflow.md)  
구조 설명: [`TEMPLATE.md`](TEMPLATE.md)

---

## 1. 준비 (복사/클론 후 한 번)

이 템플릿의 **게이트·훅·스크립트**는 Python으로 동작한다. OS마다 **설치 항목**과 **PATH(터미널에서 명령을 찾을 수 있는지)** 가 맞아야 한다.

### OS별 필수 설치

| 항목 | macOS | Windows | Linux |
|------|-------|---------|-------|
| **Python 3.8+** | 필수 | 필수 | 필수 |
| **Git** | 필수 | 필수 | 필수 |
| **AI 도구** | Cursor 등 (택 1) | 동일 | 동일 |
| **bash** | 기본 (Terminal) | Git Bash 또는 WSL (`.sh` 쓸 때) | 기본 |
| **rsync** | 선택 (수동 복사 시) | 불필요 (`new-project` 사용) | 선택 (수동 복사 시) |

**Python이 필요한 이유:** gate CLI · Cursor 쓰기/커밋 차단 훅 · git pre-commit · `new-project` / `install-hooks` 스크립트.

**Git이 필요한 이유:** `git init` · pre-commit 훅 · `install-hooks`가 `core.hooksPath` 설정.

#### macOS

1. **Python 3.8+** — [python.org](https://www.python.org/downloads/) 또는 `brew install python`  
   - 터미널에서 **`python3`** 가 PATH에 있어야 한다. (`python`만 있거나 없으면 `install-hooks` 전에 확인)  
2. **Git** — Xcode Command Line Tools (`xcode-select --install`) 또는 Homebrew `git`  
3. **Cursor** (또는 Claude Code / Codex / Antigravity) — Phase Gate **쓰기 차단**은 Cursor만 (`hooks.json`)

**PATH 확인 (새 터미널에서):**

```bash
python3 --version    # Python 3.8.x 이상
git --version
```

#### Windows

1. **Python 3.8+** — [python.org](https://www.python.org/downloads/) 설치 시  
   - **“Add python.exe to PATH”**(또는 *Add Python to environment variables*) **반드시 체크**  
   - 설치 후 **CMD·PowerShell·Cursor 터미널을 새로 연다** (PATH 반영)  
   - 터미널에서 **`python`** 이 PATH에 있어야 한다. (`py -3`만 되는 경우도 있음 — `install-hooks`가 맞춤)  
2. **Git for Windows** — [git-scm.com](https://git-scm.com/download/win) (설치 시 “Git from the command line” 권장)  
3. **Cursor** — 훅·Agent Shell이 Python을 찾으려면 **Cursor를 Python 설치·PATH 설정 후** 실행하는 것이 안전하다  

**PATH 확인 (CMD 또는 PowerShell):**

```bat
python --version
git --version
```

`python`이 없고 `py`만 있을 때:

```bat
py -3 --version
```

→ `scripts\install-hooks.cmd` 실행 시 `hooks.json`에 쓸 명령을 OS에 맞게 잡는다. 그래도 Agent gate는 **`python scripts/_gate_cli.py`** 형식을 쓴다 (`py` 래퍼는 Agent Shell에서 불안정할 수 있음).

#### Linux

1. **Python 3.8+** — 배포판 패키지 (`python3`, `python3-pip` 등) 또는 pyenv  
   - **`python3`** 가 PATH에 있어야 한다  
2. **Git** — `git` 패키지  
3. **Cursor** 등 — 동일  

**PATH 확인:**

```bash
python3 --version
git --version
```

### PATH가 안 맞을 때 (공통)

| 증상 | macOS / Linux | Windows |
|------|---------------|---------|
| `python3` / `python` not found | Python 재설치 또는 PATH에 설치 경로 추가 | 설치 시 **Add to PATH** 다시 체크 후 터미널·Cursor 재시작 |
| Cursor 훅 실패 (exit 127) | `python3 scripts/cursor_hook.py gate_check` 수동 실행 | `python scripts/cursor_hook.py gate_check` — 실패하면 PATH |
| gate / install-hooks 실패 | `./scripts/install-hooks.sh` 대신 `python3 scripts/install_hooks.py` | `python scripts/install_hooks.py` |

**한 번 더:** 클론·복사 후 **`install-hooks`** 를 OS에 맞게 실행하면 Git pre-commit과 Cursor 훅용 Python 명령이 정리된다 (아래 표 참고).

---

폴더를 통째로 복사하면 **`.git`까지 같이 가서** 원래 원격(origin)에 연결된 채로 복제된다.  
새 프로젝트로 쓰려면 **git 이력을 끊고** 새로 시작하는 것이 맞다.

### 권장: 스크립트 한 번 (가장 쉬움)

템플릿 폴더(`default_ai`)에서:

**macOS / Linux / Git Bash**

```bash
./scripts/new-project.sh
# 또는
./scripts/new-project.sh ~/Desktop/my-new-project
```

**Windows (CMD)**

```bat
scripts\new-project.cmd
scripts\new-project.cmd C:\Users\you\Desktop\my-new-project
```

**Windows (PowerShell)**

```powershell
.\scripts\new-project.ps1
.\scripts\new-project.ps1 $env:USERPROFILE\Desktop\my-new-project
```

- **부모 폴더** (예: `~/Desktop` · `%USERPROFILE%\Desktop`)와 **새 프로젝트 이름**을 물어본다  
- **폴더가 없으면 생성**, **있으면 그 안에** 템플릿 복사 (이전 실패로 일부만 있어도 재실행 가능)  
- `.git` · `guide.md` · `.cursor/gate.json`(템플릿 개발 상태) 제외하고 복사  
- `git init` → 훅 설치 → gate status 까지 자동 실행  

### 클론만 한 경우 (한 번)

| OS | 명령 |
|----|------|
| macOS / Linux / Git Bash | `./scripts/install-hooks.sh` |
| Windows CMD | `scripts\install-hooks.cmd` |
| Windows PowerShell | `.\scripts\install-hooks.ps1` |

게이트 상태 확인:

| OS | 명령 |
|----|------|
| macOS / Linux / Git Bash | `./scripts/gate.sh status` |
| Windows CMD | `scripts\gate.cmd status` |
| Windows PowerShell | `.\scripts\gate.cmd status` |
| 공통 (Python) | `python scripts/_gate_cli.py status` |

`install-hooks`는 Git `core.hooksPath=.githooks` 설정과 Cursor 훅용 Python 명령(`python3` 또는 `python`)을 맞춘다.

### 수동 복사

Finder·탐색기·zip으로 폴더를 통째로 복사하면 `guide.md`도 **따라간다.**  
새 프로젝트에는 `guide.md`를 넣지 않는다. 사용법은 **원본 템플릿**의 `guide.md`를 연다.

**macOS / Linux (rsync 있을 때)**

```bash
rsync -a --exclude='.git' --exclude='guide.md' --exclude='.cursor/gate.json' \
  /path/to/default_ai/ /path/to/my-new-project/
cd /path/to/my-new-project
git init
./scripts/install-hooks.sh
./scripts/gate.sh status
```

**Windows (탐색기 또는 PowerShell)**

1. 템플릿 폴더 내용을 새 폴더에 복사한다.  
2. **제외:** `.git` 폴더 · `guide.md` · `.cursor/gate.json`  
3. 새 폴더에서:

```powershell
git init
.\scripts\install-hooks.ps1
.\scripts\gate.cmd status
```

이미 통째로 복사했다면 새 폴더에서 `guide.md`를 삭제하면 된다.

이미 `.git`이 포함된 채로 복사했다면:

```bash
cd /path/to/my-new-project   # Windows: cd C:\path\to\my-new-project
rm -rf .git                  # Windows PowerShell: Remove-Item -Recurse -Force .git
git init
# 필요하면: git remote add origin <새-원격-URL>
./scripts/install-hooks.sh   # Windows: scripts\install-hooks.cmd
./scripts/gate.sh status     # Windows: scripts\gate.cmd status
```

- `enabled: false` → 작은 작업은 게이트 없이 진행 가능  
- **쓰는 도구로** 이 폴더를 연다 (Cursor Agent / Claude Code / Codex / Antigravity)  
- Large에서는 **채팅 선택**(버튼 또는 번호)으로 승인·단계 전진하는 것이 기본이다  
- **Windows에서 Cursor Agent**가 gate를 돌릴 때는 `./scripts/gate.sh` 대신 `python scripts/_gate_cli.py <명령>` 을 쓴다 (PowerShell/CMD).

스킬은 클론만 하면 붙는다 (설치 스크립트 없음).

| 도구 | 스킬 경로 |
|------|-----------|
| Cursor | `.cursor/skills/` |
| Claude Code | `.claude/skills/` |
| Codex, Antigravity | `.agents/skills/` |

쓰기 차단 훅(`.cursor/hooks.json`)은 **Cursor만**. 다른 도구는 규칙 + gate CLI + git pre-commit.

### 선택 UI가 버튼으로 안 보일 때

결정 메뉴는 **구조화 질문 도구가 있으면** 클릭 카드, **없으면 한글 번호** `1` / `2` / `3` 이다. 가짜 버튼을 만들지 않는다.

- **Cursor:** 가능하면 `AskQuestion`. Grok·Auto가 Grok이면 번호로 나올 수 있다. 버튼을 쓰려면 Composer / Claude / GPT로 바꾼다.
- **Claude Code:** `AskUserQuestion`이 있으면 카드, 없으면 번호.
- **Codex · Antigravity:** 보통 번호 텍스트. `1` / `2` / `3`으로 고르면 게이트는 같다.

---

## 2. 역할

### 2-1. 사람 ↔ AI

| 사람 | AI |
|------|-----|
| 무엇을 만들지, 필수 기능 확정 | Plan 초안, 구현, 자동 테스트 |
| Plan / 단계 / Phase를 **채팅에서 선택·승인** (버튼 또는 번호) | 선택에 맞춰 `./scripts/gate.sh` 대행 |
| Guide대로 **직접** 테스트·검수 | User Test Guide · 리뷰 초안 |
| (선택) 터미널에서 동일 `gate.sh` 직접 실행 | `gate.json` **직접** 수정 · **선택 없는** 자가 승인 **금지** |

### 2-2. 시니어 역할 (한 채팅 · 전문 에이전트)

사람은 **채팅 하나**. 단계가 되면 **오케스트레이터**가 해당 전문 에이전트를 띄운다.  
역할 Skill(`senior-*`)은 Quality bar다. 기획·설계·디자인·개발·QA **본문은 그 에이전트**가 쓴다. 오케스트레이터가 Skill만 바꿔 본문을 쓰는 것은 실패다.  
**건너뛰기 금지:** gate enabled 시 **단계마다** 해당 전문 에이전트 산출물 + `approve-*` 없이는 다음 step·코드·커밋 **훅 차단**. UI Phase는 `approve-design-spec` 포함. Verify 통과는 `approve-verify` → `allow-commit`.  
Marketplace에 봇을 여러 개 설치하는 구조는 아니다. spawn이 안 되면 Isolation Pass(`▶ 전문 에이전트 시작`)로 같은 흐름을 유지한다.  
AI 응답에 `역할: 시니어 ○○`이 붙는 것이 정상이다. 각 역할 Skill의 **Quality bar**를 충족해야 한다.

| Skill / 에이전트 | 한글 | 언제 주로 |
|------------------|------|-----------|
| `senior-architect` | 시니어 설계 | Explore, 구조·보안 |
| `senior-pm` | 시니어 기획 | 킥오프·Plan, 범위 |
| `senior-design` | 시니어 디자인 | **Plan(UI면 필수)** 시각 스펙 — 생략 불가 |
| `senior-dev` | 시니어 개발 | Implement |
| `senior-qa` | 시니어 QA | Verify·Review |

에이전트 파일: `.cursor/agents/` · `.claude/agents/` · `.agents/agents/` · `.codex/agents/`

| 6단계 | 띄울 에이전트 |
|--------|----------------|
| Explore | 설계 |
| Document | 설계 또는 기획 |
| Plan | 기획 → (UI면) 디자인 |
| Implement | 개발 (디자인 스펙 준수) |
| Verify | QA |
| Review | QA → 설계 |

상세 표·산출물: [`docs/ai/agent-workflow.md`](docs/ai/agent-workflow.md) 「역할 Skill」.  
Skill 목록: [`.cursor/skills/README.md`](.cursor/skills/README.md).

### 2-3. 역할 명시 호출 (Large / Medium / Small)

사용자가 채팅에서 역할을 **직접 지정**하면, 오케스트레이터는 **그 전문 에이전트만** 띄운다.  
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

- **Q. 이 화면을 디자이너 에이전트가 했나?** → UI가 있는 Phase면 **Plan에서 디자인 에이전트**가 시각 스펙을 내고, **개발 에이전트**가 그걸 구현한 것이 정상이다. 오케스트레이터가 한 응답에서 기획+디자인+코드를 섞었으면 실패.  
- **Q. 기획은 기획 에이전트가 했나?** → 킥오프 K1·K4와 Delivery Plan에서 **기획 에이전트**가 본문을 쓴 것이 정상이다.  
- **Q. 역할을 안 쓰면?** → Large Phase면 단계 기본 에이전트. Small이면 보통 개발 중심으로 처리.  
- **Q. 여러 역할을 한 번에?** → 가능하면 하나만. 필요하면 “설계 후 QA”처럼 **순서**를 적는다.  
- **Q. Small인데 게이트는?** → 보통 `off`. 역할 지정과 게이트는 별개다.  
- **Q. 그림·설계 파일은 어디?** → 그림은 **선택 버튼(또는 번호 메뉴) 바로 위**, 그 답변 안에 그린 Mermaid. 새 창이 아닙니다. 파일은 에디터에서 AI가 적어 준 경로 (Cursor는 `Cmd+P`/`Ctrl+P`).  
- **Q. 질문을 한 번에 여러 개?** → K1은 **하나씩**. 대신 턴이 더 길다(후속·체크리스트). 「제안해」를 고르면 된다.  
- **Q. 개발 언어는 누가 정하나?** → **사람**. 기획·설계가 끝난 뒤, **구현 직전**에 `어떤 프론트…` / `어떤 백엔드…` / `어떤 DB…`를 **하나씩** 번호로 고른다. **선택지는 프로젝트마다 다름**(웹/앱/CLI/API 등 설계·Constraints 기준). AI가 Next.js 등을 미리 고르면 실패. 「제안해」면 **그 목록 안** 항을 추천하고 확인.  
- **Q. 디자인을 건너뛰면?** → **UI Phase면 불가.** Plan에서 `senior-design` 시각 스펙 → 사람 승인 → `approve-design-spec` → implement. gate·훅이 코드 쓰기를 막는다. `.cursor/skills/` 없으면 규칙만 있고 **강제는 안 됨** — 템플릿 전체 복사 필수.

---

## 3. 새 프로젝트 (Large) — 권장 순서

바로 Phase Plan을 받지 않는다. **질문 → 전체 설계 합의 → docs → Phase Plan** 순이다.  
AI Skill: `project-kickoff` (자동 또는 명시).

### 3-0. 시작 — 무엇을 만들지 이렇게 적어 주세요

첫 메시지에 아래를 적으면 됩니다. **모르는 칸은 비워 두거나 “모르겠어, 제안해”** 라고 쓰면 됩니다.  
AI는 킥오프를 시작할 때 이 안내를 먼저 보여 준 뒤, 질문을 합니다.

```text
만들고 싶은 것: (누구를 위한 어떤 제품인지 한두 문장)
꼭 있어야 하는 기능:
-
지금은 안 해도 되는 것:
-
누가 쓰나: (역할·상황. 없으면 “모르겠어”)
잘 됐을 때 / 실패·빈 화면: (한 줄씩. 없으면 “모르겠어”)
화면: 웹 / 앱 / 둘 다 / 화면 없음 / 잘 모르겠음
로그인·저장할 데이터: (있으면) / 없음 / 모르겠음
알고 있는 제약: (기한 등. 없으면 생략)
```

언어(프론트·백엔드·DB)는 여기 적어도 되고, 비우면 **기획·설계가 끝난 뒤 구현 직전**에 번호로 고릅니다.

이미 자유롭게 설명해 주셨으면 그걸 기준으로 이어갑니다. 양식을 다시 붙여 넣을 필요는 없습니다.

설계·기획이 나온 단계마다 채팅 **그 답변 안에** 한눈 그림이 있어야 합니다.  
질문만 하고 그림이 없으면 잘못된 것입니다. Mermaid가 안 그려져도 **글 흐름:** `A → B → C` 한 줄은 보여야 합니다.

| 단계 | 그림 |
|------|------|
| K1 질문·이해 | 지금까지 이해한 흐름 (사람 → 하는 일 → 결과). 미정은 “미정” 노드 |
| K2 전체 설계 | 저니 또는 시스템 (누가 → 무엇 → 어디) |
| K3 문서화 | K2와 **같은** 그림 |
| K4 Phase Plan | Phase 1→N |
| Explore | 이 Phase 이해·영향 |
| Document | 문서에 넣은 그림 (Explore와 같거나 변경분) |
| Plan | **이 Phase** 작업 순서 |

### 3-1. 질문 라운드 (K1)

새 Chat에서. 기능이 비어 있어도 된다. §3-0을 붙여도 되고, 아래처럼 킥오프만 요청해도 된다.

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

AI는 먼저 §3-0 시작 가이드를 보여 준 뒤, **질문 하나씩** 한다 (한 메시지에 질문 하나). 모르면 「제안해」를 고르면 된다.  
답을 받은 다음 질문에 반영한다. 답이 흐리면 **같은 주제로 한 번 더** 묻는다. 6개를 한 번에 나열하지 않는다.  
질문은 넓은 한두 개가 아니라, 설계에 필요한 구멍을 메운다. 예: 누구용, 성공이 뭔지, 지금 vs 나중, 화면 흐름, 빈 화면·에러, 로그인·데이터, 안 하는 것.  
첫 설명에 이미 **구체적으로** 나온 것은 건너뛴다. 대략 8–14턴(후속 포함).  
프론트·백엔드·DB 언어는 K1에서 묻지 않는다. **구현해 주세요를 고른 뒤**, 코드를 쓰기 전에 번호로 하나씩 고른다.  
충분히 알면 이해 요약과 **한눈 그림**이 나온 뒤, 설계 초안으로 갈지 묻는다.

### 3-2. 전체 설계 합의 (K2)

채팅 **메시지 바로 위(이 답변 안)** 한눈 그림과, AI가 적어 준 **지금 볼 곳** 경로를 에디터에서 연다 (파일 트리 또는 Cursor `Cmd+P` / `Ctrl+P`).  
보통 `.cursor/plans/<이름>-design.md`. 그림은 선택 카드 위 답변 안에 있고, 별도 앱이 아니다.  
읽은 뒤 선택 UI: 합의하고 문서화 / 설계 수정 / 보류.

### 3-3. docs 문서화 (K3)

같은 그림(채팅 안)과 **지금 볼 곳**의 `docs/product.md`, `docs/architecture.md` 등을 에디터에서 연다.  
읽은 뒤 선택 UI: Phase Plan 초안 작성 / 문서 수정 / 보류.

### 3-4. Phase Plan 검토 후 채팅에서 선택 (K4)

1. 채팅 안의 **Phase 한눈 그림**(1→N)과 **지금 볼 곳**의 Plan 파일(`.cursor/plans/<이름>.md`)을 에디터에서 연다  
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
| 1 | Explore | 설계 | `코드 작성하지 말고 이해해` | **한눈 그림** 확인 |
| 2 | Document | 설계/기획 | `이해한 내용을 문서화해` | 그림+docs 확인 |
| 3 | Plan | 기획 → (UI면) 디자인 | `이 기능을 어떻게 구현할지 계획해` | **한눈 그림**+파일 확인 후 **메뉴에서 선택** |
| 4 | Implement | 개발 | (승인 후) 스택 미정이면 프론트→백→DB 번호 선택, 그다음 구현 | 실행 가능하면 **실행 가이드**로 켜 보기 |
| 5 | Verify | QA | `테스트하고 검증해. 직접 확인 가이드도 줘` | **직접 확인 가이드**대로 실행·확인 후 **메뉴에서 선택** |
| 6 | Review | QA+설계 | `다시 리뷰해` | 검수 결과를 **메뉴에서** 선택 |

마지막 Phase면 Verify 채팅 순서는 **실행 가이드** → **역할 기여** → **직접 확인 가이드**.

결정 지점마다 AI는 선택 UI(가능하면 버튼)를 낸다. 사용자가 고르기 전에 게이트를 전진하거나 구현하지 않는다.  
응답에 **지금 역할**(`역할: 시니어 ○○`)이 보여야 한다.

**gate enabled일 때 단계별 승인 (훅 강제):**

| 단계 | 에이전트 | 사람 승인 → gate |
|------|----------|------------------|
| Explore | 설계 | `approve-explore` → `advance document` |
| Document | 설계/기획 | `approve-document` → `advance plan` |
| Plan | 기획 → (UI) 디자인 | `approve-plan-body` → (UI) `approve-design-spec` → `advance implement` |
| Implement | 개발 | (Stack pick) → `advance verify` |
| Verify | QA | `approve-verify` → (통과 시) `allow-commit` |
| Review | QA→설계 | Human Verify → `next-phase` |

AI Skill: `delivery-phase` (+ 단계별 `senior-*`).

### 3-6. 구현 직전 — 개발 언어 고르기 (Stack pick)

**언제:** 기획·설계(K1–K4)와 이 Phase **상세 Plan 승인**이 끝난 뒤, **첫 코드를 쓰기 직전**.  
K1(질문 라운드)에서는 프론트·백·DB를 묻지 않는다.

**흐름:** `이 상세 계획을 승인하고, 이제 구현해 주세요`(§4 ④-1) → AI가 **한 번에 하나씩** 번호 메뉴를 낸다 → 세 줄이 채워진 뒤에만 Implement.

**목록은 프로젝트마다 다르다.** K1–K4·설계·Constraints(플랫폼·클라이언트·배포·연동)를 보고 **이번 제품에 맞는** 후보만 4–6개 번호로 낸다. 매번 React/Next/PostgreSQL 고정 세트를 쓰지 않는다.

**예 — 웹 SaaS (재고 관리):**

```text
이 프로젝트는 브라우저 웹 SaaS이므로 아래 중에서 고릅니다.

어떤 프론트 개발 언어로 개발할까요?
1. TypeScript + Next.js (SSR·라우팅 내장)
2. TypeScript + React (Vite)
3. TypeScript + Vue (Nuxt)
4. 없음 (화면 없음)
5. 제안해
```

**예 — iOS·Android 앱 (오프라인 메모):**

```text
이 프로젝트는 모바일 앱(스토어 배포)이므로 아래 중에서 고릅니다.

어떤 프론트 개발 언어로 개발할까요?
1. React Native (iOS·Android 공통)
2. Flutter
3. SwiftUI (iOS) + Kotlin Compose (Android) — 각각 네이티브
4. 없음
5. 제안해
```

백엔드·DB도 같은 방식으로 **맥락에 맞게** 만든다. API-only면 Frontend 질문을 생략하고 `없음`으로 기록한다.

- **한 메시지에 질문 하나.** 세 가지를 한 번에 나열하지 않는다.  
- **제안해**를 고르면 AI가 **그 목록 안**에서 하나를 추천하고, 같은 주제로 다시 확인한다.  
- 고른 값은 설계 파일 `Stack`과 `docs/architecture.md`에 적힌 뒤 구현한다.  
- AI가 설계와 무관한 스택을 **사람 선택 없이** 정하면 실패.  
- Small·Medium에서도 **새 앱 코드를 처음 넣을 때** Stack이 비어 있으면 같은 순서로 고른다 (§5).

### 3-7. 실행 가이드 (개발이 끝난 뒤)

검수 시나리오와 별개다. **결과물을 어떻게 켜고 접속하는지**를 남긴다.

구현이 실행 가능한 산출물을 만들었으면 AI는 채팅과 `README.md` / `docs/development.md`에 실제 명령을 적는다 (추측 금지, secret 금지).

```
## 실행 가이드
- 준비: (런타임, 설치)
- 실행: (복사해 붙일 명령)
- 접속: (URL / 화면)
```

실행할 앱이 없는 Phase는 “이 Phase는 실행 대상 없음” 한 줄이면 된다.

### 3-8. 역할 기여 (개발이 끝난 뒤)

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

1. **구조화 질문 도구 사용 가능** (`AskQuestion` / `AskUserQuestion` 등) → 한글 옵션으로 **클릭 가능한 선택 카드** (한 메시지에 질문 하나)  
2. **불가** (Grok, Codex, Antigravity 등) → 아래와 같은 **한글 번호 텍스트 메뉴**로 대체  
3. 선택 전에는 게이트 전진·구현 금지. 선택 후 해당 `gate.sh`만 실행하고 `status`로 짧게 보고  

### 4-2. 메뉴 문구 (한글 · 버튼/번호 공통)

화살표(→) 줄은 선택 시 돌아가는 게이트 동작이다.  
버튼 라벨도 **같은 한글 문장**을 쓴다.

**① 킥오프 K2 — 전체 설계 초안 후**

채팅 안의 한눈 그림 + **지금 볼 곳**(에디터에서 `.cursor/plans/…-design.md` 열기).  
AskQuestion: `바로 위 한눈 그림(이 답변에 그린 Mermaid)과, 에디터에서 <실제-경로> 를 연 뒤 어떻게 할까요?`

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

**④ Delivery Explore (코드 없이 이해) 후**

`역할: 시니어 설계` + 한눈 그림이 채팅에 있어야 한다.

1. Explore를 승인하고 Document(문서화)로 진행해 주세요  
   → `approve-explore` → `advance document`  
2. Explore 내용을 수정해 주세요  
3. 지금은 보류할게요  

**⑤ Delivery Document 후**

1. Document를 승인하고 Plan(상세 계획)으로 진행해 주세요  
   → `approve-document` → `advance plan`  
2. Document를 수정해 주세요  
3. 지금은 보류할게요  

**⑥ 이 Phase의 상세 구현 계획(Plan)을 받은 뒤**

채팅 안의 **이 Phase 한눈 그림**과 **지금 볼 곳**의 Plan 파일을 에디터에서 연다.  
`역할: 시니어 기획` (+ UI면 `역할: 시니어 디자인` 시각 스펙)이 있어야 한다.  
AskQuestion: `바로 위 한눈 그림(이 답변에 그린 Mermaid)과, 에디터에서 <Plan 경로> 를 연 뒤 어떻게 할까요?`

1. 이 상세 계획을 승인하고, 이제 구현해 주세요  
   → `approve-plan-body`  
   → **UI Phase:** `approve-design-spec`  
   → `advance implement`  
   → Stack 미정이면 §3-6 **프론트 → 백엔드 → DB** → **`senior-dev`**만  
2. 상세 계획을 수정해 주세요 (구현은 아직 하지 않음)  
3. 지금은 보류할게요  

**⑦ 검증(Verify) / 리뷰(Review) 후, 내가 테스트까지 해본 뒤**

채팅의 **직접 확인 가이드**(실행·확인·기대)대로 직접 해본다.  
마지막 Phase면 그 위에 **실행 가이드**(준비·실행·접속)와 **역할 기여**(누가 무엇을·어디에 쓰이는지)가 있어야 한다.  
AskQuestion: `Phase N을 직접 플레이해 보신 결과는 어떤가요?`  
(화면이 없는 Phase는 `직접 확인해 보신 결과는 어떤가요?`)

채팅 메뉴에는 **커밋 항목이 없다.** `git commit`은 내가 직접 한다.

1. 직접 확인해 보니 통과예요  
   → `approve-verify` → `allow-commit` (`git commit`은 내가 직접)  
2. 아직 문제 있어요. 같은 Phase에서 고치고 검증을 다시 해 주세요  
3. 이 Phase는 통과. 다음 Phase로 가고, 지금은 조사(Explore)만 해 주세요  
   (마지막 Phase이면: 이 Phase는 통과. 전체 개발을 마무리해 주세요)

3번(다음 Phase)은 `next-phase` 후 Explore만.  

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
**새 앱 코드를 처음 넣을 때** Stack이 미정으면, Large와 같이 프론트 → 백엔드 → DB를 번호로 고른 뒤에만 구현한다.

---

## 6. 중간 크기 (Medium)

Explore → 짧은 Plan → Implement → Verify.  
긴 Phase 분할·게이트는 필수가 아니다. 필요할 때만 `on` 한다.  
단계마다 역할을 바꾸거나, §2-3처럼 한 역할만 명시해도 된다.  
구현 전 Stack이 미정으면 프론트 → 백엔드 → DB를 하나씩 고른다.

---

## 7. 템플릿에 들어 있는 것

| 종류 | 위치 |
|------|------|
| Rules | `.cursor/rules/`, `AGENTS.md` |
| Skills | `.cursor/skills/` (`project-kickoff`, `delivery-phase`, `phase-gate` + `senior-*`) |
| Agents | `.cursor/agents/` (복제: `.claude/agents/`, `.agents/agents/`, `.codex/agents/`) |
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

**프로젝트 설명 → 질문 → 전체 설계 합의 → docs → 채팅 선택(버튼 또는 번호)으로 Phase Plan 승인 → Phase마다 6단계(오케스트레이터가 전문 에이전트를 띄움) → AI 검증 + 내가 테스트 → 선택으로 다음 진행.**  
수정이 필요하면 **수정 선택 + 고칠 내용**을 쓰면 된다. 버튼이 안 보이면 Cursor는 모델을 Composer/Claude/GPT로 바꾸거나, 모든 도구에서 번호 `1`/`2`/`3`으로 고른다.
