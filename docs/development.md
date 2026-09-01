# Development

<!-- 새 프로젝트: package.json / README / CI를 확인한 뒤 채운다. -->

## Prerequisites

- **Python 3.8+** (gate CLI, Cursor hooks, git pre-commit)
- **Git**
- **Cursor** (선택: Phase Gate 쓰기 차단 훅). Claude Code / Codex / Antigravity는 규칙 + gate CLI + pre-commit.

## AI template setup (once per clone)

| OS | Install hooks | Gate status |
|----|---------------|-------------|
| macOS / Linux / Git Bash | `./scripts/install-hooks.sh` | `./scripts/gate.sh status` |
| Windows CMD | `scripts\install-hooks.cmd` | `scripts\gate.cmd status` |
| Windows PowerShell | `.\scripts\install-hooks.ps1` | `.\scripts\gate.cmd status` |
| Any (Python) | `python scripts/install_hooks.py` | `python scripts/_gate_cli.py status` |

- Skills: `.cursor/skills/` (동일 내용: `.claude/skills/`, `.agents/skills/`)
- Hooks: `.cursor/hooks.json` (Phase Gate; `python3` 또는 `python` — `install-hooks`가 OS에 맞게 설정)
- Large 시: 채팅에서 승인 선택. 킥오프는 `approve-design` → `kickoff phase_plan` → `approve-plan` (`on`과 `approve-plan`을 한 번에 묶지 않음). 이후 `advance`. 검증 통과 후 커밋 잠금 해제는 채팅 1번(통과) 또는 gate CLI `allow-commit`. `git commit`은 사람이 직접.
- **Windows Agent:** PowerShell/CMD에서는 `./scripts/gate.sh` 대신 `python scripts/_gate_cli.py <명령>` 사용.

## Setup

<!-- 실행 가능한 산출물이 생기면 실제 설치·환경변수 이름·로컬 실행 명령을 채운다. 추측 금지. secret 금지. -->

## Common Commands

<!-- TODO: dev / build / lint / typecheck 명령. 테스트 상세는 docs/testing.md -->

## Testing

테스트 전략·구조·실행 명령은 `docs/testing.md`를 본다.
여기에는 개발 중 자주 쓰는 한두 개 명령만 적어도 된다.

Gate 자체 검증 (템플릿 유지보수):

```bash
python3 scripts/_verify_phase_gate.py
```

Windows: `python scripts/_verify_phase_gate.py`

## Contribution Notes

<!-- TODO: 브랜치·PR·리뷰에서 지켜야 할 프로젝트 관례 -->
