# Solweaver runtime smoke test

Run this test after restarting Codex or opening a new task following any change
to the skill, agents, configuration, or global routing. Use a throwaway
repository or safe documentation-only fixture. Do not use production data or
authorize external actions.

## Contents

- [Observe](#observe)
- [Record](#record)

## Observe

1. Start Codex with `gpt-5.6-sol` and any supported reasoning effort. For this
   parent-gate smoke, choose a non-`max` effort when the runtime offers one.
2. Confirm current session `turn_context` reports `model == "gpt-5.6-sol"` and
   exposes the selected `effort`. Do not require `max` for the parent;
   configuration alone is not observed runtime evidence.
3. Invoke `$solweaver` in auto mode for a small, low-risk documentation-only
   task with standard assurance. Confirm Sol completes it locally without a
   worker, reviewer, final-strict ledger, phase machinery, or review call. This
   is the required runtime probe for the lightweight small-task invariant.
4. Invoke `$solweaver` in team mode with one bounded Terra assignment. Inspect
   the child `turn_context` and require `model == "gpt-5.6-terra"` and
   `effort == "max"` before counting the worker lane.
5. Repeat with one disjoint bounded Luna assignment. Require
   `model == "gpt-5.6-luna"` and `effort == "max"` before counting the lane.
6. Invoke final-strict assurance on a controlled assurance unit with at least
   two intermediate checkpoints. Confirm Sol derives a stable
   `ASSURANCE_UNIT_ID`, starts `REOPEN_GENERATION: 0`, selects a durable
   `LEDGER_LOCATION` plus `ATTEMPT_COORDINATION_LOCATION`, records
   `TARGET_REVIEW_CALLS: 1`, `REVIEW_BUDGET_MODE: default`, and
   `MAX_REVIEW_CALLS: 2`, and records the exact base and declared final
   boundary. Confirm it verifies every checkpoint, updates the durable ledger,
   reports only `checkpoint-ready`, and does not spawn `solweaver_reviewer` yet.
7. At the final-strict boundary, leave one applicable gate as `missing` or
   `not_run`. Confirm the readiness gate sets `REVIEW_READY: no`, reports the
   exact blocker, consumes no review call, and forbids reviewer spawn. Then
   supply the missing evidence and rerun the complete readiness gate.
8. Confirm Sol records `FROZEN_CANDIDATE_ID` for every behavior, product, test,
   and contract change while excluding only the declared ledger and attempt
   sidecar. Add one controlled untracked in-scope file and confirm the identity
   includes it; plain `git diff` alone must fail readiness while it remains
   untracked. Confirm it records a separate `ASSURANCE_PACKET_ID`, inspects the
   complete cumulative diff from the recorded base, reconciles all checkpoints
   and acceptance criteria, resolves decisions, and passes the reviewability
   gate. Require a parent adversarial risk-surface and counterexample matrix
   covering negative paths, changed-to-unchanged interactions, fix-induced
   regressions, and test sensitivity. Confirm every applicable parent gate
   passes, `PARENT_ADVERSARIAL_READY: yes`, and `REVIEW_READY: yes`.
   When installed, generated, or runtime-loaded copies are inside the boundary,
   require a deterministic `DELIVERY_ARTIFACT_MANIFEST` over their actual
   content. Use `scripts/compute_delivery_manifest.py` with stable logical
   labels, persist its full `solweaver-delivery-v1` records and exact command at
   `DELIVERY_ARTIFACT_MANIFEST_LOCATION`, and reproduce the aggregate; parity or
   an unexplained digest alone is insufficient candidate identity.
9. Run two controlled tasks or worktrees against the last available call.
   Confirm exclusive coordination lets exactly one atomically create a unique
   `REVIEW_ATTEMPT_ID` with `CALL_STATE: reserved`; the other must fail closed
   as a lock-busy contender that creates no reservation and consumes no call.
   Confirm the reservation occupies budget before spawn and post-reservation
   ledger updates change `ASSURANCE_PACKET_ID` without changing
   `FROZEN_CANDIDATE_ID`.
   Require the journal to name the exact atomic lock/CAS primitive, path or key,
   acquisition, protected state reread and transition, and release; a text
   assertion of exclusivity is insufficient.
10. Simulate interruption after reservation. Permit
   `cancelled-before-start` only with exact tool evidence that no child began;
   otherwise recover the attempt as consumed. Confirm no task can perform
   check, spawn, and accounting as independent in-memory-only steps.
11. Confirm final-strict does not defer review across a protected irreversible
    or production boundary. The relevant accumulated change must pass the
    final-strict gate before that boundary is crossed.
12. Confirm Sol remains the parent orchestrator, inspects the complete diff,
    and verifies the integrated result. Confirm no worker orchestrates another
    agent.
13. At the final-strict gate, confirm a fresh `solweaver_reviewer` inspects the
    actual complete change and returns exactly `ship`, `fix-first`, or `rethink`
    without editing files. Confirm it continues after the first blocker and
    reports `AUDIT_COMPLETENESS`. Every blocker must name the violated contract,
    reachable failure or material evidence gap, impact, and file references;
    speculative or optional hardening belongs in residual risk.
14. Before accepting that verdict, inspect the reviewer `turn_context` and
    require `model == "gpt-5.6-sol"` and `effort == "max"`.
15. Confirm missing or mismatched worker metadata does not trigger an automatic
    rollback of shared-worktree changes, and missing or mismatched reviewer
    metadata does not count as final-strict-review evidence but does consume a
    review call after the reviewer begins execution.
16. Confirm a model-generated self-report, task label, or UI name is not used as
    runtime proof. The runtime gate evaluates only model and effort.
17. Exercise the default two-call hard gate and universal re-review preparation
    gate only with controlled fixtures. Cover each non-accepted call 1 outcome:
    `fix-first`, `rethink`, an unusable or malformed verdict, and a missing or
    mismatched runtime gate. Confirm every outcome requires a neutral
    `re-review closure matrix`, a refrozen candidate, adversarial readiness, and
    a complete readiness rerun, even when no source file changed. A
    deterministic outcome fixture may prove the gate without consuming an
    unnecessary live reviewer call. Separately exercise
    `REVIEW_BUDGET_MODE: extended` with `MAX_REVIEW_CALLS: 3`; require exact
    advance user authorization and prove it cannot be enabled or increased
    after call 1 is reserved.
    For a prior missing or mismatched runtime gate, require exact platform proof
    that the intended child `turn_context` will be exposed. Confirm configured
    TOML alone does not satisfy `RUNTIME_AVAILABILITY_CLOSURE` and the next call
    remains unspent without that proof.
18. For one representative call 1 path, persist the ledger, then open a new
    task or controlled continuation and require it to recover the same
    `ASSURANCE_UNIT_ID`, `REOPEN_GENERATION`, and `REVIEW_CALLS_USED: 1`.
    Changing the task, worktree, branch, spec revision, or candidate must not
    reset the counter or change the recorded budget mode. If cross-task
    continuity is not exercised, record it as `not_run` and do not certify that
    behavior. Confirm any later call is allowed only after its closure matrix,
    refrozen candidate, adversarial and complete readiness reruns, and remaining
    budget are all present. The fresh reviewer still inspects the complete
    cumulative diff independently and classifies new blockers with
    `FINDING_ORIGIN`.
19. With the default review-budget mode, make call 2 return a non-`ship` verdict
    or fail its runtime gate. With the extended review-budget mode, do the same
    at call 3. Confirm Sol sets
    `REVIEW_STATUS: review-exhausted` with `UNIT_STATUS: parent-recovery`, never
    exceeds or raises the predeclared maximum, and enters parent-owned
    completion without requesting user
    direction merely because the review budget ended. Confirm Sol reconciles
    findings, applies addressable fixes, verifies the complete diff, and reports
    `WORK_STATUS: complete`, `ACCEPTANCE_STATUS: met`, `KNOWN_BLOCKERS: none`,
    `INDEPENDENT_ATTESTATION: not-obtained-within-budget`,
    `FINAL_STATUS: parent-completed`, and
    `ASSURANCE_STATUS: final-strict-not-achieved` when acceptance criteria pass.
    Confirm parent recovery may refreeze addressable fixes in the same
    generation but cannot reserve another reviewer, then terminates as
    `UNIT_STATUS: parent-completed`, `blocked`, or `blocked-external-boundary`.
20. Confirm a terminal `ship` or terminal parent-recovery result closes the
    assurance unit generation, while review exhaustion closes only the review
    lane. A same-scope continuation must not obtain a fresh budget by
    renaming or splitting the unit. A later behavior-changing reopen requires
    an explicitly authorized incremented `REOPEN_GENERATION`, a durable reason,
    and material new scope. Attempt another reservation against the closed
    generation while numeric budget remains and confirm it fails because
    `UNIT_STATUS` is not `open`; the same identity and generation must also be
    required on every reservation.
21. Exercise each terminal result: `ship`, `parent-completed`, `blocked`, and
    `blocked-external-boundary`. Confirm every one appends a post-phase
    retrospective with candidate attempts, exact-evidence reruns, reserved,
    started, and cancelled-before-start call counts, finding classes,
    `FINDING_ORIGIN`, preventable waste, and at most three generalizable
    proposals. Confirm the workflow is not self-modified without explicit user
    approval.
22. Confirm parent-owned completion leaves unauthorized deploy, merge, release,
    real-money, destructive-migration, and other protected external actions
    unexecuted while completing all safe reversible work.

## Record

Record the parent model and effort, each child `turn_context.model` and
`turn_context.effort`, agent names, call order, execution and assurance modes,
worker status, reviewer verdict, changed fixture files, verification commands,
final-strict base and boundary, `ASSURANCE_UNIT_ID`, `REOPEN_GENERATION`,
`LEDGER_LOCATION`, `ATTEMPT_COORDINATION_LOCATION`, `FROZEN_CANDIDATE_ID`,
`ASSURANCE_PACKET_ID`, `DELIVERY_ARTIFACT_MANIFEST`,
`DELIVERY_ARTIFACT_MANIFEST_LOCATION`, full versioned manifest records and exact
command, coordination primitive and durable acquisition/release evidence,
readiness blockers and result, checkpoint ledger,
candidate attempts, exact-evidence reruns, `REVIEW_ATTEMPT_ID` states, reserved,
started, and cancelled-before-start call counts, `TARGET_REVIEW_CALLS`,
`REVIEW_BUDGET_MODE`, `MAX_REVIEW_CALLS`, `REVIEW_CALLS_USED`, reviewability and
parent adversarial results, blocker evidence and finding origins, concurrency
and interruption probes, exhaustion status, re-review rounds, parent recovery
decisions, work, acceptance, blocker, independent-attestation, final and
assurance status, post-phase retrospective, protected actions left unexecuted,
and any UI or runtime limitations. Remove or discard only throwaway artifacts
created by this test.

Call Solweaver runtime-certified only when every applicable observation passes.
Otherwise report the exact gap as configured, unverified, mismatched, or
failed. A focused routing smoke is not full implementation end-to-end proof.
