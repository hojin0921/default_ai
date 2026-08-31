#!/usr/bin/env bash
# Copy this template into a new project folder, then git init + hooks + gate status.
# Usage:
#   ./scripts/new-project.sh                          # prompts for path
#   ./scripts/new-project.sh /path/to/my-new-project  # non-interactive
set -euo pipefail

TEMPLATE_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

usage() {
  cat <<EOF
Usage: ./scripts/new-project.sh [DESTINATION]

  DESTINATION  Full path to the new project folder (created if missing).
               If omitted, prompts for parent directory and folder name.

Examples:
  ./scripts/new-project.sh
  ./scripts/new-project.sh "\$HOME/Desktop/my-new-project"

Excludes from copy: .git, guide.md, .cursor/gate.json (fresh gate defaults)
EOF
}

expand_path() {
  local p="$1"
  # shellcheck disable=SC2086
  p="${p/#\~/$HOME}"
  if [[ "$p" != /* ]]; then
    p="$(cd "$(dirname "$p")" 2>/dev/null && pwd)/$(basename "$p")" || p="$PWD/$p"
  fi
  printf '%s' "$p"
}

prompt_destination() {
  local parent name dest
  echo "템플릿: ${TEMPLATE_ROOT}" >&2
  echo "" >&2
  read -r -p "새 프로젝트를 만들 부모 폴더 (예: ~/Desktop): " parent
  parent="$(expand_path "$parent")"
  if [[ ! -d "$parent" ]]; then
    echo "부모 폴더 생성: $parent" >&2
    mkdir -p "$parent"
  fi
  read -r -p "새 프로젝트 폴더 이름 (예: my-new-project): " name
  name="${name#"${name%%[![:space:]]*}"}"
  name="${name%"${name##*[![:space:]]}"}"
  if [[ -z "$name" ]]; then
    echo "폴더 이름이 비어 있습니다." >&2
    exit 1
  fi
  dest="${parent%/}/${name}"
  printf '%s' "$dest"
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

if [[ $# -ge 1 ]]; then
  DEST="$(expand_path "$1")"
else
  DEST="$(prompt_destination)"
fi

if [[ -e "$DEST" && ! -d "$DEST" ]]; then
  echo "오류: 대상 경로에 같은 이름의 파일이 있습니다: $DEST" >&2
  exit 1
fi

if [[ -d "$DEST" ]]; then
  if [[ -n "$(ls -A "$DEST" 2>/dev/null)" ]]; then
    echo "안내: 기존 폴더에 템플릿 파일을 복사합니다 (같은 이름은 갱신): $DEST" >&2
  fi
else
  echo "새 폴더 생성: $DEST" >&2
fi

mkdir -p "$DEST"

echo ""
echo "복사 중 → $DEST"
rsync -a \
  --exclude='.git' \
  --exclude='guide.md' \
  --exclude='.cursor/gate.json' \
  "${TEMPLATE_ROOT}/" "${DEST}/"

cd "$DEST"

echo ""
echo "git init"
if [[ -d .git ]]; then
  echo "안내: .git 이 이미 있습니다. git init 으로 재초기화합니다." >&2
fi
git init

echo ""
echo "./scripts/install-hooks.sh"
./scripts/install-hooks.sh

echo ""
echo "./scripts/gate.sh status"
./scripts/gate.sh status

cat <<EOF

완료: $DEST

다음:
  1. Cursor(또는 사용 도구)에서 위 폴더를 연다
  2. 사용법은 템플릿 guide.md — ${TEMPLATE_ROOT}/guide.md
  3. Large 새 제품이면 Agent 채팅에서 킥오프(K1)부터. gate 켜기: ./scripts/gate.sh on

EOF
