# AI Project Template v1

복사해서 쓰는 **AI 개발 프로토콜** 템플릿.
Cursor의 **Rules · Skills · Hooks**(+ 선택 MCP)를 레포에 묶어,
사람·AI가 같은 Phase 워크플로로 일하게 한다.

```
Human(목표·단계 승인·사용자 테스트)
  → AI(Skills: kickoff / delivery-phase)
  → Hooks(gate) + Plans + Docs + Tests
```

## 6축 + 확장

| 축 | 위치 | 목적 |
|----|------|------|
| Rules | `AGENTS.md`, `.cursor/rules/` | AI 행동 |
| Skills | `.cursor/skills/` | 킥오프·Phase·gate 절차 |
| Hooks | `.cursor/hooks.json` | 구현/커밋/자가승인 차단 |
| Docs | `docs/` | 프로젝트 지식 |
| Plans | `.cursor/plans/` | 전체 Plan + Phase 상세 |
| Tests | AI Verify + User Test Guide | 검증 |
| Human Review | 사람 + `docs/ai/agent-workflow.md` | 승인·검수 |

Plugins에 해당하는 것: **이 레포 전체를 템플릿으로 복사**하면 Skills+Hooks+Rules가 함께 간다.
(나중에 Cursor Marketplace Plugin으로 재패키징 가능.)

핵심 흐름 (Large / 킥오프):

```
전체 Plan(Phase 1…N) → Human Review (+ gate approve-plan)
  → Phase N: Explore → Document → Plan → (승인)
             → Implement → Verify(+User Test Guide) → Review
             → Human Verify
  → 다음 Phase …
```

Small은 Implement→Verify만. Medium은 Explore 후 짧은 Plan.
Phase 0 = bootstrap. Delivery Phase는 1부터, 진행 시 6단계 필수.

## 디렉터리

```
├── AGENTS.md / CLAUDE.md
├── TEMPLATE.md
├── README.md
├── .env.example / .gitignore / .cursorignore
├── .cursor/
│   ├── rules/
│   ├── skills/          # project-kickoff, delivery-phase, phase-gate
│   ├── hooks.json + hooks/   # gate-check, protect-gate
│   ├── gate.json
│   └── plans/_template.md
├── .githooks/pre-commit
├── scripts/gate.sh, install-hooks.sh, phase-gate-check.sh
├── docs/ ... + docs/ai/agent-workflow.md
└── src/.gitkeep
```

## 클론 후 한 번

```bash
./scripts/install-hooks.sh
./scripts/gate.sh status   # 기본 enabled:false (Small 마찰 없음)
```

Large 시작 시: `./scripts/gate.sh on` → Plan 검토 → `./scripts/gate.sh approve-plan`

## Phase 0 조건

- bootstrap / docs 작성 요청 시
- Docs 비어 있음 **그리고** 초기·문서화 작업일 때

일반 Small은 Docs TODO로 막지 않는다.

## 사람 가이드

- 사용법 요약: [`가이드.md`](가이드.md)
- 프롬프트·게이트 상세: `docs/ai/agent-workflow.md`
