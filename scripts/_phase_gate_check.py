#!/usr/bin/env python3
"""Exit 0 if commit allowed, else 1 with message. Used by phase-gate-check.sh / pre-commit."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from lib.phase_gate import can_commit, find_repo_root, gate_cli_hint, load_gate  # noqa: E402


def main() -> int:
    gate = load_gate(find_repo_root(ROOT))
    if can_commit(gate):
        return 0
    print(
        "phase-gate: commit blocked.\n"
        f"  enabled={gate.get('enabled')} plan_approved={gate.get('plan_approved')} "
        f"phase={gate.get('phase')} step={gate.get('step')} allow_commit={gate.get('allow_commit')}\n"
        f"  After Verify/User Test: chat pick 통과 (Agent runs {gate_cli_hint()} allow-commit),\n"
        f"  or run that CLI, then git commit yourself.\n"
        f"  Or Small work: {gate_cli_hint()} off",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
