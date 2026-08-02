#!/usr/bin/env python3
"""Validate the public skill package using only the Python standard library."""

from __future__ import annotations

from pathlib import Path
import re
import tomllib


ROOT = Path(__file__).resolve().parents[1]
SKILL_NAME = "solweaver"
SKILL_DIR = ROOT / "skills" / SKILL_NAME


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def validate_skill() -> None:
    path = SKILL_DIR / "SKILL.md"
    text = path.read_text(encoding="utf-8")
    require(text.startswith("---\n"), "SKILL.md must start with YAML frontmatter")

    parts = text.split("---", 2)
    require(len(parts) == 3, "SKILL.md frontmatter must have a closing delimiter")
    frontmatter = parts[1]
    body = parts[2].strip()

    top_level_keys = []
    for line in frontmatter.splitlines():
        if line and not line[0].isspace():
            match = re.match(r"([a-zA-Z0-9_-]+):", line)
            if match:
                top_level_keys.append(match.group(1))

    require(
        set(top_level_keys) == {"name", "description"},
        "frontmatter must contain only name and description",
    )
    require(
        re.search(rf"^name:\s*{re.escape(SKILL_NAME)}\s*$", frontmatter, re.MULTILINE)
        is not None,
        "skill name must match its folder",
    )
    require("description: >-" in frontmatter, "description must use folded YAML")
    require(bool(body), "SKILL.md body must not be empty")
    require("terra_worker" in text, "skill must route Terra work")
    require("luna_worker" in text, "skill must route Luna work")

    ui = (SKILL_DIR / "agents" / "openai.yaml").read_text(encoding="utf-8")
    require(
        f"${SKILL_NAME}" in ui,
        "openai.yaml default prompt must invoke the skill",
    )


def validate_worker(filename: str, name: str, model: str) -> None:
    path = ROOT / "agents" / filename
    with path.open("rb") as handle:
        data = tomllib.load(handle)

    require(data.get("name") == name, f"{filename}: incorrect agent name")
    require(data.get("model") == model, f"{filename}: incorrect model")
    require(
        data.get("model_reasoning_effort") == "max",
        f"{filename}: reasoning effort must be max",
    )
    require(
        bool(data.get("developer_instructions")),
        f"{filename}: missing developer instructions",
    )


def validate_examples() -> None:
    with (ROOT / "examples" / "config.toml").open("rb") as handle:
        config = tomllib.load(handle)
    require(config.get("model") == "gpt-5.6-sol", "parent model must be Sol")
    require(
        config.get("model_reasoning_effort") == "max",
        "parent reasoning effort must be max",
    )
    require(config.get("agents", {}).get("max_depth") == 1, "max_depth must be 1")

    policy = (ROOT / "examples" / "AGENTS.md").read_text(encoding="utf-8")
    require(f"${SKILL_NAME}" in policy, "AGENTS example must load the skill")
    require("terra_worker" in policy, "AGENTS example must mention Terra")
    require("luna_worker" in policy, "AGENTS example must mention Luna")


def main() -> int:
    validate_skill()
    validate_worker("terra-worker.toml", "terra_worker", "gpt-5.6-terra")
    validate_worker("luna-worker.toml", "luna_worker", "gpt-5.6-luna")
    validate_examples()
    print("Validation passed: Sol orchestrator, Terra max, Luna max.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
