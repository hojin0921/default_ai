#!/usr/bin/env bash
# Shared commit gate check (git pre-commit / manual).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
export PYTHONPATH="${ROOT}/scripts${PYTHONPATH:+:$PYTHONPATH}"

exec python3 -c '
import sys
from lib.phase_gate import can_commit, find_repo_root, load_gate

gate = load_gate(find_repo_root())
if can_commit(gate):
    raise SystemExit(0)
print(
    "phase-gate: commit blocked.\n"
    f"  enabled={gate.get(\"enabled\")} plan_approved={gate.get(\"plan_approved\")} "
    f"phase={gate.get(\"phase\")} step={gate.get(\"step\")} allow_commit={gate.get(\"allow_commit\")}\n"
    "  Human: ./scripts/gate.sh allow-commit   (after Verify/User Test)\n"
    "  Or Small work: ./scripts/gate.sh off",
    file=sys.stderr,
)
raise SystemExit(1)
'
