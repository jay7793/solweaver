---
name: solweaver
description: >-
  Run Sol-led software development in auto, solo, solo-reviewed, or team modes,
  with GPT-5.6 Sol owning planning, implementation or delegation, integration,
  verification, and delivery; terra_worker and luna_worker providing bounded
  implementation; and solweaver_reviewer providing fresh strict review. Use
  for software-development prompts beginning with Goal: or /goal, or when the
  user requests Sol-only work, a software team, agents, subagents, parallel
  work, or delegated implementation. Do not use for general questions,
  research, writing, or operations-only requests.
---

# Solweaver

Coordinate execution without delegating orchestration itself. Keep the main
agent on the critical path. Work solo or use the smallest team that materially
improves speed, context isolation, or review quality.

## Preflight

1. Classify the request before spawning agents.
2. Read applicable `AGENTS.md` files and repository guidance. Confirm the
   working directory, branch or worktree, and existing changes before assigning
   ownership.
3. Keep the active parent as orchestrator. The intended parent configuration is
   `gpt-5.6-sol` at `max`, but this skill cannot select or prove the runtime.
4. When the selected mode permits agents, inspect available agent types before
   routing. Do not silently substitute a missing worker or reviewer.
5. Describe model evidence precisely:
   - **Observed**: public runtime or spawn metadata reports role, model, or
     effort.
   - **Configured**: a validated agent definition pins the value, but runtime
     metadata does not expose it.
   - **Unverified**: neither source establishes the value.
6. If observed routing contradicts configuration, stop accepting that lane and
   report the mismatch. Never use a task label or worker self-report as runtime
   proof.
7. Preserve user changes, repository boundaries, and explicit external-action
   approval requirements.

## Choose execution mode

- Use **auto mode** when the user does not name a mode. Sol chooses local solo
  execution or the smallest useful team; invoking Solweaver alone does not
  require a subagent.
- Use **solo mode** when the user wants Sol alone. Sol plans, implements,
  verifies, and delivers without spawning any worker or reviewer. Solo supports
  standard assurance only.
- Use **solo-reviewed mode** when the user wants Sol to implement alone with an
  independent final gate. Do not spawn implementation workers; after parent
  verification, spawn one fresh `solweaver_reviewer` at a time and apply strict
  acceptance, including a fresh review after any fix round.
- Use **team mode** when the user explicitly requests delegation. Spawn at
  least one bounded implementation worker, while Sol retains integration and
  verification. Add the fresh reviewer when strict assurance applies.
- Honor an explicit mode without silently changing it. If solo mode conflicts
  with a user-requested or risk-triggered strict review, stop before
  implementation and ask the user to choose solo without strict acceptance or
  solo-reviewed.

## Choose assurance

- Use **standard mode** for ordinary work in auto, solo, or team execution. Sol
  inspects the diff, reruns verification, and accepts or returns the work.
- Use **strict mode** when the user requests it or the change affects auth,
  authorization, secrets, tenant isolation, money, data integrity, migrations,
  destructive behavior, concurrency, public APIs, production-critical paths,
  or a wide architectural refactor.
- Apply strict mode to auto or team execution, and always apply it to
  solo-reviewed execution. Require a fresh `solweaver_reviewer` verdict after
  parent verification. If the reviewer is unavailable, do not claim strict
  completion.
- Never describe solo execution or a parent self-review as independent strict
  review.

## Plan and decompose

1. Form a short outcome-focused plan before implementation or delegation.
2. Identify the immediate blocker and keep it with the parent when local
   progress depends on it.
3. Split only bounded work. Parallelize only assignments that are independent
   and have disjoint write ownership.
4. Read [references/contracts.md](references/contracts.md) before the first
   delegated write or strict review in a task.
5. Send every worker the complete task packet from that reference. Use
   `fork_turns="none"` when selecting a custom worker so the packet, not leaked
   parent context, defines the assignment.
6. Keep delegated communication and reports in English by default. Set another
   report language explicitly in the task packet only when the user-facing
   workflow or parent integration needs it. Repository content still follows
   the task and repository conventions.
7. Keep shared-file edits, unresolved design decisions, and dependency chains
   serial.

## Select agents

Apply the selected execution mode before routing:

- In solo mode, do not spawn any agent.
- In solo-reviewed mode, spawn no implementation worker and reserve reviewer
  spawns for the final strict gate and any required re-review.
- In team mode, spawn at least one bounded implementation worker.
- In auto mode, spawn only agents that materially improve the outcome.

- Use `terra_worker` for the default implementation path and for ambiguous,
  coupled, multi-file, architecture-sensitive, backend, frontend, database,
  integration, debugging, and refactoring work.
- Use `luna_worker` when the assignment is narrow, low-coupling, mechanical, or
  high-throughput with explicit acceptance criteria. Good fits include isolated
  tests, fixtures, documentation-adjacent code, repetitive migrations, and
  independent file clusters.
- Use `solweaver_reviewer` only as a fresh, read-only reviewer. It never
  implements its own findings.
- Prefer Terra and strict mode when incorrect routing could affect a high-risk
  boundary.
- Use `code_mapper`, `tester`, `reviewer`, or `security_reviewer` only when the
  current runtime exposes them and their specialization materially helps.
- Use another implementation agent only when the user explicitly requests it.

When workers are allowed, parallelize disjoint assignments within the
configured concurrency limit; the limit is a ceiling, not a target. Terra and
Luna may run together only when their ownership is disjoint.

## Coordinate execution

Apply these rules to active subagents. In solo mode, keep all execution local
to the parent.

1. Tell every writing agent it is not alone in the codebase, must preserve
   unrelated edits, and owns only its assigned scope.
2. Assume native subagents share the active working tree unless the host
   explicitly reports an isolated worktree. Disjoint file ownership is not the
   same as filesystem isolation.
3. Create a separate user-visible task or worktree only when the user explicitly
   authorizes that action and the current surface supports it.
4. Continue parent-owned inspection, integration planning, or blocker work
   while independent agents run.
5. Track dependencies and progress. Correct missing evidence or scope drift in
   the responsible worker; do not create a replacement merely to avoid a
   correction loop.
6. Resolve overlaps and conflicts centrally. Never ask workers to orchestrate
   the team.

## Integrate and verify

1. When workers exist, treat their reports as claims. In every mode, inspect
   the working tree, complete diff, and changed-file scope.
2. Review for correctness, maintainability, contract compatibility, and
   interaction with concurrent edits.
3. Rerun focused checks first, then broader checks proportionate to risk.
   Distinguish static, unit, integration, runtime, acceptance, delivery, and
   production evidence; one level does not prove another.
4. Compare the evidence with the original acceptance criteria and note anything
   not run or not proved.
5. In strict mode, including solo-reviewed execution, spawn a fresh
   `solweaver_reviewer` with
   `fork_turns="none"` after parent verification. Send the strict review packet
   and require exactly `ship`, `fix-first`, or `rethink`.
6. On `fix-first`, return concrete findings to the responsible worker, or fix
   them in the parent for solo-reviewed execution. Verify again and obtain a
   new fresh review. On `rethink`, revise the architecture before more
   implementation. Only `ship` permits strict acceptance.
7. Stop completed subagent threads when the current surface supports it.

## Deliver

Lead with the usable outcome. Report changed files, verification actually run,
the execution mode, assurance mode, reviewer verdict when applicable,
remaining risks or unsupported behavior, and any action still requiring user
approval. Do not describe configured routing as observed runtime, or repository
checks as live production evidence. Do not deploy, mutate production, commit,
merge, push, or open a pull request unless the user authorized that external
action.
