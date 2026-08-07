---
name: solweaver
description: >-
  Run Sol-led software development in auto, solo, solo-reviewed, or team modes,
  with GPT-5.6 Sol owning planning, implementation or delegation, integration,
  verification, and delivery; terra_worker and luna_worker providing bounded
  implementation; and solweaver_reviewer providing one fresh final-strict
  review at a declared batch boundary. Use for software-development prompts
  beginning with Goal: or /goal, or when the
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
   - **Observed**: current session `turn_context` reports model and effort.
   - **Configured**: a validated agent definition pins the value, but runtime
     metadata does not expose it.
   - **Unverified**: neither source establishes the value.
6. If the observed parent is not Sol Max, stop before implementation and direct
   the user to select `gpt-5.6-sol` with `max` reasoning. If the parent is
   unverified, do not claim it is Sol Max.
7. Enforce the package-owned child identity matrix: `terra_worker` requires
   `model == "gpt-5.6-terra"` and `effort == "max"`; `luna_worker` requires
   `model == "gpt-5.6-luna"` and `effort == "max"`; and
   `solweaver_reviewer` requires `model == "gpt-5.6-sol"` and
   `effort == "max"`.
8. After every package-owned child turn, inspect the child session
   `turn_context` before accepting its report or verdict. If either value
   differs or metadata is unavailable, mark the lane mismatched or unverified
   and apply the handling in
   [references/contracts.md](references/contracts.md). A model-generated
   self-report, task label, or UI name is not runtime proof.
9. Do not impose a fixed model gate on optional platform specialists that this
   package does not define. Report their runtime as observed, configured, or
   unverified, and honor any explicit runtime requirement from the user.
10. Preserve user changes, repository boundaries, and explicit external-action
   approval requirements.
11. After installing or changing Solweaver definitions, run
    `scripts/validate_install.py`, restart Codex or open a new task, and follow
    [references/runtime-smoke-test.md](references/runtime-smoke-test.md) before
    describing the workflow as runtime-certified.

## Choose execution mode

- Use **auto mode** when the user does not name a mode. Sol chooses local solo
  execution or the smallest useful team; invoking Solweaver alone does not
  require a subagent.
- Use **solo mode** when the user wants Sol alone. Sol plans, implements,
  verifies, and delivers without spawning any worker or reviewer. Solo supports
  standard assurance only.
- Use **solo-reviewed mode** when the user wants Sol to implement alone with an
  independent final gate. Do not spawn implementation workers; after parent
  verification at the final-strict boundary, spawn one fresh
  `solweaver_reviewer` at a time and apply final-strict acceptance, including a
  fresh review after a fix round only while review budget remains.
  Solo-reviewed always uses final-strict assurance.
- Use **team mode** when the user explicitly requests delegation. Spawn at
  least one bounded implementation worker, while Sol retains integration and
  verification. Add the fresh reviewer only when a final-strict batch reaches
  its gate.
- Honor an explicit mode without silently changing it. If solo mode conflicts
  with a user-requested or risk-triggered independent review, stop before
  implementation and ask the user to choose solo with standard assurance,
  solo-reviewed, or auto/team execution with final-strict assurance.

## Choose assurance

- Use **standard mode** for ordinary work in auto, solo, or team execution. Sol
  inspects the diff, reruns verification, and accepts or returns the work.
- Use **final-strict mode** when the user wants one independent review over a
  coherent completed phase or batch, or when the change affects auth,
  authorization, secrets, tenant isolation, money, data integrity, migrations,
  destructive behavior, concurrency, public APIs, production-critical paths,
  or a wide architectural refactor. Record the exact base state, batch
  objective, acceptance criteria, final boundary, and cumulative evidence.
  Apply standard parent verification after every intermediate checkpoint, do
  not spawn `solweaver_reviewer` yet, and report only `checkpoint-ready`.
- At the declared final boundary, inspect the complete cumulative diff from the
  recorded base, rerun proportionate integration and acceptance checks, then
  apply the fresh reviewer gate and final-strict acceptance rules.
  Final-strict is compatible with auto, team, or solo-reviewed execution, but
  not plain solo because its final review is independent.
- Final-strict is the only independent-review assurance mode. Auto and team use
  standard assurance unless final-strict is requested or risk-triggered;
  solo-reviewed always uses final-strict.
- Set `MAX_REVIEW_CALLS = 2` for each final-strict batch. Count every
  `solweaver_reviewer` spawn that begins execution, including attempts with
  missing or mismatched runtime metadata or an unusable verdict. Never spawn a
  third reviewer for the same batch.
- Permit final-strict execution during high-risk implementation only
  while it remains reversible and no protected boundary is crossed. Before a
  destructive migration, real money movement, production auth or authorization
  change, deploy, merge, release, or other irreversible external mutation,
  complete the final-strict gate for the relevant cumulative change or stop.
- If a final-strict batch becomes too broad or incoherent for one complete
  review, pause and ask the user to split it into reviewable batches. Never
  omit parts of the diff merely to preserve a one-review target.
- Never describe solo execution or a parent self-review as independent review.
  Never describe an intermediate final-strict checkpoint as `ship` or
  final-strict acceptance.

## Plan and decompose

1. Form a short outcome-focused plan before implementation or delegation.
2. Identify the immediate blocker and keep it with the parent when local
   progress depends on it.
3. Split only bounded work. Parallelize only assignments that are independent
   and have disjoint write ownership.
4. Read [references/contracts.md](references/contracts.md) before the first
   delegated write or final-strict review in a task.
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
  spawns for the final-strict gate and any required re-review.
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
- Prefer Terra and final-strict assurance when incorrect routing could affect a
  high-risk boundary.
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
7. If a Terra or Luna runtime gate fails, do not accept the worker report as
   evidence or count that lane as correctly routed. Inspect the shared
   worktree and complete diff, preserve all unrelated changes, and never roll
   back child edits automatically.
8. In auto mode, Sol may take ownership of inspected changes and verify them
   locally, but must report the failed worker lane. In explicit team mode,
   pause before further implementation and either make one corrected
   re-dispatch when the expected runtime is available or request user
   direction. Never downgrade an explicit team request silently.

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
5. In final-strict mode at each intermediate checkpoint, update the referenced
   batch ledger with changed scope, verification, decisions, and known gaps.
   Do not spawn the final-strict reviewer and do not claim more than
   `checkpoint-ready`.
6. At the final-strict boundary, re-establish the recorded base, inspect the
   complete cumulative diff, reconcile every checkpoint with the batch
   acceptance criteria, and rerun final integration or acceptance evidence.
7. If final-strict work approaches a protected irreversible or production
   boundary before the declared end, treat that boundary as the final gate for
   the relevant accumulated change. Do not cross it with deferred review.
8. At a final-strict boundary, including solo-reviewed execution, verify that
   review budget remains, set `THIS_CALL` to the next call number, then spawn a
   fresh `solweaver_reviewer` with
   `fork_turns="none"` after parent verification. Send the final-strict review
   packet with the call number and require exactly `ship`, `fix-first`, or
   `rethink`. Increment `REVIEW_CALLS_USED` as soon as the child begins
   execution; a spawn that never starts does not consume a call.
9. Before accepting the verdict, inspect the reviewer child session
   `turn_context`. Accept it only when `model == "gpt-5.6-sol"` and
   `effort == "max"`. Reject missing or mismatched metadata and do not count
   the verdict as final-strict-review evidence. Never use a model-generated
   self-report as runtime proof. The failed attempt still consumes one review
   call because it began execution.
10. On `fix-first`, close the reviewer, return concrete findings to the
   responsible worker, or fix them in the parent for solo-reviewed execution.
   Verify again and complete the referenced `fix-first` closure matrix before
   using the second and final call. The new reviewer still inspects the full
   cumulative diff independently and may reject a claimed closure or raise new
   findings. On `rethink`, reconcile the architecture before more
   implementation and use the remaining call only after parent verification.
11. When call 2 returns anything other than a valid `ship`, or its runtime gate
   fails, set `REVIEW_STATUS: review-exhausted` and enter parent-owned
   completion. Perform the referenced design/acceptance reconciliation, make
   the narrowest conservative decisions consistent with the original goal and
   repository contracts, implement every addressable fix, inspect the complete
   diff, and rerun proportionate verification. Do not ask the user merely to
   resolve review exhaustion. Do not spawn call 3, reset the counter, switch
   workflows, lower the review bar, or claim final-strict completion.
12. Only a valid `ship` within the two-call budget permits final-strict
   acceptance. Without it, finish authorized reversible work as
   `FINAL_STATUS: parent-completed` with
   `ASSURANCE_STATUS: final-strict-not-achieved` when the acceptance criteria
   are met. Never invent authority for deploy, merge, release, money movement,
   destructive migration execution, or another protected external action;
   leave that action unexecuted and report the boundary.
13. Stop completed subagent threads when the current surface supports it.

## Deliver

Lead with the usable outcome. Report changed files, verification actually run,
the execution mode, assurance mode, final-strict base and boundary when
applicable, reviewer verdict, reviewer call counts, re-review rounds, child
runtime checks and any mismatched or unverified lanes, review budget and
`review-exhausted`, `parent-completed`, and assurance status when applicable,
remaining risks or unsupported behavior, and any protected external action
left unexecuted. Do not describe configured routing as observed runtime, or
repository checks as live production evidence. Do not deploy, mutate
production, commit, merge, push, or open a pull request unless the user
authorized that external action.
