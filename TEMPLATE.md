# AI Project Template v1

복사해서 쓰는 **AI 개발 프로토콜** 템플릿.
문서를 많이 주는 것이 목표가 아니라, AI·사람이 같은 방식으로 일하게 하는 것이다.

```
Human(목표·단계 승인·사용자 테스트)
  → AI(Phase마다 Explore→Document→Plan→Implement→Verify→Review)
  → Code/Docs/Tests
```

## 6축

| 축 | 위치 | 목적 |
|----|------|------|
| Rules | `AGENTS.md`, `.cursor/rules/` | AI 행동 |
| Docs | `docs/` | 프로젝트 지식 |
| Plans | `.cursor/plans/` | 전체 Plan + Phase 상세 |
| Tests | AI 검증 + 사용자 테스트 가이드 | 검증 |
| Agent Workflow | `01-agent-workflow.mdc` | AI 작업 순서 |
| Human Review | 사람 + `docs/ai/agent-workflow.md` | 단계·Phase 승인·검수 |

핵심 흐름 (Large / 킥오프):

```
전체 Plan(Phase 1…N) → Human Review
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
├── TEMPLATE.md              # 이 파일
├── README.md                # 프로젝트 stub
├── .env.example / .gitignore / .cursorignore
├── .cursor/rules/           # 00-core, 01-agent-workflow, coding, testing, git, security, documentation
├── .cursor/plans/_template.md
├── docs/ ... + docs/ai/agent-workflow.md
└── src/.gitkeep
```

## Phase 0 조건

- bootstrap / docs 작성 요청 시
- Docs 비어 있음 **그리고** 초기·문서화 작업일 때

일반 Small은 Docs TODO로 막지 않는다.

## 사람 가이드

어떻게 시킬지·프롬프트 예시: `docs/ai/agent-workflow.md`

## Bootstrap

```text
Phase 0부터. 코드 수정 금지.
1. Discovery  2. docs 채우기  3. README 개요
4. 필요 시 전용 rules  5. 첫 Large면 plan(Draft)
```
