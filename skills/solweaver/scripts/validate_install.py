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


def contains_phrase(text: str, phrase: str) -> bool:
    """Match human-authored contract prose without depending on line wrapping."""
    return " ".join(phrase.split()) in " ".join(text.split())


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
        for term in (
            "stable assurance unit",
            "REVIEW_ATTEMPT_ID",
            "FROZEN_CANDIDATE_ID",
            "ASSURANCE_PACKET_ID",
            "DELIVERY_ARTIFACT_MANIFEST",
            "DELIVERY_ARTIFACT_MANIFEST_LOCATION",
            "staged, unstaged, and untracked",
            "exclude only the declared ledger",
            "REVIEW_READY: yes",
            "UNIT_STATUS: open",
            "Markdown/text journal",
            "REVIEW_BUDGET_MODE: default",
            "MAX_REVIEW_CALLS: 3",
            "PARENT_ADVERSARIAL_READY: yes",
            "re-review closure matrix",
            "every prior",
            "complete readiness",
            "failed\nonly at runtime",
            "RUNTIME_AVAILABILITY_CLOSURE",
            "never infer missing parent evidence",
            "AUDIT_COMPLETENESS: scope-too-broad",
            "Continue the complete review after the first blocker",
            "FINDING_ORIGIN",
            "newly-exposed-evidence",
            "RESIDUAL RISK, not FINDINGS",
        ):
            require(
                contains_phrase(agent, term),
                f"{path}: reviewer missing readiness contract: {term}",
                errors,
            )
        require(
            "newly-exposed-by-evidence" not in agent,
            f"{path}: reviewer contains a noncanonical finding origin",
            errors,
        )
    require(
        "English" in agent, f"{path}: communication must default to English", errors
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--codex-home",
        type=Path,
        default=Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")),
        help="Codex home directory (default: CODEX_HOME or ~/.codex)",
    )
    parser.add_argument(
        "--user-skills-dir",
        type=Path,
        default=Path.home() / ".agents" / "skills",
        help="User-global skills directory (default: ~/.agents/skills)",
    )
    args = parser.parse_args()
    codex_home = args.codex_home.expanduser().resolve()
    user_skills_dir = args.user_skills_dir.expanduser().resolve()
    skill_dir = user_skills_dir / "solweaver"
    errors: list[str] = []
    warnings: list[str] = []

    legacy_skill_dir = codex_home / "skills" / "solweaver"
    require(
        not legacy_skill_dir.exists() or legacy_skill_dir == skill_dir,
        (
            f"legacy duplicate skill remains at {legacy_skill_dir}; migrate it "
            "with the Solweaver installer --upgrade"
        ),
        errors,
    )

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
        "allow any reasoning effort reported by the current `turn_context`",
        "Do not reject an observed Sol parent based on its reasoning effort",
        'effort == "max"',
        "model-generated",
        "self-report",
        "never roll",
        "back child edits automatically",
        "re-review rounds, child",
        "runtime checks and any mismatched",
        "`re-review closure matrix`",
        "design/acceptance reconciliation",
        "re-review rounds",
        "checkpoint-ready",
        "complete cumulative diff from the",
        "protected irreversible or production",
        "Never describe an intermediate final-strict checkpoint",
        "Use **team execution** for every Solweaver task",
        "Small, low-risk, or single-file work still requires one narrowly scoped worker",
        "Use **final-strict assurance** for every Solweaver task",
        "Final-strict is Solweaver's only assurance mode",
        "at least one bounded implementation worker for every task",
        "Keep Solweaver project-neutral",
        "`ASSURANCE_UNIT_ID`",
        "`REOPEN_GENERATION`",
        "`LEDGER_LOCATION`",
        "`ATTEMPT_COORDINATION_LOCATION`",
        "`REVIEW_ATTEMPT_ID`",
        "`CALL_STATE: reserved`",
        "`FROZEN_CANDIDATE_ID`",
        "`ASSURANCE_PACKET_ID`",
        "`DELIVERY_ARTIFACT_MANIFEST`",
        "`DELIVERY_ARTIFACT_MANIFEST_LOCATION`",
        "`scripts/compute_delivery_manifest.py`",
        "staged, unstaged, and untracked",
        "`git diff` alone is not a complete candidate identity",
        "`ACTIVE_REVIEW_RESERVATION`",
        "`cancelled-before-start`",
        "lock-busy contender creates no reservation and consumes no call",
        "exclusive atomic reservation",
        "Markdown journal alone is not a lock",
        "in-memory-only counter",
        "`TARGET_REVIEW_CALLS = 1`",
        "`MAX_REVIEW_CALLS = 2`",
        "hard maximum of 3",
        "Never exceed the recorded maximum",
        "review-budget mode",
        "`REVIEW_READY: yes`",
        "`UNIT_STATUS: open`",
        "Any status other than `open` forbids another reservation",
        "`PARENT_ADVERSARIAL_READY: yes`",
        "risk-surface map and counterexample matrix",
        "reviewability gate",
        "test-sensitivity evidence",
        "blocker must meet the referenced evidence bar",
        "later-call findings must classify their origin",
        "no `missing` or `not_run`",
        "post-phase retrospective",
        "Do not modify Solweaver or repository governance",
        "unusable or malformed verdict",
        "universal re-review preparation gate",
        "`RUNTIME_AVAILABILITY_CLOSURE`",
        "`UNIT_STATUS: parent-recovery`",
        "`REVIEW_STATUS: review-exhausted`",
        "Do not exceed the recorded maximum",
        "`WORK_STATUS: complete`",
        "`ACCEPTANCE_STATUS: met`",
        "`KNOWN_BLOCKERS: none`",
        "`INDEPENDENT_ATTESTATION: not-obtained-within-budget`",
        "`FINAL_STATUS: parent-completed`",
        "`ASSURANCE_STATUS: final-strict-not-achieved`",
        "Do not ask the user merely to",
    ):
        require(
            contains_phrase(skill, term),
            f"SKILL.md: missing contract text: {term}",
            errors,
        )
    for stale in (
        "The intended parent configuration is `gpt-5.6-sol` at `max`",
        "If the observed parent is not Sol Max",
        "select `gpt-5.6-sol` with `max` reasoning",
        "auto mode",
        "solo-reviewed",
        "solo mode",
        "standard assurance",
        "standard mode",
        "plain solo",
    ):
        require(
            stale.lower() not in skill.lower(),
            f"SKILL.md: retains legacy or parent max-only gate: {stale}",
            errors,
        )
    require(
        "Use **strict mode**" not in skill,
        "SKILL.md: legacy strict mode must be removed",
        errors,
    )
    for stale in (
        "for each final-strict batch",
        "third reviewer for the same batch",
        "Final-strict batch ledger",
    ):
        require(
            stale not in skill,
            f"SKILL.md: retains reset-prone wording: {stale}",
            errors,
        )

    ui = read_text(skill_dir / "agents" / "openai.yaml", errors)
    require(
        'display_name: "Solweaver"' in ui, "openai.yaml: wrong display name", errors
    )
    require(
        "$solweaver" in ui, "openai.yaml: default prompt must invoke $solweaver", errors
    )
    for term in (
        'short_description: "Sol leads a team with final-strict review"',
        "mandatory team execution and final-strict assurance",
    ):
        require(
            term in ui,
            f"openai.yaml: missing team/final-strict metadata: {term}",
            errors,
        )
    for stale in ("auto mode", "solo-reviewed", "solo mode", "standard assurance"):
        require(
            stale not in ui.lower(),
            f"openai.yaml: retains legacy wording: {stale}",
            errors,
        )

    manifest_path = skill_dir / "scripts" / "compute_delivery_manifest.py"
    manifest_script = read_text(manifest_path, errors)
    try:
        compile(manifest_script, str(manifest_path), "exec")
    except SyntaxError as exc:
        errors.append(f"{manifest_path}: syntax error: {exc}")
    for term in (
        'MANIFEST_VERSION = "solweaver-delivery-v1"',
        '"DELIVERY_ARTIFACT_MANIFEST sha256:',
        "sorted(records)",
    ):
        require(
            term in manifest_script,
            f"{manifest_path}: missing reproducibility contract: {term}",
            errors,
        )

    contracts = read_text(skill_dir / "references" / "contracts.md", errors)
    for term in (
        "Runtime identity gates",
        "`terra_worker` | `gpt-5.6-terra` | `max`",
        "`luna_worker` | `gpt-5.6-luna` | `max`",
        "`solweaver_reviewer` | `gpt-5.6-sol` | `max`",
        "do not infer sandbox",
        "Do not revert or delete child edits",
        "Re-review closure matrix",
        "RE-REVIEW PREPARATION",
        "fix-first, rethink, unusable, malformed, or runtime-failed",
        "The matrix is required even when no source file changed",
        "Review-budget exhaustion and parent completion",
        "Final-strict assurance-unit ledger",
        "checkpoint-ready",
        "Complete cumulative diff from base",
        "ASSURANCE_UNIT_ID: <stable repository/track/phase-or-delivery-id>",
        "REOPEN_GENERATION: <0 for first run, then explicitly authorized integer>",
        "LEDGER_LOCATION: <durable authoritative path or artifact>",
        "UNIT_STATUS: open | ship | parent-recovery | parent-completed | blocked | blocked-external-boundary",
        "TARGET_REVIEW_CALLS: 1",
        "REVIEW_BUDGET_MODE: <default | extended>",
        "MAX_REVIEW_CALLS: <2 for default | 3 for extended>",
        "REVIEWABILITY GATE",
        "PARENT ADVERSARIAL READINESS",
        "PARENT_ADVERSARIAL_READY: <yes or no>",
        "Reviewer blocker evidence bar",
        "AUDIT_COMPLETENESS: complete | scope-too-broad",
        "FINDING_ORIGIN",
        "newly-exposed-evidence",
        "REVIEW_READY: <yes or no>",
        "Post-phase retrospective",
        "WORKFLOW_CHANGE_STATUS: proposed-for-user-approval",
        "Exclusive reviewer-call reservation and identity",
        "ATTEMPT_COORDINATION_LOCATION",
        "ACTIVE_REVIEW_RESERVATION",
        "REVIEW_ATTEMPT_ID",
        "CALL_STATE: reserved",
        "FROZEN_CANDIDATE_ID",
        "ASSURANCE_PACKET_ID",
        "DELIVERY_ARTIFACT_MANIFEST",
        "DELIVERY_ARTIFACT_MANIFEST_LOCATION",
        "scripts/compute_delivery_manifest.py",
        "staged, unstaged, and untracked",
        "plain `git diff` omits untracked files",
        "cancelled-before-start",
        "lock-busy contender creates no reservation and consumes no call",
        "in-memory-only steps",
        "Markdown or text journal alone is not a lock",
        "UNIT_STATUS: open",
        "Any `UNIT_STATUS` other than `open` forbids another reservation",
        "blocked-external-boundary",
        "Final-strict protected boundaries",
        "NEXT_REVIEW_ALLOWED: no",
        "REVIEW_LANE_STATUS: closed",
        "RUNTIME_AVAILABILITY_CLOSURE",
        "UNIT_STATUS: parent-recovery",
        "same unchanged assurance unit",
        "USER_DECISION_REQUIRED: no",
        "WORK_STATUS: complete | blocked",
        "ACCEPTANCE_STATUS: met | not-met",
        "KNOWN_BLOCKERS: none | <exact unresolved blocker>",
        "INDEPENDENT_ATTESTATION: not-obtained-within-budget",
        "FINAL_STATUS: parent-completed | blocked | blocked-external-boundary",
        "ASSURANCE_STATUS: final-strict-not-achieved",
        "<1, 2, or 3>",
    ):
        require(
            contains_phrase(contracts, term),
            f"contracts: missing {term}",
            errors,
        )
    require(
        contracts.count("TARGET_REVIEW_CALLS: 1") == 3,
        "contracts: ledger, review packet, and exhaustion report must target one call",
        errors,
    )
    require(
        contains_phrase(
            contracts,
            "Use `REVIEW_BUDGET_MODE: default` with `MAX_REVIEW_CALLS: 2`",
        )
        and contains_phrase(contracts, "extended sets `MAX_REVIEW_CALLS: 3`"),
        "contracts: must define immutable default and extended review budgets",
        errors,
    )
    for stale in ("Final-strict batch ledger", "same unchanged batch"):
        require(
            stale not in contracts,
            f"contracts: retain reset-prone wording: {stale}",
            errors,
        )
    require(
        "newly-exposed-by-evidence" not in contracts,
        "contracts: noncanonical finding-origin spelling is forbidden",
        errors,
    )
    require(
        "TERMINAL_STATUS: review-exhausted" not in contracts,
        "contracts: review exhaustion must not masquerade as terminal work status",
        errors,
    )
    require(
        contracts.count("EXECUTION MODE\nteam") == 2,
        "contracts: worker and reviewer packets must fix execution to team",
        errors,
    )
    require(
        contracts.count("ASSURANCE MODE\nfinal-strict") == 2,
        "contracts: worker and reviewer packets must fix assurance to final-strict",
        errors,
    )
    for stale in (
        "<auto",
        "solo-reviewed",
        "solo mode",
        "<standard",
        "standard assurance",
    ):
        require(
            stale not in contracts.lower(),
            f"contracts: retain legacy workflow wording: {stale}",
            errors,
        )
    require(
        "<final-strict | strict>" not in contracts,
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
        "Do not require `max` for the parent",
        'effort == "max"',
        "model-generated self-report",
        "focused routing smoke is not full implementation end-to-end proof",
        "team execution",
        "at least one bounded implementation worker",
        "mandatory final-strict assurance",
        "no-lightweight-bypass invariant",
        "checkpoint-ready",
        "`ASSURANCE_UNIT_ID`",
        "`REOPEN_GENERATION`",
        "`LEDGER_LOCATION`",
        "`TARGET_REVIEW_CALLS: 1`",
        "`REVIEW_READY: no`",
        "cross-task continuity",
        "post-phase retrospective",
        "universal re-review preparation",
        "unusable or malformed verdict",
        "`re-review closure matrix`",
        "`ATTEMPT_COORDINATION_LOCATION`",
        "`FROZEN_CANDIDATE_ID`",
        "`ASSURANCE_PACKET_ID`",
        "`DELIVERY_ARTIFACT_MANIFEST`",
        "`REVIEW_ATTEMPT_ID`",
        "`CALL_STATE: reserved`",
        "exactly one atomically create",
        "text assertion of exclusivity is insufficient",
        "cancelled-before-start",
        "`blocked-external-boundary`",
        "complete cumulative",
        "diff from the recorded base",
        "protected irreversible",
        "default two-call hard gate",
        "`REVIEW_BUDGET_MODE: extended`",
        "`MAX_REVIEW_CALLS: 3`",
        "`PARENT_ADVERSARIAL_READY: yes`",
        "AUDIT_COMPLETENESS",
        "FINDING_ORIGIN",
        "`UNIT_STATUS` is not `open`",
        "`RUNTIME_AVAILABILITY_CLOSURE`",
        "`DELIVERY_ARTIFACT_MANIFEST_LOCATION`",
        "`UNIT_STATUS: parent-recovery`",
        "plain `git diff` alone must fail readiness",
        "never exceeds or raises the predeclared",
        "REVIEW_STATUS: review-exhausted",
        "WORK_STATUS: complete",
        "ACCEPTANCE_STATUS: met",
        "KNOWN_BLOCKERS: none",
        "INDEPENDENT_ATTESTATION: not-obtained-within-budget",
        "FINAL_STATUS: parent-completed",
        "ASSURANCE_STATUS: final-strict-not-achieved",
        "without requesting user direction",
    ):
        require(
            contains_phrase(runtime_smoke, term),
            f"runtime smoke test: missing {term}",
            errors,
        )
    require(
        not contains_phrase(
            runtime_smoke,
            'parent `turn_context` reports model == "gpt-5.6-sol" and effort == "max"',
        ),
        "runtime smoke test: retains parent max-only gate",
        errors,
    )
    for stale in (
        "auto mode",
        "solo-reviewed",
        "solo mode",
        "standard assurance",
        "standard mode",
        "lightweight small-task invariant",
    ):
        require(
            stale not in runtime_smoke.lower(),
            f"runtime smoke test: retains legacy workflow wording: {stale}",
            errors,
        )

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
        if not exact_line(config, "max_concurrent_threads_per_session = 2"):
            warnings.append(
                "global config does not use the example spawned-thread cap of 2"
            )
    else:
        warnings.append(
            "global config.toml was not checked; select gpt-5.6-sol before use"
        )

    policy_path = codex_home / "AGENTS.md"
    if policy_path.exists():
        policy = read_text(policy_path, errors)
        for term in ("$solweaver", "terra_worker", "luna_worker"):
            require(term in policy, f"global AGENTS.md: missing {term}", errors)
    else:
        warnings.append(
            "global AGENTS.md was not checked; merge examples/AGENTS.md manually"
        )

    if errors:
        print("Solweaver validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"Solweaver static validation passed: {skill_dir}")
    for warning in warnings:
        print(f"WARNING: {warning}")
    print("Runtime behavior still requires a restarted/new-task smoke test.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
