# AI Project Template v1

복사해서 쓰는 **AI 개발 프로토콜** 템플릿.
`AGENTS.md` · Skills · (Cursor면) Hooks를 레포에 묶어,
사람·AI가 같은 Phase 워크플로로 일하게 한다.

```
Human(목표·채팅 승인·사용자 테스트)
  → AI(Skills: kickoff / delivery-phase + senior-* 역할; 선택 후 gate.sh 대행)
    → Hooks(gate) + Plans + Docs + Tests
```

## 6축 + 확장

| 축 | 위치 | 목적 |
|----|------|------|
| Rules | `AGENTS.md`, `.cursor/rules/` | AI 행동 |
| Skills | `.cursor/skills/` · `.claude/skills/` · `.agents/skills/` (내용 동일) | 킥오프·Phase·gate + **시니어 역할** |
| Hooks | `.cursor/hooks.json` | 구현/커밋 차단 · `gate.json` 직접 수정 차단 |
| Docs | `docs/` | 프로젝트 지식 |
| Plans | `.cursor/plans/` | 전체 Plan + Phase 상세 |
| Tests | AI Verify + User Test Guide + 실행 가이드 | 검증·실행 |
| Human Review | 사람 + `docs/ai/agent-workflow.md` | 승인·검수 |

Skills는 워크플로(`project-kickoff` / `delivery-phase` / `phase-gate`)와 역할(`senior-architect` / `pm` / `design` / `dev` / `qa` / `security`)로 나뉜다.  
한 채팅의 오케스트레이터가 단계마다 전문 에이전트(`senior-*`)를 띄움. **담당 산출물 건너뛰기 금지** — Verify(코드 Phase)는 **`senior-security` Phase diff**, 마지막 Review는 **`senior-security` branch 전체**. gate enabled 시 `approve-explore` / … / `approve-verify` 후에만 advance·코드·커밋. 사람용: [`guide.md`](guide.md) §2-2 · §3-5.

Plugins에 해당하는 것: **이 레포 전체를 템플릿으로 복사**하면 Skills+Hooks+Rules가 함께 간다.
(나중에 Cursor Marketplace Plugin으로 재패키징 가능.)

핵심 흐름 (Large / 킥오프):

```
K1 질문 → K2 전체 설계 합의 → K3 docs → K4 Phase Plan
  → Human Review (채팅 선택 → gate approve-plan)
  → Phase N: Explore → Document → Plan (+ UI면 senior-design) → (채팅 승인 + approve-design-spec if UI)
             → Implement (senior-dev) → Verify (senior-qa → senior-security) → Review
             → (마지막 Phase Review: senior-security branch 전체) → Human Verify
  → 다음 Phase …
```

Small은 Implement→Verify만. Medium은 Explore 후 짧은 Plan.
Phase 0 = bootstrap (제품 없이 docs만). 제품 설명이면 킥오프 K1부터. Delivery Phase는 1부터, 진행 시 6단계 필수.

## 디렉터리

```
├── AGENTS.md / CLAUDE.md
├── TEMPLATE.md
├── README.md
├── .env.example / .gitignore / .cursorignore
├── .cursor/
│   ├── rules/
│   ├── skills/          # Cursor. 동일 내용: .claude/skills/ , .agents/skills/
│   ├── agents/          # 전문 에이전트. Claude: .claude/agents/ , Antigravity: .agents/agents/ , Codex: .codex/agents/
│   ├── hooks.json + hooks/   # gate-check, protect-gate (Cursor)
│   ├── gate.json
│   └── plans/_template.md, _design-template.md
├── .claude/skills/      # Claude Code
├── .claude/agents/
├── .agents/skills/      # Codex · Antigravity
├── .agents/agents/      # Antigravity
├── .codex/agents/       # Codex TOML
├── .githooks/pre-commit
├── scripts/gate.sh, gate.cmd, gate.ps1, install-hooks.sh, install-hooks.cmd,
│   install_hooks.py, new-project.sh, new-project.cmd, new_project.py,
│   phase-gate-check.sh, cursor_hook.py, _gate_cli.py
├── docs/ ... + docs/ai/agent-workflow.md
└── src/.gitkeep
```

## 클론 후 한 번

**macOS / Linux / Git Bash**

```bash
./scripts/install-hooks.sh
./scripts/gate.sh status   # 기본 enabled:false (Small 마찰 없음)
```

**Windows (CMD / PowerShell)**

```bat
scripts\install-hooks.cmd
scripts\gate.cmd status
```

공통: `python scripts/_gate_cli.py status`

Large: 채팅에서 Plan 승인(또는 동등하게 `./scripts/gate.sh on` → `approve-plan`)

## Phase 0 조건

- bootstrap / docs 작성 요청 시
- Docs 비어 있음 **그리고** 초기·문서화 작업일 때

일반 Small은 Docs TODO로 막지 않는다.

## 사람 가이드

- 사용법 요약: 원본 템플릿 [`guide.md`](guide.md) (권장: `new-project` 스크립트 — `guide.md`·`.cursor/gate.json` 제외 복사)
- 프롬프트·게이트 상세: `docs/ai/agent-workflow.md`
