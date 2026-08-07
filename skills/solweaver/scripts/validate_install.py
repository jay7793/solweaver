#!/usr/bin/env python3
"""Validate an installed Solweaver skill, agents, configuration, and routing."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import re
import sys
from typing import Optional


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def read_text(path: Path, errors: list[str]) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        errors.append(f"cannot read {path}: {exc}")
        return ""


def exact_line(text: str, line: str) -> bool:
    return re.search(rf"^{re.escape(line)}$", text, re.MULTILINE) is not None


def validate_agent(
    path: Path,
    expected_name: str,
    expected_model: str,
    errors: list[str],
    *,
    sandbox_mode: Optional[str] = None,
) -> None:
    agent = read_text(path, errors)
    for line in (
        f'name = "{expected_name}"',
        f'model = "{expected_model}"',
        'model_reasoning_effort = "max"',
    ):
        require(exact_line(agent, line), f"{path}: missing {line}", errors)
    if sandbox_mode is not None:
        require(
            exact_line(agent, f'sandbox_mode = "{sandbox_mode}"'),
            f"{path}: sandbox_mode must be {sandbox_mode}",
            errors,
        )
    if expected_name == "solweaver_reviewer":
        require(
            "final-strict" in agent,
            f"{path}: reviewer must be scoped to final-strict acceptance",
            errors,
        )
    require("English" in agent, f"{path}: communication must default to English", errors)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--codex-home",
        type=Path,
        default=Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")),
        help="Codex home directory (default: CODEX_HOME or ~/.codex)",
    )
    args = parser.parse_args()
    codex_home = args.codex_home.expanduser().resolve()
    skill_dir = codex_home / "skills" / "solweaver"
    errors: list[str] = []
    warnings: list[str] = []

    skill = read_text(skill_dir / "SKILL.md", errors)
    frontmatter = re.match(r"\A---\n(.*?)\n---\n", skill, re.DOTALL)
    require(frontmatter is not None, "SKILL.md: missing YAML frontmatter", errors)
    if frontmatter:
        keys = re.findall(
            r"^([A-Za-z0-9_-]+):",
            frontmatter.group(1),
            re.MULTILINE,
        )
        require(
            keys == ["name", "description"],
            "SKILL.md: frontmatter must contain only name and description",
            errors,
        )

    for term in (
        "terra_worker",
        "luna_worker",
        "solweaver_reviewer",
        'fork_turns="none"',
        "runtime-smoke-test.md",
        "`turn_context`",
        'model == "gpt-5.6-terra"',
        'model == "gpt-5.6-luna"',
        'model == "gpt-5.6-sol"',
        'effort == "max"',
        "model-generated",
        "self-report",
        "never roll",
        "back child edits automatically",
        "re-review rounds, child",
        "runtime checks and any mismatched",
        "`fix-first` closure matrix",
        "design/acceptance reconciliation",
        "re-review rounds",
        "checkpoint-ready",
        "complete cumulative diff from the",
        "protected irreversible or production",
        "Never describe an intermediate final-strict checkpoint",
        "Final-strict is the only independent-review assurance mode",
        "`MAX_REVIEW_CALLS = 2`",
        "third reviewer for the same batch",
        "`REVIEW_STATUS: review-exhausted`",
        "Do not spawn call 3",
        "`FINAL_STATUS: parent-completed`",
        "`ASSURANCE_STATUS: final-strict-not-achieved`",
        "Do not ask the user merely to",
    ):
        require(term in skill, f"SKILL.md: missing contract text: {term}", errors)
    require(
        "Use **strict mode**" not in skill,
        "SKILL.md: legacy strict mode must be removed",
        errors,
    )

    ui = read_text(skill_dir / "agents" / "openai.yaml", errors)
    require('display_name: "Solweaver"' in ui, "openai.yaml: wrong display name", errors)
    require("$solweaver" in ui, "openai.yaml: default prompt must invoke $solweaver", errors)

    contracts = read_text(skill_dir / "references" / "contracts.md", errors)
    for term in (
        "Runtime identity gates",
        "`terra_worker` | `gpt-5.6-terra` | `max`",
        "`luna_worker` | `gpt-5.6-luna` | `max`",
        "`solweaver_reviewer` | `gpt-5.6-sol` | `max`",
        "do not infer sandbox",
        "Do not revert or delete child edits",
        "`fix-first` closure matrix",
        "Review-budget exhaustion and parent completion",
        "Final-strict batch ledger",
        "checkpoint-ready",
        "Complete cumulative diff from base",
        "Final-strict protected boundaries",
        "NEXT_REVIEW_ALLOWED: no",
        "same unchanged batch",
        "USER_DECISION_REQUIRED: no",
        "FINAL_STATUS: parent-completed | blocked-external-boundary",
        "ASSURANCE_STATUS: final-strict-not-achieved",
    ):
        require(term in contracts, f"contracts: missing {term}", errors)
    require(
        contracts.count("MAX_REVIEW_CALLS: 2") == 3,
        "contracts: ledger, review packet, and exhaustion report must pin two calls",
        errors,
    )
    require(
        "<standard | final-strict | strict>" not in contracts
        and "<final-strict | strict>" not in contracts,
        "contracts: legacy strict assurance must be removed",
        errors,
    )

    runtime_smoke = read_text(
        skill_dir / "references" / "runtime-smoke-test.md",
        errors,
    )
    for term in (
        "`turn_context`",
        'model == "gpt-5.6-terra"',
        'model == "gpt-5.6-luna"',
        'model == "gpt-5.6-sol"',
        'effort == "max"',
        "model-generated self-report",
        "focused routing smoke is not full implementation end-to-end proof",
        "final-strict mode",
        "checkpoint-ready",
        "complete cumulative",
        "diff from the recorded base",
        "protected irreversible",
        "two-call hard gate",
        "never spawns call 3",
        "REVIEW_STATUS: review-exhausted",
        "FINAL_STATUS: parent-completed",
        "ASSURANCE_STATUS: final-strict-not-achieved",
        "without requesting user direction",
    ):
        require(term in runtime_smoke, f"runtime smoke test: missing {term}", errors)

    validate_agent(
        codex_home / "agents" / "terra-worker.toml",
        "terra_worker",
        "gpt-5.6-terra",
        errors,
    )
    validate_agent(
        codex_home / "agents" / "luna-worker.toml",
        "luna_worker",
        "gpt-5.6-luna",
        errors,
    )
    validate_agent(
        codex_home / "agents" / "solweaver-reviewer.toml",
        "solweaver_reviewer",
        "gpt-5.6-sol",
        errors,
        sandbox_mode="read-only",
    )

    config_path = codex_home / "config.toml"
    if config_path.exists():
        config = read_text(config_path, errors)
        if not exact_line(config, 'model = "gpt-5.6-sol"'):
            warnings.append("global config does not pin parent model to gpt-5.6-sol")
        if not exact_line(config, 'model_reasoning_effort = "max"'):
            warnings.append("global config does not pin parent reasoning effort to max")
        if not exact_line(config, "max_concurrent_threads_per_session = 2"):
            warnings.append("global config does not use the example spawned-thread cap of 2")
    else:
        warnings.append("global config.toml was not checked; select Sol Max before use")

    policy_path = codex_home / "AGENTS.md"
    if policy_path.exists():
        policy = read_text(policy_path, errors)
        for term in ("$solweaver", "terra_worker", "luna_worker"):
            require(term in policy, f"global AGENTS.md: missing {term}", errors)
    else:
        warnings.append("global AGENTS.md was not checked; merge examples/AGENTS.md manually")

    if errors:
        print("Solweaver validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"Solweaver static validation passed: {codex_home}")
    for warning in warnings:
        print(f"WARNING: {warning}")
    print("Runtime behavior still requires a restarted/new-task smoke test.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
