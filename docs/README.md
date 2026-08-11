# Docs

사람과 AI가 프로젝트를 이해하기 위한 지식. 실제 secret은 적지 않는다.

| 파일 | 역할 | 상태 |
|------|------|------|
| `architecture.md` | 구조·데이터 흐름 | TODO |
| `development.md` | 로컬 실행·기여 | TODO |
| `testing.md` | 테스트 전략·명령 | TODO |
| `security.md` | 보안 원칙(값 제외) | TODO |
| `environment.md` | env 이름·설명 | TODO |
| `deployment.md` | 배포·CI | TODO |
| `decisions/` | 왜 그렇게 결정했는지 (ADR) | README만 |
| `ai/agent-workflow.md` | **사람** — 킥오프·Phase 검수·프롬프트 | 복사 유지 |

6축: Rules · Docs · Plans · Tests · Agent Workflow · **Human Review**.
Large는 Delivery Phase마다 6단계(Explore→Document→Plan→Implement→Verify→Review) + 사람 검수.
템플릿 구조는 `TEMPLATE.md`.

## Rules vs Docs

| Rules | Docs |
|-------|------|
| `security.mdc` — secret을 어떻게 다룰지 | `security.md` — 이 프로젝트의 보안 모델 |
| `testing.mdc` — 테스트를 어떻게 수행할지 | `testing.md` — 명령·폴더·전략 |
| `documentation.mdc` — 언제 Docs를 고칠지 | 각 Docs 본문 |

DB/API 전용 Docs·Rules는 프로젝트가 필요할 때 추가한다.
