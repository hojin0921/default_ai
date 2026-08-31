# Project Instructions

모든 AI Agent 최소 공통 원칙. 프로젝트 지식은 `docs/`에 둔다.

## General

- 기존 코드를 먼저 이해한 후 수정한다. 최소 범위만 변경한다.
- 관련 없는 파일은 수정하지 않는다. 불필요한 리팩터링을 하지 않는다.
- 기존 패턴을 우선 재사용한다. 새 dependency는 필요성 확인 후에만 추가한다.

## Development Workflow

- Small: 바로 구현·검증. Medium: 조사 후 구현. Large/킥오프: K1 질문 → K2 설계 합의 → K3 docs → K4 Phase Plan, 승인 전 구현 금지.
- Delivery Phase(특히 Phase 1)는 6단계 고정: Explore→Document→Plan→Implement→Verify(+User Test Guide)→Review. **단계·Phase 검수 전 다음으로 가지 않는다**.
- **Stack(프론트·백·DB)은 K1이 아니라 구현 직전**에 사람이 번호로 고른다 (`delivery-phase` Stack pick). **선택지는 설계·Constraints에 맞게 매번 다르게** 만든다. 미정이면 코드 금지. AI가 언어·DB를 침묵 선택하면 실패.
- Agent는 `gate.json` **직접** 수정 금지. mutating `gate.sh`는 **사람 채팅 선택 후에만** 대행 (선택 없이 전진 금지). 선택은 구조화 질문 도구(`AskQuestion` 등, 가능 시) 또는 한글 번호 텍스트. 터미널 직접 실행도 동등.
- Skills: `.cursor/skills/` (Cursor), `.claude/skills/` (Claude Code), `.agents/skills/` (Codex·Antigravity). 워크플로 3 + 시니어 역할 5. **세 경로 내용을 같게 유지**한다. Hooks: `.cursor/hooks.json` (Cursor). Large 강제 검사는 `.cursor/gate.json`.
- Delivery 단계마다 오케스트레이터가 해당 **전문 에이전트**를 띄운다 (`delivery-phase` Role map). **담당 산출물 대체 금지.** gate enabled 시 단계별 `approve-explore` / `approve-document` / `approve-plan-body` / `approve-design-spec`(UI) / `approve-verify` 없이 advance·코드·커밋 **훅 차단**. 사용자 명시 호출(“시니어 QA로만 …” 등)이 있으면 그 에이전트만. Quality bar는 `senior-*` Skill.
- Phase 0은 bootstrap 요청, 또는 제품 없이 Docs만 초기화할 때만. 제품 설명이면 킥오프 K1부터. 일반 작업은 Docs TODO로 막지 않는다.
- 관련 Docs·코드만 본다. docs 전체·프로젝트 전체를 읽지 않는다.
- 구현 후 관련 테스트를 실행한다. 실패를 무시·삭제·우회하지 않는다.
- 실행 가능한 산출물이 있으면 **실행 가이드**(준비·실행·접속)를 채팅과 README/`docs/development.md`에 남긴다.
- 마지막 Phase면 **역할 기여**(시니어 역할별 만든 것·어떻게 쓰이는지)를 채팅과 Phase Plan에 남긴다.

## Safety

- 사용자 변경사항을 임의로 되돌리지 않는다.
- secret/`.env` 실제 값을 코드·로그·채팅에 넣지 않는다.
- 파괴적 작업(삭제, DB/migration, dependency)은 주의한다.
- 커밋·푸시·배포는 사용자가 요청할 때만 한다.
- 제품·아키텍처·보안의 최종 판단을 대신하지 않는다.
