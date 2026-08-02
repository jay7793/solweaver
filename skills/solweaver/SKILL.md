---
name: solweaver
description: >-
  Orchestrate bounded multi-agent software-development work with the main
  GPT-5.6 Sol agent owning planning, delegation, integration, verification, and
  delivery while terra_worker handles coupled or judgment-heavy implementation
  and luna_worker handles narrow, mechanical, or high-throughput assignments.
  Use for software-development prompts beginning with Goal: or /goal, or when
  the user asks to use a software team, team mode, agents, subagents, parallel
  work, or delegated feature implementation. Do not use for general questions,
  research, writing, operations-only requests, or small fixes where delegation
  adds no value.
---

# Solweaver

Coordinate the team without delegating orchestration itself. Keep the main
agent on the critical path and use subagents only when they materially improve
speed, isolation, or review quality.

## Confirm the execution contract

1. Classify the request before spawning agents.
2. Use team mode only for material software-development work covered by the
   trigger description.
3. Treat the active parent as the orchestrator. The intended global runtime is
   `gpt-5.6-sol` with reasoning effort `max`; this skill defines behavior and
   cannot change the active model. Never claim that runtime is active when the
   current task reports otherwise.
4. Require configured `terra_worker` and `luna_worker` agent definitions before
   claiming heterogeneous routing is available. If one worker is unavailable,
   use the other only when the assignment fits its routing criteria; otherwise
   keep the work on the parent and report the configuration gap.
5. Read repository instructions, confirm the working directory, and inspect
   existing changes before assigning write ownership.
6. Preserve user changes and repository boundaries.

## Plan and decompose

1. Form a short outcome-focused plan before delegation.
2. Identify the immediate blocker and keep it with the parent when local
   progress depends on it.
3. Split only independent work into bounded assignments.
4. Give each assignment a goal, explicit file or module ownership, acceptance
   criteria, commands to run, and expected evidence.
5. Avoid having multiple workers edit the same files. Prefer sequential work
   when assignments share state or depend on unresolved design decisions.

## Select agents

- Use `terra_worker` for the default implementation path and for ambiguous,
  coupled, multi-file, architecture-sensitive, backend, frontend, database,
  integration, debugging, and refactoring work.
- Use `luna_worker` when the assignment is narrow, low-coupling, mechanical, or
  high-throughput with explicit acceptance criteria. Good fits include isolated
  tests, fixtures, documentation-adjacent code, repetitive migrations, and
  independent file clusters.
- Prefer `terra_worker` when choosing incorrectly could affect auth,
  authorization, money, tenant isolation, data integrity, concurrency,
  production behavior, or a public contract. Add `security_reviewer` when the
  risk warrants it.
- Use `code_mapper` for a specific, read-only code-path or architecture
  question.
- Use `tester` for reproduction, regression coverage, focused verification, or
  failure diagnosis.
- Use `reviewer` for independent correctness and regression review.
- Use `security_reviewer` for auth, authorization, secrets, tenant isolation,
  money movement, webhooks, destructive operations, and production-risk paths.
- Use another implementation agent only when the user explicitly requests it.

Spawn only the agents that materially help. Parallelize disjoint assignments
within the available concurrency limit; do not create a large team by default.
Terra and Luna may run in parallel only when their file ownership is disjoint.

## Coordinate execution

1. Tell every writing agent it is not alone in the codebase, must preserve
   unrelated edits, and owns only its assigned scope.
2. Continue parent-owned inspection, integration planning, or blocker work
   while independent agents run.
3. Track dependencies and progress. Send follow-up instructions when evidence
   is missing or scope drifts.
4. Do not accept a worker summary as proof. Inspect the resulting diff and
   relevant files.
5. Resolve overlaps and conflicts centrally. Never ask workers to orchestrate
   the team.

## Integrate and verify

1. Review every worker change for scope, correctness, maintainability, and
   compatibility with concurrent edits.
2. Run focused checks first, then the broad repository checks appropriate to
   the risk and change size.
3. Use an independent reviewer for complex or high-risk changes.
4. Return failed work to the responsible worker with concrete evidence, or fix
   it on the parent critical path when that is more efficient.
5. Do not deploy, mutate production, merge, push, or open a pull request unless
   the user authorized that action.

## Deliver

Lead with the usable outcome. Report changed files, verification actually run,
remaining risks or unsupported behavior, and any action still requiring user
approval. Do not describe unverified repository checks as live production
evidence.
