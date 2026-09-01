#!/usr/bin/env python3
"""Copy this template into a new project folder (cross-platform)."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from lib.python_exec import resolve_python_argv  # noqa: E402

EXCLUDE_NAMES = frozenset({".git", "guide.md"})
EXCLUDE_REL = frozenset({".cursor/gate.json"})


def expand_path(raw: str) -> Path:
    text = raw.strip().strip('"').strip("'")
    text = os.path.expanduser(text)
    return Path(text).resolve()


def should_exclude(src: Path, rel: Path) -> bool:
    parts = rel.parts
    if parts and parts[0] in EXCLUDE_NAMES:
        return True
    rel_posix = rel.as_posix()
    if rel_posix in EXCLUDE_REL:
        return True
    if "__pycache__" in parts:
        return True
    return False


def copy_template(template_root: Path, dest: Path) -> None:
    def ignore(directory: str, names: list[str]) -> set[str]:
        dir_path = Path(directory)
        ignored: set[str] = set()
        for name in names:
            rel = dir_path.relative_to(template_root) / name
            if should_exclude(template_root, rel):
                ignored.add(name)
        return ignored

    dest.mkdir(parents=True, exist_ok=True)
    for item in template_root.iterdir():
        rel = item.relative_to(template_root)
        if should_exclude(template_root, rel):
            continue
        target = dest / item.name
        if item.is_dir():
            shutil.copytree(item, target, dirs_exist_ok=True, ignore=ignore)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, target)


def prompt_destination() -> Path:
    print(f"템플릿: {ROOT}", file=sys.stderr)
    print("", file=sys.stderr)
    if os.name == "nt":
        default_parent = Path.home() / "Desktop"
        parent_hint = "%USERPROFILE%\\Desktop"
    else:
        default_parent = Path.home() / "Desktop"
        parent_hint = "~/Desktop"
    parent_raw = input(f"새 프로젝트를 만들 부모 폴더 (예: {parent_hint}): ").strip()
    parent = expand_path(parent_raw) if parent_raw else default_parent
    parent.mkdir(parents=True, exist_ok=True)
    name = input("새 프로젝트 폴더 이름 (예: my-new-project): ").strip()
    if not name:
        print("폴더 이름이 비어 있습니다.", file=sys.stderr)
        raise SystemExit(1)
    return parent / name


def run_install(dest: Path) -> None:
    py = resolve_python_argv()
    if os.name == "nt" and (dest / "scripts" / "install_hooks.py").is_file():
        subprocess.run([*py, "scripts/install_hooks.py"], cwd=str(dest), check=True)
    elif (dest / "scripts" / "install_hooks.py").is_file():
        subprocess.run([*py, "scripts/install_hooks.py"], cwd=str(dest), check=True)
    elif (dest / "scripts" / "install-hooks.sh").is_file():
        subprocess.run(["./scripts/install-hooks.sh"], cwd=str(dest), check=True)


def run_gate_status(dest: Path) -> None:
    py = resolve_python_argv()
    if os.name == "nt" and (dest / "scripts" / "gate.cmd").is_file():
        subprocess.run(["cmd", "/c", "scripts\\gate.cmd", "status"], cwd=str(dest), check=False)
    elif (dest / "scripts" / "gate.sh").is_file():
        subprocess.run(["./scripts/gate.sh", "status"], cwd=str(dest), check=False)
    else:
        subprocess.run([*py, "scripts/_gate_cli.py", "status"], cwd=str(dest), check=False)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Copy AI template into a new project folder.")
    parser.add_argument(
        "destination",
        nargs="?",
        help="Full path to the new project folder (created if missing).",
    )
    args = parser.parse_args(argv)

    dest = expand_path(args.destination) if args.destination else prompt_destination()

    if dest.exists() and not dest.is_dir():
        print(f"오류: 대상 경로에 같은 이름의 파일이 있습니다: {dest}", file=sys.stderr)
        return 1

    if dest.is_dir() and any(dest.iterdir()):
        print(f"안내: 기존 폴더에 템플릿 파일을 복사합니다 (같은 이름은 갱신): {dest}", file=sys.stderr)
    else:
        print(f"새 폴더 생성: {dest}", file=sys.stderr)

    print("")
    print(f"복사 중 → {dest}")
    copy_template(ROOT, dest)

    os.chdir(dest)
    print("")
    print("git init")
    if (dest / ".git").is_dir():
        print("안내: .git 이 이미 있습니다. git init 으로 재초기화합니다.", file=sys.stderr)
    subprocess.run(["git", "init"], check=True)

    print("")
    print("install hooks")
    run_install(dest)

    print("")
    print("gate status")
    run_gate_status(dest)

    gate_hint = (
        r".\scripts\gate.cmd on"
        if os.name == "nt"
        else "./scripts/gate.sh on"
    )
    print(
        f"""
완료: {dest}

다음:
  1. Cursor(또는 사용 도구)에서 위 폴더를 연다
  2. 사용법은 템플릿 guide.md — {ROOT / "guide.md"}
  3. Large 새 제품이면 Agent 채팅에서 킥오프(K1)부터. gate 켜기: {gate_hint}
"""
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
