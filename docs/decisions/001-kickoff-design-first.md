# ADR-001: 킥오프는 질문 → 전체 설계 합의 → docs → Phase Plan

## Status

Accepted

## Context

템플릿 Large 킥오프는 프로젝트 설명만 받으면 `.cursor/plans/`에 Phase 분할 Plan을 바로 썼다.  
사람은 승인/수정 메뉴로만 고칠 수 있어, 전체 설계를 묻고 답하며 합의한 뒤 문서화하는 단계가 없었다.

## Decision

Large 킥오프를 Delivery Phase 1 전에 다음 순서로 둔다. Delivery 6단계 이름과 섞지 않는다.

| 단계 | 산출물 | 사람 |
|------|--------|------|
| K1 Discover | 질문·이해 요약 (Plan/docs 쓰기 금지) | 설계 초안 진행 / 더 질문 / 보류 |
| K2 Design | `.cursor/plans/<name>-design.md` | 설계 합의 / 수정 / 보류 |
| K3 Docs | `docs/product.md`, `docs/architecture.md` 등 | 문서 확인 후 Phase Plan / 수정 / 보류 |
| K4 Phase Plan | `.cursor/plans/<name>.md` (`_template.md`) | 전체 Plan 승인 후 Phase 1 Explore / 수정 / 보류 |

합의 후 **docs가 제품·구조의 진실 원천**이다. `*-design.md`는 합의 스냅샷이다.  
게이트 필드(`kickoff_step`, `design_approved`)와 `approve-design`은 별도 작업으로 넣는다.  
구현 시 고정할 점:

- Delivery `step`과 킥오프 단계를 섞지 않는다. `kickoff_step`은 별도 필드 (`discover|design|docs|phase_plan|done`).
- `save_gate`가 새 키를 버려서는 안 된다.
- 구 `gate.json`에 필드가 없으면: `plan_approved`이면 `design_approved=true`, `kickoff_step=done`.
- K2 합의 → `./scripts/gate.sh approve-design` (`design_approved=true`, `kickoff_step=docs`, 필요 시 게이트 on).
- K3 확인 → `./scripts/gate.sh kickoff phase_plan`.
- K4 승인 → `./scripts/gate.sh approve-plan`만. **`on`과 묶지 않는다** (`on`은 `design_approved`를 다시 false로 만든다).
- `approve-plan`은 `design_approved`가 true일 때만 성공한다.
- `on`은 Large 리셋: `kickoff_step=discover`, `design_approved=false`, `plan_approved=false`. phase 번호는 유지.
- docs/`plans` 쓰기는 훅으로 막지 않는다. 앱 코드 차단은 기존과 같다.

Small/Medium과 Delivery 6단계 순서는 바꾸지 않는다.

## Alternatives

- Skill만 바꾸고 게이트는 그대로 — 바로 Plan을 쓰는 행동이 남을 위험이 큼
- 킥오프 단계를 Delivery `step`(explore/document/…)에 섞음 — `explore` 의미가 이중이 됨

## Consequences

- `project-kickoff`가 Plan을 즉시 쓰면 안 된다
- Phase 1 Document는 기초 docs가 아니라 킥오프 K3 이후 **변경분**
- Phase 0은 제품 없이 bootstrap할 때만. 제품 설명으로 시작하면 킥오프 K1부터
- `documentation.mdc`의 “코드 확인 전 Docs 추측 금지”는 킥오프 K3(합의된 설계 기록)만 예외
