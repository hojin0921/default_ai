# Project Skills

이 템플릿에 포함된 Agent Skills. 저장소를 복사하면 프로젝트 스킬로 따라간다.

| 도구 | 경로 |
|------|------|
| Cursor | `.cursor/skills/<name>/SKILL.md` |
| Claude Code | `.claude/skills/<name>/SKILL.md` |
| Codex, Antigravity | `.agents/skills/<name>/SKILL.md` |

세 경로의 `SKILL.md`는 같게 유지한다. 이 README는 `.cursor/skills/`에만 있다.

## 워크플로 (오케스트레이션)

| Skill | 언제 |
|-------|------|
| `project-kickoff` | 질문 → 전체 설계 합의 → docs → Phase Plan, 구현 금지 · 기획+설계 관점 |
| `delivery-phase` | Phase마다 6단계 진행 · 단계별 전문 에이전트 spawn |
| `phase-gate` | `gate.json` / `gate.sh` — 채팅 선택 후 대행 |

## 역할 (시니어 에이전트)

한 채팅의 오케스트레이터가 단계마다 전문 에이전트를 띄운다. Skill은 Quality bar. 상세: `docs/ai/agent-workflow.md` 「역할 Skill」.

| Skill | 한글 | 주로 |
|-------|------|------|
| `senior-architect` | 시니어 설계 | Explore, 구조·보안·영향 범위 |
| `senior-pm` | 시니어 기획 | 킥오프·Plan, 범위·수락 기준 |
| `senior-design` | 시니어 디자인 | Plan(UI) 시각 스펙 |
| `senior-dev` | 시니어 개발 | Implement |
| `senior-qa` | 시니어 QA | Verify·Review·User Test Guide |
| `senior-security` | 시니어 보안 | Verify(코드 Phase)·마지막 Review branch 스캔 |

에이전트 정의: `.cursor/agents/` · `.claude/agents/` · `.agents/agents/` · `.codex/agents/`  
Quality bar: `.cursor/skills/<skill-name>/SKILL.md` (복제: `.claude/skills/`, `.agents/skills/`)

`delivery-phase`가 현재 단계의 에이전트를 **띄운다**. spawn이 없으면 Isolation Pass.  
응답 관례: `역할: 시니어 ○○`. Quality bar 미달이면 실패.  
**사용자 명시 호출**(“시니어 QA로만 …”)이 있으면 그 에이전트만 — `guide.md` §2-3.

Cursor: Customize → Skills, 또는 Agent가 description 기준으로 자동 선택.  
Claude Code / Codex / Antigravity: 위 경로의 스킬을 도구가 자동 로드.
