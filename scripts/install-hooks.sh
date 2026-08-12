#!/usr/bin/env bash
# Point this repo at .githooks (phase-gate pre-commit).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

git config core.hooksPath .githooks
chmod +x .githooks/pre-commit scripts/gate.sh scripts/phase-gate-check.sh \
  scripts/install-hooks.sh scripts/_gate_cli.py \
  .cursor/hooks/gate-check.sh .cursor/hooks/protect-gate.sh 2>/dev/null || true

echo "Installed: core.hooksPath=.githooks"
echo "Phase gate CLI: ./scripts/gate.sh status"
git config --get core.hooksPath
