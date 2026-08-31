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
    can_advance_to,
    find_repo_root,
    load_gate,
    reset_phase_delivery_flags,
    save_gate,
)

_ADVANCE_CHECK_STEPS = frozenset(
    {"document", "plan", "implement", "verify", "review", "human_verify"}
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
        reset_phase_delivery_flags(gate)
        gate["kickoff_step"] = "discover"
        gate["phase"] = int(gate.get("phase") or 1)
        gate["step"] = "explore"
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
        reset_phase_delivery_flags(gate)
        save_gate(gate, root)
        print(json.dumps(load_gate(root), ensure_ascii=False, indent=2))
        return 0

    if cmd == "approve-explore":
        gate["explore_approved"] = True
        save_gate(gate, root)
        print(json.dumps(load_gate(root), ensure_ascii=False, indent=2))
        return 0

    if cmd == "approve-document":
        gate["document_approved"] = True
        save_gate(gate, root)
        print(json.dumps(load_gate(root), ensure_ascii=False, indent=2))
        return 0

    if cmd == "approve-plan-body":
        gate["plan_body_approved"] = True
        save_gate(gate, root)
        print(json.dumps(load_gate(root), ensure_ascii=False, indent=2))
        return 0

    if cmd == "phase-ui":
        if len(argv) < 2 or argv[1] not in ("true", "false"):
            print("usage: gate.sh phase-ui true|false", file=sys.stderr)
            return 1
        gate["phase_has_ui"] = argv[1] == "true"
        if not gate["phase_has_ui"]:
            gate["design_spec_approved"] = False
        save_gate(gate, root)
        print(json.dumps(load_gate(root), ensure_ascii=False, indent=2))
        return 0

    if cmd == "approve-design-spec":
        if not gate.get("phase_has_ui"):
            print(
                "approve-design-spec requires phase_has_ui=true "
                "(run ./scripts/gate.sh phase-ui true during Plan when UI is in scope)",
                file=sys.stderr,
            )
            return 1
        gate["design_spec_approved"] = True
        save_gate(gate, root)
        print(json.dumps(load_gate(root), ensure_ascii=False, indent=2))
        return 0

    if cmd == "approve-verify":
        gate["verify_approved"] = True
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
        if step in _ADVANCE_CHECK_STEPS:
            ok, msg = can_advance_to(gate, step)
            if not ok:
                print(msg, file=sys.stderr)
                return 1
        gate["step"] = step
        save_gate(gate, root)
        print(json.dumps(load_gate(root), ensure_ascii=False, indent=2))
        return 0

    if cmd == "allow-commit":
        if gate.get("enabled") and not gate.get("verify_approved"):
            print(
                "allow-commit requires verify_approved=true "
                "(run ./scripts/gate.sh approve-verify after senior-qa Verify)",
                file=sys.stderr,
            )
            return 1
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
        reset_phase_delivery_flags(gate)
        save_gate(gate, root)
        print(json.dumps(load_gate(root), ensure_ascii=False, indent=2))
        return 0

    print(f"unknown command: {cmd}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
