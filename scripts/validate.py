#!/usr/bin/env python3
"""Validate the public skill package using only the Python standard library."""

from __future__ import annotations

from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import tomllib


ROOT = Path(__file__).resolve().parents[1]
SKILL_NAME = "solweaver"
SKILL_DIR = ROOT / "skills" / SKILL_NAME


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def contains_phrase(text: str, phrase: str) -> bool:
    """Match human-authored contract prose without depending on line wrapping."""
    return " ".join(phrase.split()) in " ".join(text.split())


def validate_python(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    compile(text, str(path), "exec")
    return text


def tree_manifest(root: Path) -> dict[str, bytes]:
    """Return a deterministic content map while ignoring local cache artifacts."""
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in sorted(root.rglob("*"))
        if path.is_file()
        and "__pycache__" not in path.parts
        and path.suffix not in {".pyc", ".pyo"}
        and path.name != ".DS_Store"
    }


def validate_installer_behavior() -> None:
    """Exercise install, overlap refusal, upgrade, backup, and migration paths."""
    installer = ROOT / "scripts" / "install.py"
    with tempfile.TemporaryDirectory(prefix="solweaver-validate-") as temp:
        test_root = Path(temp)
        codex_home = test_root / "codex"
        user_skills_dir = test_root / "user-skills"
        command = [
            sys.executable,
            str(installer),
            "--codex-home",
            str(codex_home),
            "--user-skills-dir",
            str(user_skills_dir),
        ]

        initial = subprocess.run(command, capture_output=True, text=True)
        require(
            initial.returncode == 0,
            f"isolated installer failed: {initial.stdout}{initial.stderr}",
        )
        for argument, value in (
            ("--codex-home", codex_home.resolve()),
            ("--user-skills-dir", user_skills_dir.resolve()),
        ):
            require(
                f"{argument} {value}" in initial.stdout,
                f"installer next-step command omitted {argument}: {initial.stdout}",
            )

        installed_skill = user_skills_dir / SKILL_NAME
        installed_validator = installed_skill / "scripts" / "validate_install.py"
        installed_check = subprocess.run(
            [
                sys.executable,
                str(installed_validator),
                "--codex-home",
                str(codex_home),
                "--user-skills-dir",
                str(user_skills_dir),
            ],
            capture_output=True,
            text=True,
        )
        require(
            installed_check.returncode == 0,
            "fresh installed-copy validation failed: "
            f"{installed_check.stdout}{installed_check.stderr}",
        )
        require(
            tree_manifest(SKILL_DIR) == tree_manifest(installed_skill),
            "fresh installed skill differs from source",
        )
        for agent in (
            "terra-worker.toml",
            "luna-worker.toml",
            "solweaver-reviewer.toml",
        ):
            require(
                (ROOT / "agents" / agent).read_bytes()
                == (codex_home / "agents" / agent).read_bytes(),
                f"fresh installed agent differs from source: {agent}",
            )

        manifest_tool = installed_skill / "scripts" / "compute_delivery_manifest.py"
        manifest_command = [
            sys.executable,
            str(manifest_tool),
            "--root",
            f"skill={installed_skill}",
        ]
        for agent in (
            "terra-worker.toml",
            "luna-worker.toml",
            "solweaver-reviewer.toml",
        ):
            manifest_command.extend(
                [
                    "--file",
                    f"agents/{agent}={codex_home / 'agents' / agent}",
                ]
            )
        first_manifest = subprocess.run(
            manifest_command,
            capture_output=True,
            text=True,
        )
        second_manifest = subprocess.run(
            manifest_command,
            capture_output=True,
            text=True,
        )
        require(
            first_manifest.returncode == 0,
            f"delivery manifest failed: {first_manifest.stdout}{first_manifest.stderr}",
        )
        require(
            first_manifest.stdout == second_manifest.stdout,
            "delivery manifest is not deterministic",
        )
        require(
            "MANIFEST_VERSION solweaver-delivery-v1" in first_manifest.stdout
            and "DELIVERY_ARTIFACT_MANIFEST sha256:" in first_manifest.stdout,
            "delivery manifest omitted its version or aggregate identity",
        )

        refusal = subprocess.run(command, capture_output=True, text=True)
        require(refusal.returncode != 0, "installer overwrote an existing skill")
        require(
            "Refusing to overwrite existing paths" in refusal.stdout,
            "installer refusal did not explain the existing-path conflict",
        )

        legacy_skill = codex_home / "skills" / SKILL_NAME
        legacy_skill.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(installed_skill, legacy_skill)
        upgrade = subprocess.run(
            [*command, "--upgrade"],
            capture_output=True,
            text=True,
        )
        require(
            upgrade.returncode == 0,
            f"isolated upgrade failed: {upgrade.stdout}{upgrade.stderr}",
        )
        require(not legacy_skill.exists(), "legacy skill duplicate survived upgrade")

        backup_roots = sorted((codex_home / "backups").glob("solweaver-*"))
        require(len(backup_roots) == 1, "upgrade did not create exactly one backup")
        backup_root = backup_roots[0]
        for backup_skill in (
            backup_root / "user-skills" / SKILL_NAME,
            backup_root / "legacy-codex-skills" / SKILL_NAME,
        ):
            require(backup_skill.is_dir(), f"missing upgrade backup: {backup_skill}")
            require(
                tree_manifest(backup_skill) == tree_manifest(SKILL_DIR),
                f"upgrade backup content differs from source: {backup_skill}",
            )

        upgraded_check = subprocess.run(
            [
                sys.executable,
                str(installed_validator),
                "--codex-home",
                str(codex_home),
                "--user-skills-dir",
                str(user_skills_dir),
            ],
            capture_output=True,
            text=True,
        )
        require(
            upgraded_check.returncode == 0,
            "upgraded installed-copy validation failed: "
            f"{upgraded_check.stdout}{upgraded_check.stderr}",
        )
        require(
            tree_manifest(SKILL_DIR) == tree_manifest(installed_skill),
            "upgraded installed skill differs from source",
        )
        require(
            not any(path.name == "__pycache__" for path in installed_skill.rglob("*")),
            "installer copied a Python cache directory",
        )

        overlap_repo = test_root / "overlap-source"
        (overlap_repo / "scripts").mkdir(parents=True)
        shutil.copy2(installer, overlap_repo / "scripts" / "install.py")
        shutil.copytree(
            SKILL_DIR,
            overlap_repo / "skills" / SKILL_NAME,
            ignore=shutil.ignore_patterns("__pycache__", "*.py[co]", ".DS_Store"),
        )
        shutil.copytree(ROOT / "agents", overlap_repo / "agents")
        overlap_installer = overlap_repo / "scripts" / "install.py"
        overlap_source_before = tree_manifest(overlap_repo)
        symlink_skills_home = test_root / "overlap-codex-symlink-skills"
        symlink_skills_home.mkdir()
        (symlink_skills_home / "skills").symlink_to(
            overlap_repo / "skills", target_is_directory=True
        )
        symlink_agents_home = test_root / "overlap-codex-symlink-agents"
        symlink_agents_home.mkdir()
        (symlink_agents_home / "agents").symlink_to(
            overlap_repo / "agents", target_is_directory=True
        )
        symlink_backups_home = test_root / "overlap-codex-symlink-backups"
        symlink_backups_home.mkdir()
        (symlink_backups_home / "backups").symlink_to(
            overlap_repo / "skills" / SKILL_NAME,
            target_is_directory=True,
        )
        overlap_commands = (
            (
                "skill-source-equal",
                [
                    sys.executable,
                    str(overlap_installer),
                    "--codex-home",
                    str(test_root / "overlap-codex-equal"),
                    "--user-skills-dir",
                    str(overlap_repo / "skills"),
                    "--upgrade",
                ],
            ),
            (
                "skill-destination-nested-in-source",
                [
                    sys.executable,
                    str(overlap_installer),
                    "--codex-home",
                    str(test_root / "overlap-codex-nested"),
                    "--user-skills-dir",
                    str(
                        overlap_repo
                        / "skills"
                        / SKILL_NAME
                        / "nested-user-skills"
                    ),
                    "--upgrade",
                ],
            ),
            (
                "agent-and-legacy-source-equal",
                [
                    sys.executable,
                    str(overlap_installer),
                    "--codex-home",
                    str(overlap_repo),
                    "--user-skills-dir",
                    str(test_root / "overlap-user-skills"),
                    "--upgrade",
                ],
            ),
            (
                "symlinked-legacy-skill-into-source",
                [
                    sys.executable,
                    str(overlap_installer),
                    "--codex-home",
                    str(symlink_skills_home),
                    "--user-skills-dir",
                    str(test_root / "symlink-skills-user-skills"),
                    "--upgrade",
                ],
            ),
            (
                "symlinked-agent-destinations-into-source",
                [
                    sys.executable,
                    str(overlap_installer),
                    "--codex-home",
                    str(symlink_agents_home),
                    "--user-skills-dir",
                    str(test_root / "symlink-agents-user-skills"),
                    "--upgrade",
                ],
            ),
            (
                "symlinked-backup-parent-into-source",
                [
                    sys.executable,
                    str(overlap_installer),
                    "--codex-home",
                    str(symlink_backups_home),
                    "--user-skills-dir",
                    str(test_root / "symlink-backups-user-skills"),
                    "--upgrade",
                ],
            ),
        )
        for label, overlap_command in overlap_commands:
            overlap = subprocess.run(
                overlap_command,
                capture_output=True,
                text=True,
            )
            require(
                overlap.returncode == 2,
                f"installer accepted unsafe overlap {label}: "
                f"{overlap.stdout}{overlap.stderr}",
            )
            require(
                "Refusing unsafe overlapping install paths before mutation"
                in overlap.stdout,
                f"overlap refusal omitted its reason for {label}: {overlap.stdout}",
            )
            require(
                tree_manifest(overlap_repo) == overlap_source_before,
                f"overlap refusal mutated its source tree for {label}",
            )
        require(
            not (overlap_repo / "backups").exists(),
            "overlap refusal created a source-tree backup before rejection",
        )


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
    require("solweaver_reviewer" in text, "skill must define final-strict review")
    require("standard mode" in text, "skill must define standard assurance")
    require("final-strict mode" in text, "skill must define final-strict assurance")
    require(
        "Final-strict is the only independent-review assurance mode" in text,
        "skill must prohibit a separate strict assurance mode",
    )
    for term in (
        "Keep Solweaver project-neutral",
        "For small, low-risk, low-coupling tasks",
        "Do not spawn a worker or reviewer",
    ):
        require(
            contains_phrase(text, term),
            f"skill missing portability contract: {term}",
        )
    require("Use **strict mode**" not in text, "legacy strict mode must be removed")
    for stale in (
        "for each final-strict batch",
        "third reviewer for the same batch",
        "Final-strict batch ledger",
    ):
        require(stale not in text, f"SKILL.md retains reset-prone wording: {stale}")
    for mode in ("auto mode", "solo mode", "solo-reviewed mode", "team mode"):
        require(mode in text, f"skill must define {mode}")
    require(
        "do not spawn any agent" in text,
        "solo mode must prohibit subagent spawning",
    )
    require(
        "Never describe solo execution" in text,
        "solo mode must not claim strict review",
    )
    for term in (
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
        "`re-review closure matrix`",
        "design/acceptance reconciliation",
        "re-review rounds",
        "checkpoint-ready",
        "complete cumulative diff from the",
        "protected irreversible or production",
        "Never describe an intermediate final-strict checkpoint",
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
            contains_phrase(text, term),
            f"SKILL.md missing runtime contract text: {term}",
        )

    contracts = (SKILL_DIR / "references" / "contracts.md").read_text(encoding="utf-8")
    require("Worker task packet" in contracts, "missing worker task contract")
    require(
        "Final-strict review packet" in contracts,
        "missing final-strict review contract",
    )
    require("VERDICT: ship | fix-first | rethink" in contracts, "missing verdicts")
    require(
        contracts.count("REPORT LANGUAGE") == 2,
        "worker and reviewer packets must define report language",
    )
    require(
        contracts.count("EXECUTION MODE") == 2,
        "worker and reviewer packets must define execution mode",
    )
    require(
        contracts.count("ASSURANCE MODE") == 2,
        "worker and reviewer packets must define assurance mode",
    )
    require(
        "<standard | final-strict | strict>" not in contracts
        and "<final-strict | strict>" not in contracts,
        "contracts must not expose legacy strict assurance",
    )
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
            f"contracts missing runtime gate text: {term}",
        )
    require(
        contracts.count("TARGET_REVIEW_CALLS: 1") == 3,
        "ledger, review packet, and exhaustion report must target one call",
    )
    require(
        contains_phrase(
            contracts,
            "Use `REVIEW_BUDGET_MODE: default` with `MAX_REVIEW_CALLS: 2`",
        )
        and contains_phrase(contracts, "extended sets `MAX_REVIEW_CALLS: 3`"),
        "contracts must define immutable default and extended review budgets",
    )
    for stale in ("Final-strict batch ledger", "same unchanged batch"):
        require(
            stale not in contracts,
            f"contracts retain reset-prone wording: {stale}",
        )
    require(
        "newly-exposed-by-evidence" not in contracts,
        "contracts must reject the noncanonical finding-origin spelling",
    )
    require(
        "TERMINAL_STATUS: review-exhausted" not in contracts,
        "review exhaustion must not masquerade as terminal work status",
    )

    runtime_smoke = (SKILL_DIR / "references" / "runtime-smoke-test.md").read_text(
        encoding="utf-8"
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
        "lightweight small-task invariant",
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
            f"runtime smoke test missing: {term}",
        )

    validate_python(SKILL_DIR / "scripts" / "validate_install.py")
    validate_python(SKILL_DIR / "scripts" / "compute_delivery_manifest.py")

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
    if name == "solweaver_reviewer":
        require(
            "final-strict" in data.get("description", ""),
            f"{filename}: reviewer must be scoped to final-strict acceptance",
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
                contains_phrase(data.get("developer_instructions", ""), term),
                f"{filename}: reviewer missing readiness contract: {term}",
            )
        require(
            "newly-exposed-by-evidence"
            not in data.get("developer_instructions", ""),
            f"{filename}: reviewer contains a noncanonical finding origin",
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
    require("solo-reviewed" in policy, "AGENTS example must define solo-reviewed")
    require("final-strict" in policy, "AGENTS example must define final-strict")
    require("checkpoint-ready" in policy, "AGENTS example must bound checkpoints")
    require(
        "Support two assurance modes" in policy,
        "AGENTS example must expose only standard and final-strict assurance",
    )
    require(
        "REVIEW_BUDGET_MODE: default" in policy
        and "MAX_REVIEW_CALLS = 2" in policy
        and "REVIEW_BUDGET_MODE: extended" in policy
        and "MAX_REVIEW_CALLS = 3" in policy,
        "AGENTS example must define bounded default and extended review budgets",
    )
    require(
        "TARGET_REVIEW_CALLS = 1" in policy,
        "AGENTS example must target one review call",
    )
    require(
        "ASSURANCE_UNIT_ID" in policy and "REVIEW_READY: yes" in policy,
        "AGENTS example must define stable identity and readiness",
    )
    require(
        "REVIEW_ATTEMPT_ID" in policy
        and "FROZEN_CANDIDATE_ID" in policy
        and "ASSURANCE_PACKET_ID" in policy,
        "AGENTS example must define exclusive call identity",
    )
    require(
        "post-phase retrospective" in policy,
        "AGENTS example must require a terminal retrospective",
    )
    require(
        contains_phrase(
            policy,
            "A lock-busy contender creates no reservation and consumes no call",
        ),
        "AGENTS example must not charge a lock-busy contender",
    )
    require(
        contains_phrase(
            policy,
            "an ambiguous created reservation remains occupied and is recovered conservatively as consumed",
        ),
        "AGENTS example must conservatively retain an ambiguous created reservation",
    )
    require(
        "re-review closure matrix" in policy and "failed runtime gate" in policy,
        "AGENTS example must gate every re-review path",
    )
    for term in (
        "PARENT_ADVERSARIAL_READY: yes",
        "FINDING_ORIGIN",
        "never exceed or raise the maximum",
        "WORK_STATUS: complete",
        "ACCEPTANCE_STATUS: met",
        "KNOWN_BLOCKERS: none",
        "INDEPENDENT_ATTESTATION: not-obtained-within-budget",
        "DELIVERY_ARTIFACT_MANIFEST",
        "DELIVERY_ARTIFACT_MANIFEST_LOCATION",
        "configured TOML is not closure",
        "UNIT_STATUS: parent-recovery",
        "staged, unstaged, and untracked",
    ):
        require(
            contains_phrase(policy, term),
            f"AGENTS example missing convergence contract: {term}",
        )
    require("parent-completed" in policy, "AGENTS example must define parent recovery")
    require(
        contains_phrase(policy, "Do not request user direction merely"),
        "AGENTS example must keep review exhaustion parent-owned",
    )


def validate_package() -> None:
    installer = validate_python(ROOT / "scripts" / "install.py")
    for term in (
        '"--upgrade"',
        '"--user-skills-dir"',
        'Path.home() / ".agents" / "skills"',
        'codex_home / "backups"',
        'Path("legacy-codex-skills")',
        'shutil.ignore_patterns("__pycache__", "*.py[co]", ".DS_Store")',
        "Refusing to overwrite existing paths",
        "Refusing unsafe overlapping install paths before mutation",
        "unsafe_path_relationships",
        "shlex.join",
        "Reusing identical agent definition",
    ):
        require(term in installer, f"installer missing upgrade contract: {term}")
    validate_installer_behavior()

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    require("### Strict mode" not in readme, "README must not expose strict mode")
    for term in (
        "Runtime identity gates",
        "python3 scripts/install.py --upgrade",
        "`~/.agents/skills/solweaver`",
        "small ordinary task",
        "project-neutral",
        "scripts/validate_install.py",
        "never rolls them back automatically",
        "Final-strict mode",
        "complete cumulative diff",
        "protected boundary",
        "stable `ASSURANCE_UNIT_ID`",
        "`REVIEW_READY: yes`",
        "targets one reviewer call",
        "default hard budget is two",
        "optional `extended` budget",
        "at most three",
        "`PARENT_ADVERSARIAL_READY: yes`",
        "risk-surface map",
        "test-sensitivity evidence",
        "post-phase retrospective",
        "same re-review",
        "unusable or malformed verdict",
        "neutral re-review closure",
        "`FROZEN_CANDIDATE_ID`",
        "`ASSURANCE_PACKET_ID`",
        "`DELIVERY_ARTIFACT_MANIFEST`",
        "`DELIVERY_ARTIFACT_MANIFEST_LOCATION`",
        "`scripts/compute_delivery_manifest.py`",
        "staged, unstaged, and untracked paths",
        "plain `git diff` is not sufficient",
        "`REVIEW_ATTEMPT_ID`",
        "exclusive durable coordination",
        "lock-busy contender creates no reservation and consumes no call",
        "Markdown/text journal alone is not a lock",
        "Any `UNIT_STATUS` other than `open` blocks another reservation",
        "cancelled-before-start",
        "`blocked-external-boundary`",
        "Review exhausted",
        "never exceeds or raises that maximum",
        "REVIEW_STATUS: review-exhausted",
        "UNIT_STATUS: parent-recovery",
        "Review exhaustion closes only the independent review lane",
        "WORK_STATUS: complete",
        "ACCEPTANCE_STATUS: met",
        "KNOWN_BLOCKERS: none",
        "INDEPENDENT_ATTESTATION: not-obtained-within-budget",
        "FINAL_STATUS: parent-completed",
        "ASSURANCE_STATUS: final-strict-not-achieved",
        "without asking the user merely",
        "throwaway installer matrix",
        "must be disjoint from the Solweaver source tree",
        "both selected roots preserved",
    ):
        require(
            contains_phrase(readme, term),
            f"README missing runtime or upgrade guidance: {term}",
        )
    for stale in ("per batch", "same batch", "Final-strict batch"):
        require(stale not in readme, f"README retains reset-prone wording: {stale}")

    workflow = (ROOT / ".github" / "workflows" / "validate.yml").read_text(
        encoding="utf-8"
    )
    for term in ("validate_install.py", "--upgrade"):
        require(term in workflow, f"CI workflow missing: {term}")


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
    validate_package()
    print(
        "Validation passed: auto/solo/solo-reviewed/team execution, "
        "standard/final-strict assurance, runtime-gated Terra/Luna workers, "
        "phase-stable final-strict ledger with exclusive call reservation, "
        "separate candidate/packet identities, adversarial readiness and "
        "evidence-bar review, one-call target with bounded default/extended "
        "budgets, explicit completion/attestation status, safe upgrades, and "
        "concurrency 2."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
