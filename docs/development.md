# Development

<!-- 새 프로젝트: package.json / README / CI를 확인한 뒤 채운다. -->

## Prerequisites

<!-- TODO: 런타임, 패키지 매니저, 필수 도구 버전 -->

## AI template setup (once per clone)

```bash
./scripts/install-hooks.sh
./scripts/gate.sh status
```

- Skills: `.cursor/skills/`
- Hooks: `.cursor/hooks.json` (Phase Gate)
- Large 시: 채팅에서 승인 선택(또는 `./scripts/gate.sh on` → `approve-plan` → `advance` → `allow-commit`)

## Setup

<!-- TODO: 설치·환경변수·로컬 실행 절차 -->

## Common Commands

<!-- TODO: dev / build / lint / typecheck 명령. 테스트 상세는 docs/testing.md -->

## Testing

테스트 전략·구조·실행 명령은 `docs/testing.md`를 본다.
여기에는 개발 중 자주 쓰는 한두 개 명령만 적어도 된다.

<!-- TODO: 예) 관련 테스트만 실행하는 대표 명령 한 줄 -->

## Contribution Notes

<!-- TODO: 브랜치·PR·리뷰에서 지켜야 할 프로젝트 관례 -->
