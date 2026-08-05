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
    require("solweaver_reviewer" in text, "skill must define strict review")
    require("standard mode" in text, "skill must define standard assurance")
    require("strict mode" in text, "skill must define strict assurance")

    contracts = (SKILL_DIR / "references" / "contracts.md").read_text(
        encoding="utf-8"
    )
    require("Worker task packet" in contracts, "missing worker task contract")
    require("Strict review packet" in contracts, "missing strict review contract")
    require("VERDICT: ship | fix-first | rethink" in contracts, "missing verdicts")
    require(
        contracts.count("REPORT LANGUAGE") == 2,
        "worker and reviewer packets must define report language",
    )

    ui = (SKILL_DIR / "agents" / "openai.yaml").read_text(encoding="utf-8")
    require(
        f"${SKILL_NAME}" in ui,
        "openai.yaml default prompt must invoke the skill",
    )


def validate_agent(
    filename: str,
    name: str,
    model: str,
    *,
    effort: str = "max",
    sandbox_mode: str | None = None,
) -> None:
    path = ROOT / "agents" / filename
    with path.open("rb") as handle:
        data = tomllib.load(handle)

    require(data.get("name") == name, f"{filename}: incorrect agent name")
    require(data.get("model") == model, f"{filename}: incorrect model")
    require(
        data.get("model_reasoning_effort") == effort,
        f"{filename}: reasoning effort must be {effort}",
    )
    require(
        bool(data.get("developer_instructions")),
        f"{filename}: missing developer instructions",
    )
    require(
        "English" in data.get("developer_instructions", ""),
        f"{filename}: communication must default to English",
    )
    if sandbox_mode is not None:
        require(
            data.get("sandbox_mode") == sandbox_mode,
            f"{filename}: sandbox_mode must be {sandbox_mode}",
        )


def validate_examples() -> None:
    with (ROOT / "examples" / "config.toml").open("rb") as handle:
        config = tomllib.load(handle)
    require(config.get("model") == "gpt-5.6-sol", "parent model must be Sol")
    require(
        config.get("model_reasoning_effort") == "max",
        "parent reasoning effort must be max",
    )
    agents = config.get("agents", {})
    require(agents.get("enabled") is True, "agents must be enabled")
    require(
        agents.get("max_concurrent_threads_per_session") == 2,
        "concurrent spawned-agent limit must be 2",
    )
    require("max_threads" not in agents, "use the current concurrency key")

    policy = (ROOT / "examples" / "AGENTS.md").read_text(encoding="utf-8")
    require(f"${SKILL_NAME}" in policy, "AGENTS example must load the skill")
    require("terra_worker" in policy, "AGENTS example must mention Terra")
    require("luna_worker" in policy, "AGENTS example must mention Luna")
    require(
        "solweaver_reviewer" in policy,
        "AGENTS example must mention strict reviewer",
    )


def main() -> int:
    validate_skill()
    validate_agent("terra-worker.toml", "terra_worker", "gpt-5.6-terra")
    validate_agent("luna-worker.toml", "luna_worker", "gpt-5.6-luna")
    validate_agent(
        "solweaver-reviewer.toml",
        "solweaver_reviewer",
        "gpt-5.6-sol",
        sandbox_mode="read-only",
    )
    validate_examples()
    print(
        "Validation passed: Sol orchestrator, Terra/Luna workers, "
        "strict Sol reviewer, and concurrency 2."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
