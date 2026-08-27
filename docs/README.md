# Docs

사람과 AI가 프로젝트를 이해하기 위한 지식. 실제 secret은 적지 않는다.

| 파일 | 역할 | 상태 |
|------|------|------|
| `product.md` | 사용자·문제·필수 기능·저니 | K3 반영 (단계별 전문 에이전트) |
| `architecture.md` | 구조·데이터 흐름 | K3 목표 + Phase 1 Implement (에이전트 네 경로) |
| `development.md` | 로컬 실행·기여 | TODO |
| `testing.md` | 테스트 전략·명령 | TODO |
| `security.md` | 보안 원칙(값 제외) | K3 반영 (secret 없음·에이전트 입력 패키지·훅 범위) |
| `environment.md` | env 이름·설명 | TODO |
| `deployment.md` | 배포·CI | TODO |
| `decisions/` | 왜 그렇게 결정했는지 (ADR) | README만 |
| `ai/agent-workflow.md` | **사람** — 킥오프·Phase 검수·프롬프트 | K3 매핑. `guide.md` §2-2 등 옛 문구는 Phase 2 |

축: Rules · Skills · Hooks · Docs · Plans · Tests · **Human Review**.  
Skills = 워크플로 + **시니어 역할 Quality bar**. 실행은 단계별 **전문 에이전트**. 사람용 요약: `guide.md` §2-2.  
Large 킥오프: 질문 → 전체 설계 합의 → docs → Phase Plan. 그다음 Delivery Phase마다 6단계 + 사람 검수.  
강제 게이트: 채팅 선택 → `./scripts/gate.sh` (터미널 동등). 결정: `docs/decisions/001-kickoff-design-first.md`.  
템플릿 구조는 `TEMPLATE.md`. Skills 목록: `.cursor/skills/README.md`.

## Rules vs Docs

| Rules | Docs |
|-------|------|
| `security.mdc` — secret을 어떻게 다룰지 | `security.md` — 이 프로젝트의 보안 모델 |
| `testing.mdc` — 테스트를 어떻게 수행할지 | `testing.md` — 명령·폴더·전략 |
| `documentation.mdc` — 언제 Docs를 고칠지 | 각 Docs 본문 |

DB/API 전용 Docs·Rules는 프로젝트가 필요할 때 추가한다.
