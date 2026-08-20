#!/usr/bin/env python3
"""CLI for scripts/gate.sh — human advances the phase gate."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from lib.phase_gate import (  # noqa: E402
    VALID_KICKOFF_STEPS,
    VALID_STEPS,
    find_repo_root,
    load_gate,
    save_gate,
)


def main(argv: list[str]) -> int:
    root = find_repo_root(ROOT)
    if not argv:
        print("missing command", file=sys.stderr)
        return 1
    cmd = argv[0]

    if cmd == "status":
        print(json.dumps(load_gate(root), ensure_ascii=False, indent=2))
        return 0

    gate = load_gate(root)

    if cmd == "on":
        gate["enabled"] = True
        gate["plan_approved"] = False
        gate["design_approved"] = False
        gate["kickoff_step"] = "discover"
        gate["phase"] = int(gate.get("phase") or 1)
        gate["step"] = "explore"
        gate["allow_commit"] = False
        save_gate(gate, root)
        print(json.dumps(load_gate(root), ensure_ascii=False, indent=2))
        return 0

    if cmd == "off":
        gate["enabled"] = False
        gate["allow_commit"] = False
        save_gate(gate, root)
        print(json.dumps(load_gate(root), ensure_ascii=False, indent=2))
        return 0

    if cmd == "approve-design":
        if not gate.get("enabled"):
            gate["enabled"] = True
        gate["design_approved"] = True
        gate["kickoff_step"] = "docs"
        gate["plan_approved"] = False
        gate["allow_commit"] = False
        save_gate(gate, root)
        print(json.dumps(load_gate(root), ensure_ascii=False, indent=2))
        return 0

    if cmd == "kickoff":
        if len(argv) < 2:
            print(
                f"usage: gate.sh kickoff <{'|'.join(VALID_KICKOFF_STEPS)}>",
                file=sys.stderr,
            )
            return 1
        kstep = argv[1]
        if kstep not in VALID_KICKOFF_STEPS:
            print(f"invalid kickoff_step: {kstep}", file=sys.stderr)
            return 1
        gate["kickoff_step"] = kstep
        save_gate(gate, root)
        print(json.dumps(load_gate(root), ensure_ascii=False, indent=2))
        return 0

    if cmd == "approve-plan":
        if not gate.get("design_approved"):
            print(
                "approve-plan requires design_approved=true "
                "(run ./scripts/gate.sh approve-design first)",
                file=sys.stderr,
            )
            return 1
        if not gate.get("enabled"):
            gate["enabled"] = True
        gate["plan_approved"] = True
        gate["kickoff_step"] = "done"
        gate["step"] = "explore"
        gate["allow_commit"] = False
        save_gate(gate, root)
        print(json.dumps(load_gate(root), ensure_ascii=False, indent=2))
        return 0

    if cmd == "advance":
        if len(argv) < 2:
            print(f"usage: gate.sh advance <{'|'.join(VALID_STEPS)}>", file=sys.stderr)
            return 1
        step = argv[1]
        if step not in VALID_STEPS:
            print(f"invalid step: {step}", file=sys.stderr)
            return 1
        gate["step"] = step
        save_gate(gate, root)
        print(json.dumps(load_gate(root), ensure_ascii=False, indent=2))
        return 0

    if cmd == "allow-commit":
        gate["allow_commit"] = True
        save_gate(gate, root)
        print(json.dumps(load_gate(root), ensure_ascii=False, indent=2))
        return 0

    if cmd == "deny-commit":
        gate["allow_commit"] = False
        save_gate(gate, root)
        print(json.dumps(load_gate(root), ensure_ascii=False, indent=2))
        return 0

    if cmd == "next-phase":
        gate["phase"] = int(gate.get("phase") or 1) + 1
        gate["step"] = "explore"
        save_gate(gate, root)
        print(json.dumps(load_gate(root), ensure_ascii=False, indent=2))
        return 0

    print(f"unknown command: {cmd}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
