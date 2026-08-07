#!/usr/bin/env python3
"""Install Solweaver without overwriting existing Codex files."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import os
from pathlib import Path
import shutil


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_NAME = "solweaver"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Install Solweaver, its Terra/Luna workers, and final-strict reviewer."
    )
    parser.add_argument(
        "--codex-home",
        type=Path,
        default=Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")),
        help="Codex configuration directory (default: CODEX_HOME or ~/.codex).",
    )
    parser.add_argument(
        "--upgrade",
        action="store_true",
        help="Back up and replace an existing Solweaver installation.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    codex_home = args.codex_home.expanduser().resolve()

    sources = {
        REPO_ROOT / "skills" / SKILL_NAME: codex_home / "skills" / SKILL_NAME,
        REPO_ROOT / "agents" / "terra-worker.toml": (
            codex_home / "agents" / "terra-worker.toml"
        ),
        REPO_ROOT / "agents" / "luna-worker.toml": (
            codex_home / "agents" / "luna-worker.toml"
        ),
        REPO_ROOT / "agents" / "solweaver-reviewer.toml": (
            codex_home / "agents" / "solweaver-reviewer.toml"
        ),
    }

    existing = []
    reusable = set()
    for source, destination in sources.items():
        if not destination.exists():
            continue
        if (
            source.is_file()
            and destination.is_file()
            and source.read_bytes() == destination.read_bytes()
        ):
            reusable.add(destination)
        else:
            existing.append(destination)

    if existing and not args.upgrade:
        print("Refusing to overwrite existing paths:")
        for path in existing:
            print(f"  - {path}")
        print("Move or remove them explicitly, or rerun with --upgrade to create backups.")
        return 1

    if existing:
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
        backup_root = codex_home / "backups" / f"solweaver-{timestamp}"
        for destination in existing:
            backup = backup_root / destination.relative_to(codex_home)
            backup.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(destination), str(backup))
            print(f"Backed up {destination} to {backup}")

    for source, destination in sources.items():
        if destination in reusable:
            print(f"Reusing identical agent definition {destination}")
            continue
        destination.parent.mkdir(parents=True, exist_ok=True)
        if source.is_dir():
            shutil.copytree(source, destination)
        else:
            shutil.copy2(source, destination)
        print(f"Installed {destination}")

    print()
    print("Next:")
    print("  1. Merge examples/config.toml into your Codex config.toml.")
    print("  2. Merge examples/AGENTS.md into your global AGENTS.md.")
    print("  3. Restart Codex or open a new task.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
