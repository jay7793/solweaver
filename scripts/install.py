#!/usr/bin/env python3
"""Install Solweaver without overwriting existing Codex files."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import os
from pathlib import Path
import shlex
import shutil


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_NAME = "solweaver"


def paths_overlap(first: Path, second: Path) -> bool:
    """Return whether either resolved path contains the other."""
    first = first.resolve(strict=False)
    second = second.resolve(strict=False)
    try:
        first.relative_to(second)
        return True
    except ValueError:
        pass
    try:
        second.relative_to(first)
        return True
    except ValueError:
        return False


def unsafe_path_relationships(
    sources: tuple[Path, ...],
    install_targets: tuple[Path, ...],
    backup_root: Path,
) -> list[tuple[str, Path, Path]]:
    """Find source/write and write/write overlaps before any mutation."""
    conflicts: list[tuple[str, Path, Path]] = []
    mutable_paths = tuple(dict.fromkeys((*install_targets, backup_root)))
    for source in sources:
        for target in mutable_paths:
            if paths_overlap(source, target):
                conflicts.append(("source/write", source, target))
    for index, first in enumerate(mutable_paths):
        for second in mutable_paths[index + 1 :]:
            if paths_overlap(first, second):
                conflicts.append(("write/write", first, second))
    return conflicts


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Install Solweaver, its Terra/Luna workers, and final-strict reviewer."
    )
    parser.add_argument(
        "--codex-home",
        type=Path,
        default=Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")),
        help=(
            "Codex configuration directory for agents and backups "
            "(default: CODEX_HOME or ~/.codex)."
        ),
    )
    parser.add_argument(
        "--user-skills-dir",
        type=Path,
        default=Path.home() / ".agents" / "skills",
        help="User-global skills directory (default: ~/.agents/skills).",
    )
    parser.add_argument(
        "--upgrade",
        action="store_true",
        help="Back up and replace an existing Solweaver installation.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    codex_home = args.codex_home.expanduser().resolve(strict=False)
    user_skills_dir = args.user_skills_dir.expanduser().resolve(strict=False)

    sources = (
        (
            (REPO_ROOT / "skills" / SKILL_NAME).resolve(strict=False),
            (user_skills_dir / SKILL_NAME).resolve(strict=False),
            Path("user-skills") / SKILL_NAME,
        ),
        (
            (REPO_ROOT / "agents" / "terra-worker.toml").resolve(strict=False),
            (codex_home / "agents" / "terra-worker.toml").resolve(strict=False),
            Path("agents") / "terra-worker.toml",
        ),
        (
            (REPO_ROOT / "agents" / "luna-worker.toml").resolve(strict=False),
            (codex_home / "agents" / "luna-worker.toml").resolve(strict=False),
            Path("agents") / "luna-worker.toml",
        ),
        (
            (REPO_ROOT / "agents" / "solweaver-reviewer.toml").resolve(
                strict=False
            ),
            (codex_home / "agents" / "solweaver-reviewer.toml").resolve(
                strict=False
            ),
            Path("agents") / "solweaver-reviewer.toml",
        ),
    )
    legacy_skill = (codex_home / "skills" / SKILL_NAME).resolve(strict=False)
    backup_parent = (codex_home / "backups").resolve(strict=False)

    conflicts = unsafe_path_relationships(
        tuple(source for source, _, _ in sources),
        tuple(destination for _, destination, _ in sources) + (legacy_skill,),
        backup_parent,
    )
    if conflicts:
        print("Refusing unsafe overlapping install paths before mutation:")
        for relationship, first, second in conflicts:
            print(f"  - {relationship}: {first} <-> {second}")
        print(
            "Choose disjoint --codex-home and --user-skills-dir roots outside "
            "the Solweaver source tree and each other."
        )
        return 2

    existing: list[tuple[Path, Path]] = []
    reusable = set()
    for source, destination, backup_relative in sources:
        if not destination.exists():
            continue
        if (
            source.is_file()
            and destination.is_file()
            and source.read_bytes() == destination.read_bytes()
        ):
            reusable.add(destination)
        else:
            existing.append((destination, backup_relative))

    installed_skill = (user_skills_dir / SKILL_NAME).resolve(strict=False)
    if legacy_skill.exists() and legacy_skill != installed_skill:
        existing.append((legacy_skill, Path("legacy-codex-skills") / SKILL_NAME))

    if existing and not args.upgrade:
        print("Refusing to overwrite existing paths:")
        for destination, _ in existing:
            print(f"  - {destination}")
        print(
            "Move or remove them explicitly, or rerun with --upgrade to "
            "create backups and migrate a legacy skill installation."
        )
        return 1

    if existing:
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
        backup_root = (backup_parent / f"solweaver-{timestamp}").resolve(
            strict=False
        )
        for destination, backup_relative in existing:
            backup = (backup_root / backup_relative).resolve(strict=False)
            backup.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(destination), str(backup))
            print(f"Backed up {destination} to {backup}")

    for source, destination, _ in sources:
        if destination in reusable:
            print(f"Reusing identical agent definition {destination}")
            continue
        destination.parent.mkdir(parents=True, exist_ok=True)
        if source.is_dir():
            shutil.copytree(
                source,
                destination,
                ignore=shutil.ignore_patterns("__pycache__", "*.py[co]", ".DS_Store"),
            )
        else:
            shutil.copy2(source, destination)
        print(f"Installed {destination}")

    print()
    print("Next:")
    print("  1. Merge examples/config.toml into your Codex config.toml.")
    print("  2. Merge examples/AGENTS.md into your global AGENTS.md.")
    validator_command = shlex.join(
        [
            "python3",
            str(user_skills_dir / SKILL_NAME / "scripts" / "validate_install.py"),
            "--codex-home",
            str(codex_home),
            "--user-skills-dir",
            str(user_skills_dir),
        ]
    )
    print(f"  3. Validate with {validator_command}.")
    print("  4. Restart Codex or open a new task.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
