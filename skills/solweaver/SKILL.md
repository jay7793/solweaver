---
name: solweaver
description: >-
  Run Sol-led software development in auto, solo, solo-reviewed, or team modes,
  with GPT-5.6 Sol owning planning, implementation or delegation, integration,
  verification, and delivery; terra_worker and luna_worker providing bounded
  implementation; and solweaver_reviewer providing one fresh final-strict
  review at a declared assurance-unit boundary. Use when explicitly invoked
  for any software-development task, including small fixes; for
  software-development prompts beginning with Goal: or /goal; or when the user
  requests Sol-only work, a software team, agents, subagents, parallel work, or
  delegated implementation. Do not use for general questions, research,
  writing, or operations-only requests.
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
3. Keep the active parent as orchestrator. Require `gpt-5.6-sol` as the parent
   model, but allow any reasoning effort reported by the current `turn_context`.
   This skill cannot select or prove the runtime.
4. Inspect agent availability only when the selected path actually needs an
   agent. Auto or solo execution with standard assurance does not require a
   worker or reviewer to be available. Do not silently substitute a missing
   agent when an explicit mode or assurance gate requires it.
5. Describe model evidence precisely:
   - **Observed**: current session `turn_context` reports model and effort.
   - **Configured**: a validated agent definition pins the value, but runtime
     metadata does not expose it.
   - **Unverified**: neither source establishes the value.
6. If the observed parent model is not `gpt-5.6-sol`, stop before
   implementation and direct the user to select that model. Do not reject an
   observed Sol parent based on its reasoning effort. If the parent model or
   effort metadata is unavailable, do not claim the parent runtime gate passed.
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
11. Keep Solweaver project-neutral. Discover language, framework, commands,
    repository layout, product contracts, and evidence conventions from the
    active workspace. Keep project-specific names, paths, requirements, and
    governance in task-local artifacts rather than the Solweaver package.
12. After installing or changing Solweaver definitions, run
    `scripts/validate_install.py`, restart Codex or open a new task, and follow
    [references/runtime-smoke-test.md](references/runtime-smoke-test.md) before
    describing the workflow as runtime-certified.

## Choose execution mode

- Use **auto mode** when the user does not name a mode. Sol chooses local solo
  execution or the smallest useful team; invoking Solweaver alone does not
  require a subagent.
- For small, low-risk, low-coupling tasks in auto mode, prefer local solo
  execution with standard assurance. Do not spawn a worker or reviewer, create
  final-strict artifacts, or add phase machinery merely because Solweaver was
  invoked.
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
  verification. Add the fresh reviewer only when a final-strict assurance unit
  reaches its gate.
- Honor an explicit mode without silently changing it. If solo mode conflicts
  with a user-requested or risk-triggered independent review, stop before
  implementation and ask the user to choose solo with standard assurance,
  solo-reviewed, or auto/team execution with final-strict assurance.

In auto mode, spawn only when at least one concrete benefit outweighs the
coordination cost: a disjoint lane can shorten the critical path, context
isolation reduces material risk, or the worker is a substantially better fit
for a bounded assignment. File count, task size labels, or skill invocation
alone are not reasons to delegate. Prefer one worker; add another only for
independent write scopes that can make useful progress concurrently.

## Choose assurance

- Use **standard assurance** for ordinary work in auto, solo, or team execution.
  Sol inspects the complete diff, reruns proportionate verification, and
  accepts or returns the work without final-strict artifacts or a reviewer.
- Use **final-strict assurance** when the user wants one independent review over
  a coherent completed phase or delivery unit, or when the change affects auth,
  authorization, secrets, tenant isolation, money, data integrity, migrations,
  destructive behavior, concurrency, public APIs, production-critical paths,
  or a wide architectural refactor. Before implementation, assign a stable
  `ASSURANCE_UNIT_ID`, set `REOPEN_GENERATION`, choose a durable
  `LEDGER_LOCATION` plus an exclusive `ATTEMPT_COORDINATION_LOCATION`, and
  record the exact base state, objective, acceptance criteria, final boundary,
  and cumulative evidence. Derive the identity from repository and product
  authority such as repository, track, and canonical phase or delivery ID;
  never derive it from a task, thread, worktree, branch, timestamp, or candidate
  SHA.
  Apply standard parent verification after every intermediate checkpoint, do
  not spawn `solweaver_reviewer` yet, and report only `checkpoint-ready`.
- At the declared final boundary, inspect the complete cumulative diff from the
  recorded base, rerun proportionate integration and acceptance checks, then
  pass the referenced final-strict readiness gate before applying the fresh
  reviewer gate and final-strict acceptance rules.
- Final-strict is Solweaver's only independent-review assurance mode. Auto and
  team use standard assurance unless final-strict is requested or
  risk-triggered; solo-reviewed always uses final-strict. Readiness must lead
  to a fresh `solweaver_reviewer` attempt; parent self-review never satisfies
  the independent gate.
- Record `REVIEW_BUDGET_MODE` before reviewer call 1. Use `default` unless the
  user explicitly authorizes `extended` in advance: `default` sets
  `TARGET_REVIEW_CALLS = 1` and `MAX_REVIEW_CALLS = 2`; `extended` keeps the
  one-call target and sets a hard maximum of 3. Once any call is reserved, never
  increase or change the mode. Count every `solweaver_reviewer` spawn that
  begins execution, including attempts with missing or mismatched runtime
  metadata or an unusable verdict. Carry `REVIEW_CALLS_USED` across tasks,
  chats, continuations, worktrees, branches, spec revisions, and candidate
  commits. Never exceed the recorded maximum or reset it by renaming,
  splitting, or reopening unchanged scope. Extended budget is not a substitute
  for making the assurance unit coherent and reviewable.
- Keep the assurance-unit ledger in the repository's existing phase, build, or
  evidence log when one is authoritative. Otherwise choose a user-authorized
  durable artifact before implementation. It must survive task context and be
  recoverable from another worktree or continuation. Never create a competing
  generic ledger when repository guidance defines another authority. If a
  prior final-strict attempt is mentioned or discoverable but its exact call
  count cannot be reconstructed, treat the remaining budget as unknown and do
  not spawn a reviewer as though the count were zero.
- Keep reviewer-attempt coordination in a durable sidecar or repository-provided
  lock/CAS facility outside the frozen behavior candidate. A Markdown journal
  alone is not a lock: record and use an exact atomic primitive, path or key,
  acquisition result, protected state transition, and release. It must support
  an exclusive atomic reservation across tasks and worktrees. Before a spawn,
  reserve one call with a unique `REVIEW_ATTEMPT_ID` and `CALL_STATE: reserved`;
  a reservation occupies the remaining budget. A lock-busy contender creates
  no reservation and consumes no call. After the child begins, mark it
  `started` and increment `REVIEW_CALLS_USED`. Release a reservation as
  `cancelled-before-start` only when exact tool evidence proves the child never
  began. After interruption or ambiguous recovery, count the reservation as
  consumed. If exclusive reservation is unavailable, reviewer spawn is
  forbidden.
- Record a `FROZEN_CANDIDATE_ID` for the complete declared behavior scope and a
  separate `ASSURANCE_PACKET_ID` for the ledger, attempt journal, and evidence
  snapshot. Exclude only the declared ledger and coordination artifacts from
  the behavior-candidate identity; never omit product, test, contract, or other
  changed scope. Attempt accounting changes the assurance packet but does not
  invalidate the frozen candidate. Any change outside those declared artifacts
  requires candidate refreeze and a full readiness rerun.
  Include staged, unstaged, and untracked files inside the declared scope;
  `git diff` alone is not a complete candidate identity when untracked files
  exist.
- When installed, generated, or runtime-loaded copies are part of the declared
  acceptance boundary, bind their actual content into `FROZEN_CANDIDATE_ID`
  with a deterministic `DELIVERY_ARTIFACT_MANIFEST`. Point-in-time parity alone
  is evidence, not immutable identity. Use
  `scripts/compute_delivery_manifest.py` with stable logical labels and persist
  its full versioned per-file records, aggregate, and exact command at
  `DELIVERY_ARTIFACT_MANIFEST_LOCATION`; an unexplained aggregate is not
  reproducible. Mark it not applicable only when those copies are genuinely
  outside the boundary.
- Permit final-strict execution during high-risk implementation only
  while it remains reversible and no protected boundary is crossed. Before a
  destructive migration, real money movement, production auth or authorization
  change, deploy, merge, release, or other irreversible external mutation,
  complete the final-strict gate for the relevant cumulative change or stop.
- Before the first reviewer call, pass the referenced reviewability gate: one
  coherent objective, explicit invariant and risk surfaces, a complete diff
  that one reviewer can inspect in a single full pass, and captured cross-unit
  interactions. If it fails, redefine the delivery units before call 1;
  extended budget cannot repair incoherent scope. After a reviewer begins,
  splitting or renaming scope never replenishes the budget. Never omit parts
  of the diff merely to preserve the one-review target.
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
   pause before further implementation and make at most one corrected
   re-dispatch when the expected runtime is available; otherwise request user
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
5. In final-strict mode at each intermediate checkpoint, update the durable
   assurance-unit ledger with changed scope, verification, decisions, and
   known gaps.
   Do not spawn the final-strict reviewer and do not claim more than
   `checkpoint-ready`.
6. At the final-strict boundary, re-establish the recorded base, inspect the
   complete cumulative diff, reconcile every checkpoint with the assurance-unit
   acceptance criteria, and rerun final integration or acceptance evidence.
   Then perform a distinct parent adversarial pass over the frozen scope. Build
   a proportionate risk-surface map and counterexample matrix; inspect negative
   paths, changed-to-unchanged interactions, fix-induced regressions, and
   test-sensitivity evidence. Mark an item not applicable only with a concrete
   reason. This parent challenge is not independent review.
7. If final-strict work approaches a protected irreversible or production
   boundary before the declared end, treat that boundary as the final gate for
   the relevant accumulated change. Do not cross it with deferred review.
8. At a final-strict boundary, including solo-reviewed execution, complete the
   referenced readiness gate. Require a durable loaded ledger, stable identity,
   recorded review-budget mode, exact base, `FROZEN_CANDIDATE_ID`,
   `ASSURANCE_PACKET_ID`, fully classified acceptance criteria, resolved product
   and architecture decisions, a passed reviewability gate, complete cumulative
   diff, any required `DELIVERY_ARTIFACT_MANIFEST`,
   `PARENT_ADVERSARIAL_READY: yes`, every applicable parent gate green
   with no `missing` or `not_run`, justified `not-applicable` entries, working
   exclusive attempt coordination with durable acquisition proof,
   `UNIT_STATUS: open`, and `REVIEW_READY: yes`. A known gap is
   allowed only when the acceptance contract explicitly permits it and it
   cannot hide blocking risk. If any item fails, remain `checkpoint-ready`; the
   reviewer is forbidden and no review call is consumed.
9. When readiness is green, acquire exclusive attempt coordination, reread the
   durable ledger, and atomically verify the intended identity and generation,
   `UNIT_STATUS: open`, `REVIEW_READY: yes`, remaining budget, and no active
   reservation. Record `THIS_CALL`, a unique `REVIEW_ATTEMPT_ID`, and
   `CALL_STATE: reserved` before releasing the lock. Then spawn a fresh
   `solweaver_reviewer` with `fork_turns="none"` after parent verification and
   send both candidate and assurance-packet identities. When the child begins,
   reacquire coordination and atomically mark the attempt `started` plus
   increment `REVIEW_CALLS_USED`. If exact tool evidence proves it never began,
   mark `cancelled-before-start` and release the reservation. On interruption
   or uncertainty, recover the reservation as consumed. Require exactly
   `ship`, `fix-first`, or `rethink` and never rely on an in-memory-only counter.
10. Before accepting the verdict, inspect the reviewer child session
   `turn_context`. Accept it only when `model == "gpt-5.6-sol"` and
   `effort == "max"`. Reject missing or mismatched metadata and do not count
   the verdict as final-strict-review evidence. Never use a model-generated
   self-report as runtime proof. The failed attempt still consumes one review
   call because it began execution. Under exclusive coordination, finish the
   attempt as `completed` with its observed runtime gate and verdict or unusable
   outcome, then clear `ACTIVE_REVIEW_RESERVATION`. In the same protected
   transition set `UNIT_STATUS: ship` for an accepted `ship`, leave it `open`
   only when a predeclared call remains, or set
   `REVIEW_STATUS: review-exhausted` with `UNIT_STATUS: parent-recovery` after a
   non-`ship` final budget call. Any status other than `open` forbids another
   reservation in that generation even when numeric budget remains.
11. After any consumed call that does not produce a valid accepted `ship`,
   close that reviewer. If recorded budget remains, enter the universal
   re-review preparation gate. This includes `fix-first`, `rethink`, an
   unusable or malformed verdict, and a missing or mismatched runtime gate.
   Return concrete findings to the responsible worker, or fix them in the
   parent for solo-reviewed execution; reconcile architecture and scope on
   `rethink`; and correct packet, capacity, or runtime prerequisites for an
   unusable attempt.
   Refreeze the candidate, rerun parent verification,
   adversarial readiness, and the complete readiness gate, then complete the
   referenced `re-review closure matrix` before reserving the next call. The
   matrix is required even when no source file changed. Each fresh reviewer
   still inspects the full cumulative diff and may reject closure or raise a
   new finding, but every blocker must meet the referenced evidence bar and
   later-call findings must classify their origin. Scope, outcome type, or
   candidate changes never reset the budget.
   If the prior runtime gate was missing or mismatched, configured agent files
   do not close it: require `RUNTIME_AVAILABILITY_CLOSURE` with exact platform
   evidence that child `turn_context` will be exposed for the intended role
   before spending another call. If that prerequisite cannot be proved, do not
   spawn and preserve the remaining call.
12. When a call does not produce a valid `ship` and no recorded budget remains,
   atomically set `REVIEW_STATUS: review-exhausted` and
   `UNIT_STATUS: parent-recovery`, then enter parent-owned completion. Review
   is closed, but parent recovery in the same generation may refreeze the
   candidate without creating or replenishing reviewer budget.
   Perform the referenced design/acceptance reconciliation, make the narrowest
   conservative decisions consistent with the original goal and repository
   contracts, implement every addressable fix, inspect the complete diff, and
   rerun proportionate verification. Do not ask the user merely to resolve
   review exhaustion. Do not exceed the recorded maximum, raise the budget,
   reset the counter, switch workflows, lower the review bar, or claim
   final-strict completion.
13. Only a valid `ship` within the recorded budget permits final-strict
   acceptance. Without it, finish authorized reversible work as
   `WORK_STATUS: complete`, `ACCEPTANCE_STATUS: met`, `KNOWN_BLOCKERS: none`,
   `INDEPENDENT_ATTESTATION: not-obtained-within-budget`, and
   `FINAL_STATUS: parent-completed` with
   `ASSURANCE_STATUS: final-strict-not-achieved` only after every addressable
   blocker is resolved. If a genuine external decision or protected boundary
   prevents completion, report the exact blocked status instead. Atomically
   finish recovery as `UNIT_STATUS: parent-completed`, `blocked`, or
   `blocked-external-boundary`; none permits another reviewer reservation.
   Never invent
   authority for deploy, merge, release, money movement, destructive migration
   execution, or another protected external action; leave it unexecuted.
14. A valid `ship` or a terminal parent-recovery result closes the current
   assurance unit generation. Review exhaustion closes only the independent
   review lane; it does not forbid addressable parent recovery inside the same
   generation and never replenishes calls. Non-behavioral evidence or status
   closure does not reopen it.
   Later behavior-changing work requires an explicitly authorized incremented
   `REOPEN_GENERATION`, a durable reason, and material new scope. Never reopen
   unchanged code or unresolved findings merely to obtain more review calls.
15. After every terminal result—valid `ship`, `parent-completed`, `blocked`, or
   `blocked-external-boundary`—record the referenced post-phase retrospective.
   Capture candidate attempts, evidence reruns, reserved and started reviewer
   calls, finding classes, preventable waste, and at most three generalizable
   workflow improvements. Do not modify Solweaver or repository governance
   automatically; present proposed workflow changes for user approval.
16. Stop completed subagent threads when the current surface supports it.

## Deliver

Lead with the usable outcome. Report changed files, verification actually run,
the execution mode, assurance mode, final-strict base and boundary when
applicable, `ASSURANCE_UNIT_ID`, `REOPEN_GENERATION`, ledger location,
attempt-coordination location, `FROZEN_CANDIDATE_ID`, `ASSURANCE_PACKET_ID`,
readiness result, reviewer verdict, reserved and started call counts, attempt
states, re-review rounds, child runtime checks and any mismatched or unverified
lanes, review-budget mode and exhaustion, `WORK_STATUS`, `ACCEPTANCE_STATUS`,
`KNOWN_BLOCKERS`, `INDEPENDENT_ATTESTATION`, final and assurance status when
applicable, post-phase retrospective status, remaining risks or unsupported
behavior, and any protected external action left unexecuted. Lead with work and
acceptance state so lack of independent attestation is not mistaken for
unfinished implementation. Do not describe configured routing as observed
runtime, or repository checks as live production evidence. Do not deploy,
mutate production, commit, merge, push, or open a pull request unless the user
authorized that external action.
