#!/usr/bin/env python3
"""Install the skill and agent definitions without overwriting existing files."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import shutil


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_NAME = "solweaver"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Install Solweaver, its Terra/Luna workers, and strict reviewer."
    )
    parser.add_argument(
        "--codex-home",
        type=Path,
        default=Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")),
        help="Codex configuration directory (default: CODEX_HOME or ~/.codex).",
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

    existing = [destination for destination in sources.values() if destination.exists()]
    if existing:
        print("Refusing to overwrite existing paths:")
        for path in existing:
            print(f"  - {path}")
        print("Move or remove those paths explicitly, then run the installer again.")
        return 1

    for source, destination in sources.items():
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
