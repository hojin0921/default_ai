#!/usr/bin/env bash
# Human-only phase gate controls. Agent must not run mutating commands.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
export PYTHONPATH="${ROOT}/scripts${PYTHONPATH:+:$PYTHONPATH}"
PY="${ROOT}/scripts/_gate_cli.py"

usage() {
  cat <<'EOF'
Usage: ./scripts/gate.sh <command> [args]

  status                 Show current gate
  on                     Enable Large/kickoff gate (plan not approved)
  off                    Disable gate (Small work)
  approve-plan           plan_approved=true, step=explore, allow_commit=false
  advance <step>         Set step (explore|document|plan|implement|verify|review|human_verify)
  allow-commit           Allow git commit
  deny-commit            Disallow git commit
  next-phase             phase+=1, step=explore, allow_commit=false

Enforcement source of truth: .cursor/gate.json
EOF
}

if [[ $# -lt 1 ]]; then
  usage
  exit 1
fi

exec python3 "$PY" "$@"
