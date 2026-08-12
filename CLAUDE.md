# Claude Code Instructions

공통 원칙: `AGENTS.md`. 사람용 협업 가이드: `docs/ai/agent-workflow.md`.
템플릿: `TEMPLATE.md`.

## Workflow

- Small → Implement→Verify / Medium → Explore 후 구현 / Large·킥오프 → 전체 Plan 후 **승인 전 구현 금지**.
- Delivery Phase는 6단계: Explore→Document→Plan→Implement→Verify(+User Test Guide)→Review. **단계·Phase 검수 전 다음 금지**.
- Cursor 템플릿: `.cursor/skills/`, `.cursor/hooks.json`, `.cursor/gate.json` + `./scripts/gate.sh` (Agent는 gate 전진 금지).
- Phase 0은 bootstrap 또는 Docs 비어 있음+초기/문서화일 때만.
- 관련 파일·관련 docs만. docs 전체 읽기 금지. secret 출력 금지.
- 구현 후 관련 테스트. 실패 무시 금지.
- 보고: 단계 결과, docs, 검증, User Test Guide, 리뷰, 남은 이슈.

## Bootstrap (Phase 0)

요청 시 코드 수정 없이: Discovery → docs 초안 → README 개요 → (필요 시) 전용 rules → 첫 Large면 plan Draft.

## Notes

`AGENTS.md` 우선. Docs/Rule 본문을 여기로 복사하지 않는다.
