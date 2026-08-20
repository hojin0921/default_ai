# Claude Code Instructions

공통 원칙: `AGENTS.md`. 사람용 협업 가이드: `docs/ai/agent-workflow.md`.
템플릿: `TEMPLATE.md`.

## Workflow

- Small → Implement→Verify / Medium → Explore 후 구현 / Large·킥오프 → K1 질문 → K2 설계 합의 → K3 docs → K4 Phase Plan, **승인 전 구현 금지**.
- Delivery Phase는 6단계: Explore→Document→Plan→Implement→Verify(+User Test Guide)→Review. **단계·Phase 검수 전 다음 금지**.
- Cursor 템플릿: `.cursor/skills/` (kickoff / delivery-phase / phase-gate + senior-*), `.cursor/hooks.json`, `.cursor/gate.json` + `./scripts/gate.sh` (Agent는 사람 채팅 선택 후에만 gate.sh 대행; `gate.json` 직접 수정 금지). 단계마다 `역할: 시니어 ○○`.
- Phase 0은 bootstrap 또는 제품 없이 Docs만 초기화할 때만. 제품 설명이면 킥오프 K1부터.
- 관련 파일·관련 docs만. docs 전체 읽기 금지. secret 출력 금지.
- 구현 후 관련 테스트. 실패 무시 금지.
- 보고: 단계 결과, docs, 검증, User Test Guide, 실행 가이드(실행 가능 시), 역할 기여(마지막 Phase), 리뷰, 남은 이슈.

## Bootstrap (Phase 0)

요청 시 코드 수정 없이: Discovery → docs 초안 → README 개요 → (필요 시) 전용 rules.
제품 아이디어가 있으면 킥오프 K1(질문)부터.

## Notes

`AGENTS.md` 우선. Docs/Rule 본문을 여기로 복사하지 않는다.
