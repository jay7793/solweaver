# Solweaver contracts

Use these packets to keep delegated work bounded and reviewable. Replace every
placeholder; do not assume a fresh agent inherited parent context.

## Contents

- [Worker task packet](#worker-task-packet)
- [Final-strict assurance-unit ledger](#final-strict-assurance-unit-ledger)
- [Exclusive reviewer-call reservation and identity](#exclusive-reviewer-call-reservation-and-identity)
- [Reviewer blocker evidence bar](#reviewer-blocker-evidence-bar)
- [Final-strict review packet](#final-strict-review-packet)
- [Re-review closure matrix](#re-review-closure-matrix)
- [Review-budget exhaustion and parent completion](#review-budget-exhaustion-and-parent-completion)
- [Post-phase retrospective](#post-phase-retrospective)
- [Runtime identity gates](#runtime-identity-gates)
- [Final-strict protected boundaries](#final-strict-protected-boundaries)

## Worker task packet

```text
ROLE
Act as the assigned implementation worker. You are not alone in the codebase.
Preserve unrelated edits and own only the scope below.

EXECUTION MODE
<auto | team>

ASSURANCE MODE
<standard | final-strict>

OBJECTIVE
<Observable outcome and why it matters.>

OWNERSHIP
- Own: <exact files, modules, or bounded responsibility>
- Do not touch: <excluded files, modules, generated artifacts, or other work>

CONTRACTS
- <Interfaces, behavior, schemas, routes, or compatibility requirements>

CONSTRAINTS
- <Repository instructions, settled decisions, safety boundaries, and excluded scope>
- Do not deploy, mutate production, merge, push, or open a pull request.
- Return a blocker before changing files outside ownership.

REPORT LANGUAGE
English by default. Use <another language> only when the parent explicitly
requests it. Keep repository content in the language required by the task and
repository conventions.

ACCEPTANCE
- <Concrete behavior or artifact that must be true>
- <Regression or compatibility condition>

VERIFICATION
- Run: <exact focused command>
  Success: <expected exit status or output>
- Run: <exact broader command when proportionate>
  Success: <expected exit status or output>

RETURN
STATUS: complete | partial | blocked
CHANGES: <file-by-file summary from the actual diff>
VERIFIED: <commands run and concrete results>
JUDGMENT CALLS: <decisions made, or none>
GAPS: <unfinished work, unrun checks, blockers, or none>
```

## Final-strict assurance-unit ledger

Create this ledger before the first final-strict implementation checkpoint and
keep it in a durable location that survives task context. Prefer the
repository's authoritative phase, build, or evidence log. Otherwise choose a
user-authorized artifact that another task or worktree can recover. Do not
create a competing generic ledger when repository guidance names an authority.

Derive `ASSURANCE_UNIT_ID` from stable repository and product identity, such as
`<repository>/<track>/<canonical-phase-or-delivery-id>`. A task, thread,
worktree, branch, timestamp, spec revision, or candidate SHA is not an
assurance-unit identity. Search for an existing ledger before starting work.
If earlier final-strict work is mentioned or discoverable but its call count
cannot be reconstructed, set the remaining budget to unknown and do not assume
zero calls were used.

```text
IDENTITY
- ASSURANCE_UNIT_ID: <stable repository/track/phase-or-delivery-id>
- REOPEN_GENERATION: <0 for first run, then explicitly authorized integer>
- LEDGER_LOCATION: <durable authoritative path or artifact>
- ATTEMPT_COORDINATION_LOCATION: <durable journal plus exact atomic lock/CAS primitive and path or key>
- UNIT_STATUS: open | ship | parent-recovery | parent-completed | blocked | blocked-external-boundary

AUTHORITY AND BOUNDARY
- Objective: <one coherent phase or delivery unit>
- Canonical scope authority: <phase, issue, PRD section, or equivalent>
- Acceptance criteria: <complete cumulative criteria>
- Base state: <exact SHA, branch/worktree, and initial dirty files>
- Spec or contract revision: <exact revision or not-applicable>
- Candidate scope: <all behavior, product, test, contract, and in-boundary
  installed/generated artifact paths; exclude only the declared ledger and
  attempt-coordination artifacts>
- DELIVERY_ARTIFACT_MANIFEST: <deterministic hash over installed/generated/runtime-loaded copies in the boundary, or justified not-applicable>
- DELIVERY_ARTIFACT_MANIFEST_LOCATION: <durable full versioned records and exact command, or justified not-applicable>
- FROZEN_CANDIDATE_ID: <exact SHA or immutable scoped diff identity>
- ASSURANCE_PACKET_ID: <immutable review-packet and ledger snapshot identity>
- Declared final boundary: <observable condition that triggers final-strict review>
- Protected boundaries: <migration execution, money movement, production auth,
  deploy, merge, release, or other irreversible actions that cannot be crossed>
- REVIEW_BUDGET_MODE: <default | extended>
- REVIEW_BUDGET_AUTHORITY: <default policy or exact advance user authorization>
- TARGET_REVIEW_CALLS: 1
- MAX_REVIEW_CALLS: <2 for default | 3 for extended>
- REVIEW_CALLS_USED: <0 | 1 | 2 | 3>
- ACTIVE_REVIEW_RESERVATION: <none or REVIEW_ATTEMPT_ID>

CHECKPOINTS
| Checkpoint | Changed scope | Parent verification | Decisions | Known gaps | Status |
| --- | --- | --- | --- | --- | --- |
| <id> | <files/modules> | <commands and results> | <material choices> | <gaps or none> | checkpoint-ready |

REVIEWABILITY GATE
- One coherent objective and invariant family: <yes or split-required>
- Explicit risk surfaces: <list>
- Complete diff inspectable in one full reviewer pass: <yes or split-required>
- Cross-unit and unchanged-code interactions captured: <yes or blocker>
- REVIEWABILITY: <pass | split-required>

PARENT ADVERSARIAL READINESS
| Risk or invariant | Counterexample or negative path | Reachable interaction | Prevention or behavior | Sensitivity evidence | Result |
| --- | --- | --- | --- | --- | --- |
| <risk> | <input, state, race, rollback, or failure> | <changed and unchanged paths> | <expected handling> | <test fails without fix, mutation/sabotage, direct proof, or justified not-applicable> | <pass or blocker> |

- Fix-induced regression pass: <commands and observed result>
- Acceptance-versus-implementation contradiction pass: <result>
- Unresolved assumptions: <none or blocker>
- PARENT_ADVERSARIAL_READY: <yes or no>

FINAL-STRICT READINESS GATE
- Stable identity and durable ledger loaded: <yes or blocker>
- Review-budget mode fixed before call 1: <mode, authority, and yes or blocker>
- Candidate and assurance-packet identities separated: <yes or blocker>
- Exact base and FROZEN_CANDIDATE_ID: <refs and yes or blocker>
- Acceptance criteria fully classified: <yes, with not-applicable reasons>
- Product and architecture decisions resolved: <yes or blocker>
- Reviewability gate: <pass or split-required>
- Complete cumulative diff from base: <command and observed scope>
- Parent adversarial readiness: <yes with matrix or blocker>
- Exclusive attempt coordination primitive and latest acquisition proof: <exact lock/CAS command or operation, durable journal evidence, and yes or blocker>
- Applicable parent gates: <commands and concrete green results>
- Missing or not-run applicable evidence: <none or blocker>
- Explicitly permitted non-blocking gaps: <contract basis or none>
- REVIEW_READY: <yes or no>
- REVIEW_BLOCKERS: <none or exact blockers>

REVIEW ATTEMPTS
| REVIEW_ATTEMPT_ID | Call | State | Runtime gate | Verdict | Outcome |
| --- | --- | --- | --- | --- | --- |
| <unique id> | <1, 2, or 3> | <reserved, started, completed, or cancelled-before-start> | <pass, mismatch, or unverified> | <ship, fix-first, rethink, or unusable> | <accepted, revise, or review-exhausted> |
```

## Exclusive reviewer-call reservation and identity

The attempt journal at `ATTEMPT_COORDINATION_LOCATION` is the authoritative
concurrency record, but a Markdown or text journal alone is not a lock. Pair it
with an exact exclusive primitive such as atomic directory or file creation,
`flock`, or a compare-and-set key that works across tasks and worktrees. Record
the primitive, path or key, acquisition result, state reread, transition, and
release in the durable journal. Keep both outside `FROZEN_CANDIDATE_ID`. A
tracked phase/build ledger may mirror the attempt state, but post-freeze
accounting is assurance metadata, not a behavior-candidate mutation.
A lock-busy contender creates no reservation and consumes no call. Only a
successfully created reservation occupies budget; an ambiguous created
reservation remains occupied until exact never-started proof permits
`cancelled-before-start`.

Before every reviewer spawn:

1. acquire the recorded exclusive primitive and reread `ASSURANCE_UNIT_ID`,
   `REOPEN_GENERATION`, `UNIT_STATUS`, candidate/packet identities, and budget;
2. fail closed unless the identity and generation match the intended call,
   `UNIT_STATUS: open`, `REVIEW_READY: yes`,
   `REVIEW_CALLS_USED < MAX_REVIEW_CALLS`, and
   `ACTIVE_REVIEW_RESERVATION: none`;
3. atomically create a unique `REVIEW_ATTEMPT_ID`, assign `THIS_CALL`, bind the
   current `FROZEN_CANDIDATE_ID` and `ASSURANCE_PACKET_ID`, set
   `CALL_STATE: reserved`, and make that reservation occupy the budget;
4. release coordination, spawn exactly that attempt, then reacquire coordination
   to mark it `started` and increment `REVIEW_CALLS_USED` when execution begins;
5. after the result, atomically mark it `completed` with runtime gate, verdict,
   and outcome, then clear `ACTIVE_REVIEW_RESERVATION`; in the same protected
   transition set `UNIT_STATUS: ship` for an accepted `ship`, keep it `open`
   only when another predeclared call remains, or set
   `REVIEW_STATUS: review-exhausted` with `UNIT_STATUS: parent-recovery` when the
   final budget call is non-`ship`; and
6. use `cancelled-before-start` and release the reservation only when exact tool
   evidence proves the child never began. After interruption or uncertainty,
   recover a lingering reservation as consumed before any later decision.

If the exclusive operation, state recovery, or identity separation cannot be
proved, set `REVIEW_READY: no` and do not spawn. Never perform check, spawn, and
accounting as independent in-memory-only steps.

Any `UNIT_STATUS` other than `open` forbids another reservation in that
generation even when numeric budget remains. A later material reopen first requires explicit
authorization, an incremented `REOPEN_GENERATION`, and a new ready candidate;
the stale generation can never spend its unused numeric capacity.

`checkpoint-ready` means parent-verified progress only. It is not `ship`, an
independent review, permission to cross a protected boundary, or evidence that
the final cumulative diff is reviewable. `REVIEW_READY: yes` requires every
applicable parent gate to be green; `missing` or `not_run` blocks review, while
`not-applicable` requires a concrete contract reason. If the assurance unit is
too broad or incoherent for one complete review, redefine it before call 1
rather than omitting scope from the final packet.

Carry `REVIEW_CALLS_USED` across tasks, chats, continuations, worktrees,
branches, spec revisions, and candidate commits. Splitting or renaming scope
after a reviewer begins does not replenish the budget. A valid `ship` or a
terminal parent-recovery result closes the generation. Review exhaustion closes
only the independent review lane: parent recovery may still refreeze and verify
addressable fixes in the same generation, but it can never reserve another
reviewer or replenish calls. Later behavior-changing work after terminal
closure requires an explicitly authorized incremented `REOPEN_GENERATION`, a
durable reason, and material new scope. Evidence-only status closure does not
reopen a unit, and unchanged code or unresolved findings cannot be reopened to
buy more calls.

When installed, generated, or runtime-loaded copies are part of the declared
acceptance boundary, bind their actual content into `FROZEN_CANDIDATE_ID` with a
deterministic `DELIVERY_ARTIFACT_MANIFEST`. Point-in-time parity by itself is
verification evidence, not immutable candidate identity. If such copies are
outside the boundary, say why they are not applicable instead of silently
omitting them.

Use `scripts/compute_delivery_manifest.py` with stable logical labels rather
than absolute-path-dependent output. Persist its complete
`solweaver-delivery-v1` output—version, sorted per-file records, and aggregate
digest—plus the exact command at `DELIVERY_ARTIFACT_MANIFEST_LOCATION`. Bind the
aggregate manifest line into `FROZEN_CANDIDATE_ID`. An unexplained aggregate
digest without the durable records and recipe is not reproducible evidence.

The repository component of `FROZEN_CANDIDATE_ID` must include every staged,
unstaged, and untracked path in candidate scope. Record the exact recipe. A
plain `git diff` omits untracked files and is insufficient whenever any are in
scope.

Use `REVIEW_BUDGET_MODE: default` with `MAX_REVIEW_CALLS: 2` unless the user
explicitly authorizes `extended` before call 1; extended sets
`MAX_REVIEW_CALLS: 3`. Record the authority in the ledger. After any call is
reserved, the mode and maximum are immutable. Never escalate automatically,
and never use extended budget to compensate for a failed reviewability gate.

## Reviewer blocker evidence bar

A reviewer must complete the whole review pass after finding a blocker and
return every blocking issue discovered in that pass. Do not stop after the
first finding or intentionally drip-feed findings across calls. If the complete
scope cannot be inspected in one pass, return `rethink` with
`AUDIT_COMPLETENESS: scope-too-broad`; do not present a partial blocker list as
a comprehensive review.

A finding is blocking only when the report establishes all of these:

1. the exact violated acceptance criterion, invariant, repository contract, or
   required safety property;
2. a concrete reachable code path, state transition, failing observation, or
   material evidence gap;
3. the correctness, security, data, compatibility, or user-visible impact;
4. precise file or contract references within the declared assurance unit; and
5. why existing evidence does not already close the issue.

Missing tests are blocking only when required or critical behavior lacks other
direct proof. Style preferences, speculative future concerns, optional
hardening, and low-confidence possibilities belong in `RESIDUAL_RISK`, not in
`FINDINGS`. A later-call blocker must also set `FINDING_ORIGIN` to one of
`pre-existing`, `introduced-by-fix`, `newly-exposed-evidence`, or
`acceptance-mismatch`, and explain the classification. These rules raise the
quality of a blocking verdict; they never suppress a real blocker.

## Final-strict review packet

Send this only after the parent has inspected the diff and rerun verification.
The reviewer must remain behaviorally read-only even if the host grants broader
filesystem permissions.

```text
ROLE
Act as a fresh read-only reviewer. Do not edit files, implement fixes, commit,
push, or orchestrate other agents.

EXECUTION MODE
<auto | solo-reviewed | team>

ASSURANCE MODE
<final-strict>

ASSURANCE UNIT
- ASSURANCE_UNIT_ID: <stable repository/track/phase-or-delivery-id>
- REOPEN_GENERATION: <integer loaded from durable ledger>
- LEDGER_LOCATION: <durable authoritative path or artifact>
- ATTEMPT_COORDINATION_LOCATION: <durable journal plus exact atomic lock/CAS primitive and path or key>
- UNIT_CONTINUITY_CHECKED: <yes, including prior tasks and review attempts>
- UNIT_STATUS: open
- COORDINATION_PRIMITIVE: <exact atomic lock/CAS operation and path or key>
- RESERVATION_EVIDENCE: <durable acquisition, reread, transition, and release record>

REVIEW BUDGET
- REVIEW_BUDGET_MODE: <default | extended, loaded from ledger>
- REVIEW_BUDGET_AUTHORITY: <default policy or exact advance user authorization>
- TARGET_REVIEW_CALLS: 1
- MAX_REVIEW_CALLS: <2 | 3, loaded from ledger and immutable after call 1 reservation>
- REVIEW_CALLS_USED: <count before this reserved call begins>
- REVIEW_ATTEMPT_ID: <unique durable id>
- CALL_STATE: reserved
- THIS_CALL: <1, 2, or 3 within recorded budget>

RE-REVIEW PREPARATION (complete when THIS_CALL is greater than 1)
- Required for this call: <yes or not-applicable for call 1>
- Prior call outcomes: <ordered outcomes or not-applicable for call 1>
- Candidate refrozen after closure: <exact identity or not-applicable for call 1>
- Complete readiness gate rerun: <yes with evidence, or not-applicable for call 1>
- Parent adversarial readiness rerun: <yes with evidence, or not-applicable for call 1>
- Neutral re-review closure matrix attached: <yes or not-applicable for call 1>

OBJECTIVE
<Original objective and acceptance criteria.>

CHANGE SCOPE
- Base or starting state: <exact ref or observed state>
- Intended files or modules: <scope>
- Actual changed files: <paths from parent inspection>
- Staged, unstaged, and untracked scope reconciliation: <complete paths and identity recipe>
- Candidate scope exclusions: <only declared ledger and coordination artifacts>
- FROZEN_CANDIDATE_ID: <exact immutable scoped identity>
- ASSURANCE_PACKET_ID: <exact immutable packet and ledger snapshot identity>
- DELIVERY_ARTIFACT_MANIFEST: <deterministic installed/generated/runtime-loaded content identity or justified not-applicable>
- DELIVERY_ARTIFACT_MANIFEST_LOCATION: <durable full versioned records and exact command or justified not-applicable>

RISK
- Assurance reason: <auth, money, migration, public API, production, etc.>
- Invariants: <behavior or data that must not regress>

EVIDENCE
- Diff inspected by parent: <yes and summary>
- Commands rerun by parent: <commands and concrete results>
- Reviewability gate: <pass>
- Parent adversarial readiness: <yes with risk/counterexample matrix>
- Applicable missing or not-run evidence: <none>
- Explicitly permitted non-blocking gaps: <contract basis or none>
- Product and architecture decisions resolved: <yes>
- REVIEW_READY: yes

FINAL-STRICT ASSURANCE UNIT
- Base state: <exact ref>
- FROZEN_CANDIDATE_ID: <exact SHA or immutable scoped diff identity>
- ASSURANCE_PACKET_ID: <review-packet and ledger snapshot identity>
- Declared final boundary: <boundary>
- Complete cumulative diff: <command and observed scope>
- Durable checkpoint ledger reconciled: <yes with summary>

REPORT LANGUAGE
English by default. Use <another language> only when the parent explicitly
requests it. Preserve quoted repository content when fidelity matters.

REVIEW
Inspect the actual files and complete diff. Prioritize correctness, regressions,
security, data integrity, concurrency, public contracts, and missing tests.
Apply the reviewer blocker evidence bar above. Continue the complete audit after
the first blocker and report every blocking finding discovered in this pass.
Classify every later-call finding with `FINDING_ORIGIN`. If the full scope cannot
be reviewed in one pass, return `rethink` rather than a partial audit.
Return exactly one verdict:
- ship: no blocking finding remains.
- fix-first: the design is viable but blocking fixes are required.
- rethink: architecture or scope must change before implementation continues.

RETURN
VERDICT: ship | fix-first | rethink
AUDIT_COMPLETENESS: complete | scope-too-broad
FINDINGS: <ordered evidence-bar-qualified blockers with contract, path, impact, file references, and later-call FINDING_ORIGIN; or none>
EVIDENCE: <what supports the verdict>
RESIDUAL RISK: <non-blocking uncertainty, optional hardening, or none>
```

## Re-review closure matrix

After any consumed call that does not produce a valid accepted `ship`, close
that reviewer. If recorded budget remains, complete this matrix before the next
review call. This universal gate covers `fix-first`, `rethink`, an unusable or
malformed verdict, and a missing or mismatched runtime gate. Implement bounded
findings, reconcile architecture or scope, or correct the packet/runtime
prerequisite as appropriate. Then refreeze the candidate, inspect the complete
diff, rerun parent verification, adversarial readiness, and the full readiness
gate. The matrix is required even when no source file changed. When no recorded
budget remains, go directly to review-budget exhaustion.

| Prior call | Outcome | Blocking item or failed gate | Exact closure | Changed files or decision artifact | Direct and sensitivity evidence | Runtime availability closure | Fix-induced regression check | Known limitations |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| <call number> | <fix-first, rethink, unusable, malformed, or runtime-failed> | <finding or gate> | <fix, decision, or corrected prerequisite> | <paths, decision record, or none> | <commands, tests, mutation/sabotage, or runtime proof> | <exact platform proof or not-applicable when prior runtime gate passed> | <result> | <remaining gap or none> |

Send the neutral matrix with every later review packet as accountability
evidence. Do not send the prior reviewer conversation, disposition, or an
expected verdict. The fresh reviewer must inspect the complete diff
independently and may reject a claimed closure or identify a new problem. Every
new blocker must meet the evidence bar and set `FINDING_ORIGIN`.

If a prior call had a missing or mismatched runtime gate, add
`RUNTIME_AVAILABILITY_CLOSURE` to the matrix. Configured TOML or self-report is
not closure. Require exact platform evidence that child `turn_context` will be
available for the intended role before another spawn; otherwise keep the
remaining call unspent and do not claim final-strict attestation.

## Review-budget exhaustion and parent completion

When a call does not produce a valid `ship` and `REVIEW_CALLS_USED` has reached
the predeclared `MAX_REVIEW_CALLS`, atomically set
`REVIEW_STATUS: review-exhausted` and `UNIT_STATUS: parent-recovery`.
Never exceed the recorded maximum or raise it after review begins. Sol owns the
recovery and completes the authorized task without asking the user merely to
resolve the review loop. Reconcile every remaining issue as one of:

1. implementation defect;
2. evidence defect;
3. unresolved product or architecture decision; or
4. mismatch between stated acceptance criteria and reviewer expectations; or
5. workflow or review-budget defect.

Record the classification, supporting facts, exact missing proof or decision,
and next action. Resolve decisions using this order: the original user goal and
acceptance criteria, repository instructions and contracts, compatibility with
existing behavior, then the narrowest reversible conservative implementation.
Implement every addressable fix, inspect the complete diff, and rerun
proportionate verification. Do not silently weaken semantics, expand authority,
force a workflow switch, lower the review bar, or treat review count as
permission to claim final-strict acceptance.

```text
ASSURANCE_UNIT_ID: <stable repository/track/phase-or-delivery-id>
REOPEN_GENERATION: <integer>
REVIEW_BUDGET_MODE: <default | extended>
TARGET_REVIEW_CALLS: 1
MAX_REVIEW_CALLS: <2 | 3 as predeclared>
REVIEW_CALLS_USED: <same as MAX_REVIEW_CALLS>
REVIEW_STATUS: review-exhausted
UNIT_STATUS: parent-recovery
NEXT_REVIEW_ALLOWED: no
REVIEW_LANE_STATUS: closed
PARENT_RECOVERY: reconcile-fix-verify
WORK_STATUS: complete | blocked
ACCEPTANCE_STATUS: met | not-met
KNOWN_BLOCKERS: none | <exact unresolved blocker>
INDEPENDENT_ATTESTATION: not-obtained-within-budget
FINAL_STATUS: parent-completed | blocked | blocked-external-boundary
ASSURANCE_STATUS: final-strict-not-achieved
USER_DECISION_REQUIRED: no for review exhaustion alone | <exact real decision if blocked>
```

Use `parent-completed` only when `WORK_STATUS: complete`,
`ACCEPTANCE_STATUS: met`, and `KNOWN_BLOCKERS: none` after parent recovery.
This is an explicit completed-work result with independent attestation not
obtained, not a silent downgrade or reviewer `ship`. A genuine unresolved
external decision or protected boundary may be reported as blocked; review
exhaustion by itself is not a user-decision blocker. Do not reset the counter,
create a continuation, switch worktrees, or rename the same unchanged assurance
unit to evade the cap.
Parent recovery may change and refreeze the candidate inside this same
generation because the review lane—not the authorized work lane—is exhausted.
After recovery, atomically set `UNIT_STATUS: parent-completed`, `blocked`, or
`blocked-external-boundary`; all remain ineligible for reviewer reservation.
Continue all safe reversible work, but never invent authority to deploy, merge,
release, move real money, execute a destructive migration, or perform another
protected external action. Leave such an action unexecuted and report
`blocked-external-boundary` only for that boundary.

## Post-phase retrospective

After every terminal result—valid reviewer `ship`, `parent-completed`,
`blocked`, or `blocked-external-boundary`—append a lightweight retrospective to
the durable ledger. This is process evidence, not another product review and
not permission to edit Solweaver, repository governance, or production state
automatically.

```text
ASSURANCE UNIT
- ASSURANCE_UNIT_ID: <stable id>
- REOPEN_GENERATION: <integer>
- TERMINAL_RESULT: ship | parent-completed/final-strict-not-achieved | blocked | blocked-external-boundary

EFFICIENCY
- CANDIDATE_ATTEMPTS: <count of frozen candidates presented to final readiness>
- EXACT_EVIDENCE_RERUNS: <count and expensive lanes>
- REVIEW_CALLS_RESERVED: <count>
- REVIEW_CALLS_USED: <0 | 1 | 2 | 3>
- CANCELLED_BEFORE_START: <count with exact proof>
- ELAPSED_CONTEXT: <timestamps or not-measured; never invent>

FINDING CLASSIFICATION
| Finding or waste | Class | Origin | Preventable before review? | Preventive gate or change |
| --- | --- | --- | --- | --- |
| <item> | requirement-ambiguity | acceptance-mismatch | yes/no | <action> |
| <item> | implementation-defect | pre-existing or introduced-by-fix | yes/no | <action> |
| <item> | evidence-or-harness-defect | newly-exposed-evidence | yes/no | <action> |
| <item> | runtime-migration-or-delivery-gap | pre-existing or introduced-by-fix | yes/no | <action> |
| <item> | workflow-or-review-budget-defect | acceptance-mismatch | yes/no | <action> |

IMPROVEMENT PROPOSALS
1. <generalizable proposal, or none>
2. <generalizable proposal, or omit>
3. <generalizable proposal, or omit>
WORKFLOW_CHANGE_STATUS: proposed-for-user-approval | applied-with-explicit-user-approval | no-generalizable-change
```

Keep at most three proposals and separate phase-specific defects from reusable
workflow improvements. Apply a workflow change only after explicit user
approval. After changing Solweaver definitions, validate the source and
installed copy, then require a restarted or new-task runtime smoke before
claiming runtime certification.

## Runtime evidence language

- Say **observed `<role/model/effort>`** only when the child session
  `turn_context` exposes it.
- Say **configured `<role/model/effort>`** when a validated agent TOML pins it
  but runtime metadata is unavailable.
- Say **unverified** when neither source establishes it.
- A UI label, task title, prompt, or agent self-report is never model telemetry.

## Runtime identity gates

Apply these expected pairs only to agents defined by the Solweaver package:

| Agent | Required `turn_context.model` | Required `turn_context.effort` |
| --- | --- | --- |
| `terra_worker` | `gpt-5.6-terra` | `max` |
| `luna_worker` | `gpt-5.6-luna` | `max` |
| `solweaver_reviewer` | `gpt-5.6-sol` | `max` |

After every package-owned child turn, inspect both fields before accepting its
report or verdict. Missing metadata fails the gate instead of falling back to
the agent definition. A model-generated self-report is not runtime proof. This
runtime gate intentionally checks only model and effort; do not infer sandbox
enforcement from it.

When a worker gate fails:

1. Mark the lane mismatched or unverified and do not count it as correctly
   routed or accept its report as evidence.
2. Preserve the shared worktree. Do not revert or delete child edits
   automatically.
3. Let Sol inspect the complete diff and verify any salvageable changes before
   taking ownership of them.
4. In auto mode, Sol may continue locally while reporting the failed lane. In
   explicit team mode, pause and make at most one corrected re-dispatch when
   the expected runtime is available; otherwise request user direction.

When the reviewer gate fails, reject the verdict and do not claim final-strict
acceptance. The attempt still consumes one review call when the child began
execution. Spawn a later fresh reviewer only when predeclared budget remains
and after completing the universal re-review closure matrix, refreezing the
candidate, rerunning parent adversarial readiness and the full readiness gate,
confirming the expected runtime is available, confirming capacity, and
verifying the next call has not already been consumed.

Do not hard-code an expected model for optional platform specialists such as
`code_mapper`, `tester`, `reviewer`, or `security_reviewer`; Solweaver does not
own those definitions. Report their runtime evidence honestly and enforce an
exact pair only when the user explicitly requires one.

## Final-strict protected boundaries

Final-strict defers only the independent reviewer, never parent verification.
Do not cross any of these boundaries before the fresh final-strict gate accepts
the relevant cumulative change:

- executing a destructive or irreversible migration;
- moving real money or changing production financial state;
- changing production authentication or authorization behavior;
- deploying, merging, releasing, or performing another irreversible external
  mutation.

If a protected boundary arrives before the declared assurance-unit end, move
the final gate forward for the accumulated relevant change or stop. The user
may define a later material delivery unit after that gate; do not silently
continue under a stale ledger or reset the closed unit's review budget.
