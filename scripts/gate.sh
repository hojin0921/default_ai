#!/usr/bin/env bash
# Phase gate controls. Prefer human chat choice → Agent runs this; terminal is equivalent.
# Do not edit .cursor/gate.json directly.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
export PYTHONPATH="${ROOT}/scripts${PYTHONPATH:+:$PYTHONPATH}"
PY="${ROOT}/scripts/_gate_cli.py"

usage() {
  cat <<'EOF'
Usage: ./scripts/gate.sh <command> [args]

  status                 Show current gate
  on                     Enable Large (kickoff_step=discover, design not approved)
  off                    Disable gate (Small work)
  approve-design         design_approved=true, kickoff_step=docs
  kickoff <step>         Set kickoff_step (discover|design|docs|phase_plan|done)
  approve-plan           requires design_approved; plan_approved=true, kickoff_step=done, step=explore
  approve-explore        senior-architect Explore approved (this Phase)
  approve-document       Document step approved (this Phase)
  approve-plan-body      senior-pm Plan body approved (this Phase)
  phase-ui true|false    Mark current Delivery Phase UI scope (Plan step)
  approve-design-spec    senior-design visual spec approved (requires phase_has_ui)
  approve-verify         senior-qa Verify approved (this Phase)
  advance <step>         Set step (explore|document|plan|implement|verify|review|human_verify)
  allow-commit           Allow git commit (requires verify_approved when enabled)
  deny-commit            Disallow git commit
  next-phase             phase+=1, step=explore (resets Phase delivery flags; writes .cursor/handoff.md)
  handoff                Regenerate .cursor/handoff.md from current gate (no advance)
  handoff-url            Print cursor deeplink for new Chat (stdout)

Enforcement source of truth: .cursor/gate.json
EOF
}

if [[ $# -lt 1 ]]; then
  usage
  exit 1
fi

exec python3 "$PY" "$@"
