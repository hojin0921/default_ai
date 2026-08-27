# Security

앱 인증·사용자 데이터는 없다. 프로토콜 레포 수준의 원칙만 둔다.

## Principles

- API key, password, token, secret을 스킬·docs·테스트·로그에 넣지 않는다.
- `.env` 실제 값을 읽거나 출력하지 않는다.
- Agent는 `.cursor/gate.json`을 직접 수정하지 않는다. 전진은 사람 선택 후 `./scripts/gate.sh`만.

## Secrets

이 템플릿은 secret 저장소가 없다. 복사한 프로젝트에서 쓰는 값은 환경변수 또는 secret manager. 값은 이 문서에 적지 않는다.

## AuthN / AuthZ

해당 없음 (앱 로그인 없음). 게이트는 개발 절차 잠금이지 인증이 아니다.

## Threat Notes

- 스킬 파일이 세 경로에 복제된다. 내용에 secret을 넣으면 유출면이 세 배가 되므로 스킬에는 비밀을 두지 않는다.
- 전문 에이전트 정의(`.cursor/agents/` 등)에도 secret을 넣지 않는다. 오케스트레이터가 자식에게 넘기는 입력 패키지에 `.env` 실제 값을 넣지 않는다.
- 전문 에이전트도 `.cursor/gate.json`을 직접 수정하지 않는다. mutating `gate.sh`는 사람 선택 후 오케스트레이터만.
- Cursor 밖에서는 `.cursor/hooks.json` 쓰기 차단이 없다. 구현 전 코드 쓰기는 규칙 + 사람 승인 + git pre-commit에 의존한다.

## Reporting

해당 없음.
