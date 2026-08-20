# Project Instructions

모든 AI Agent 최소 공통 원칙. 프로젝트 지식은 `docs/`에 둔다.

## General

- 기존 코드를 먼저 이해한 후 수정한다. 최소 범위만 변경한다.
- 관련 없는 파일은 수정하지 않는다. 불필요한 리팩터링을 하지 않는다.
- 기존 패턴을 우선 재사용한다. 새 dependency는 필요성 확인 후에만 추가한다.

## Development Workflow

- Small: 바로 구현·검증. Medium: 조사 후 구현. Large/킥오프: 전체 Plan(Phases) 승인 전 구현 금지.
- Delivery Phase(특히 Phase 1)는 6단계 고정: Explore→Document→Plan→Implement→Verify(+User Test Guide)→Review. **단계·Phase 검수 전 다음으로 가지 않는다**.
- Skills: `.cursor/skills/` (kickoff / delivery-phase / phase-gate + senior-architect|pm|design|dev|qa). Hooks: `.cursor/hooks.json`. Large 강제 검사는 `.cursor/gate.json`.
- Delivery 단계마다 역할 Skill을 따른다 (`delivery-phase` Role map). 응답에 `역할: 시니어 ○○`을 밝힌다. 사용자 명시 호출(“시니어 QA로만 …” 등)이 있으면 그 역할이 Role map보다 우선.
- Agent는 `gate.json` **직접** 수정 금지. mutating `gate.sh`는 **사람 채팅 선택 후에만** 대행 (선택 없이 전진 금지). 선택은 `AskQuestion`(가능 시) 또는 한글 번호 텍스트. 터미널 직접 실행도 동등.
- Phase 0은 bootstrap 요청, 또는 Docs 비어 있음 + 초기/문서화일 때만. 일반 작업은 Docs TODO로 막지 않는다.
- 관련 Docs·코드만 본다. docs 전체·프로젝트 전체를 읽지 않는다.
- 구현 후 관련 테스트를 실행한다. 실패를 무시·삭제·우회하지 않는다.

## Safety

- 사용자 변경사항을 임의로 되돌리지 않는다.
- secret/`.env` 실제 값을 코드·로그·채팅에 넣지 않는다.
- 파괴적 작업(삭제, DB/migration, dependency)은 주의한다.
- 커밋·푸시·배포는 사용자가 요청할 때만 한다.
- 제품·아키텍처·보안의 최종 판단을 대신하지 않는다.
