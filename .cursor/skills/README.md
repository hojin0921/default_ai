# Project Skills (Cursor)

이 템플릿에 포함된 Agent Skills. 저장소를 복사하면 프로젝트 스킬로 따라간다.

## 워크플로 (오케스트레이션)

| Skill | 언제 |
|-------|------|
| `project-kickoff` | 질문 → 전체 설계 합의 → docs → Phase Plan, 구현 금지 · 기획+설계 관점 |
| `delivery-phase` | Phase마다 6단계 진행 · 단계별 primary 역할 Skill 지정 |
| `phase-gate` | `gate.json` / `gate.sh` — 채팅 선택 후 대행 |

## 역할 (시니어 관점)

한 Agent + Skill 전환. 다중 봇이 아님. 상세 매핑: `docs/ai/agent-workflow.md` 「역할 Skill」.

| Skill | 한글 | 주로 |
|-------|------|------|
| `senior-architect` | 시니어 설계 | Explore, 구조·보안·영향 범위 |
| `senior-pm` | 시니어 기획 | 킥오프·Plan, 범위·수락 기준 |
| `senior-design` | 시니어 디자인 | 시각·레이아웃·정보구조·카피 |
| `senior-dev` | 시니어 개발 | Implement |
| `senior-qa` | 시니어 QA | Verify·Review·User Test Guide |

경로: `.cursor/skills/<skill-name>/SKILL.md`

잘못된 자동 선택 완화: `delivery-phase`가 현재 단계의 primary 역할을 **명시**한다.  
응답 관례: `역할: 시니어 ○○` 한 줄.  
각 Skill의 **Quality bar**를 충족할 것. 피상적 요약은 실패.  
**사용자 명시 호출**(“시니어 QA로만 …”)이 있으면 그 역할이 Role map보다 우선 — `guide.md` §2-3.

Cursor: Customize → Skills, 또는 Agent가 description 기준으로 자동 선택.
