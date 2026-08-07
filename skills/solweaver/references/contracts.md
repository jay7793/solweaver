# Solweaver contracts

Use these packets to keep delegated work bounded and reviewable. Replace every
placeholder; do not assume a fresh agent inherited parent context.

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

## Final-strict batch ledger

Create this ledger before the first final-strict implementation checkpoint.
Keep it in the parent task context unless the user authorizes a repository
artifact. If the work spans tasks, reconstruct every field from exact Git and
verification evidence before claiming continuity.

```text
BASE STATE
- Ref or observed state: <exact SHA, branch/worktree, and initial dirty files>

BATCH
- Objective: <one coherent phase or delivery unit>
- Acceptance criteria: <complete cumulative criteria>
- Declared final boundary: <observable condition that triggers final-strict review>
- Protected boundaries: <migration execution, money movement, production auth,
  deploy, merge, release, or other irreversible actions that cannot be crossed>
- MAX_REVIEW_CALLS: 2
- REVIEW_CALLS_USED: <0 | 1 | 2>

CHECKPOINTS
| Checkpoint | Changed scope | Parent verification | Decisions | Known gaps | Status |
| --- | --- | --- | --- | --- | --- |
| <id> | <files/modules> | <commands and results> | <material choices> | <gaps or none> | checkpoint-ready |

FINAL GATE
- Complete cumulative diff from base: <command and observed scope>
- Integration/acceptance evidence: <commands and concrete results>
- Remaining gaps: <not-run or unproved behavior>
- Ready for one fresh final-strict reviewer: <yes or blocker>

REVIEW ATTEMPTS
| Call | Runtime gate | Verdict | Outcome |
| --- | --- | --- | --- |
| <1 or 2> | <pass, mismatch, or unverified> | <ship, fix-first, rethink, or unusable> | <accepted, revise, or review-exhausted> |
```

`checkpoint-ready` means parent-verified progress only. It is not `ship`, an
independent review, permission to cross a protected boundary, or evidence that
the final cumulative diff is reviewable. If the batch becomes too broad or
incoherent for one complete review, pause and ask the user to split it rather
than omitting scope from the final packet.

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

REVIEW BUDGET
- MAX_REVIEW_CALLS: 2
- REVIEW_CALLS_USED: <1 or 2, including this call>
- THIS_CALL: <1 or 2>

OBJECTIVE
<Original objective and acceptance criteria.>

CHANGE SCOPE
- Base or starting state: <exact ref or observed state>
- Intended files or modules: <scope>
- Actual changed files: <paths from parent inspection>

RISK
- Assurance reason: <auth, money, migration, public API, production, etc.>
- Invariants: <behavior or data that must not regress>

EVIDENCE
- Diff inspected by parent: <yes and summary>
- Commands rerun by parent: <commands and concrete results>
- Known gaps: <not-run or unproved evidence>

FINAL-STRICT BATCH
- Base state: <exact ref>
- Declared final boundary: <boundary>
- Complete cumulative diff: <command and observed scope>
- Checkpoint ledger reconciled: <yes with summary>

REPORT LANGUAGE
English by default. Use <another language> only when the parent explicitly
requests it. Preserve quoted repository content when fidelity matters.

REVIEW
Inspect the actual files and complete diff. Prioritize correctness, regressions,
security, data integrity, concurrency, public contracts, and missing tests.
Return exactly one verdict:
- ship: no blocking finding remains.
- fix-first: the design is viable but blocking fixes are required.
- rethink: architecture or scope must change before implementation continues.

RETURN
VERDICT: ship | fix-first | rethink
FINDINGS: <ordered blocking findings with file references, or none>
EVIDENCE: <what supports the verdict>
RESIDUAL RISK: <remaining uncertainty, or none>
```

## `fix-first` closure matrix

After a call 1 `fix-first` verdict, close that reviewer. The responsible worker,
or Sol in solo-reviewed execution, implements the bounded changes. Sol then
inspects the full diff, verifies the result, and completes this matrix before
using the second and final review call. A call 2 `fix-first` goes directly to
review-budget exhaustion; never spawn another reviewer.

| Prior finding | Exact changed files | Intended behavior | Direct tests | Evidence class | Known limitations |
| --- | --- | --- | --- | --- | --- |
| <finding identity> | <paths> | <observable change> | <commands/tests and results> | <one class> | <remaining gap or none> |

Send the neutral matrix with the second and final review packet as
accountability evidence. Do not send the prior reviewer conversation,
disposition, or an expected verdict. The fresh reviewer must inspect the
complete diff independently and may reject a claimed closure or identify new
problems.

## Review-budget exhaustion and parent completion

When review call 2 does not produce a valid `ship`, set
`REVIEW_STATUS: review-exhausted`. Never spawn call 3 for the same batch. Sol
owns the recovery and completes the authorized task without asking the user
merely to resolve the review loop. Reconcile every remaining issue as one of:

1. implementation defect;
2. evidence defect;
3. unresolved product or architecture decision; or
4. mismatch between stated acceptance criteria and reviewer expectations.

Record the classification, supporting facts, exact missing proof or decision,
and next action. Resolve decisions using this order: the original user goal and
acceptance criteria, repository instructions and contracts, compatibility with
existing behavior, then the narrowest reversible conservative implementation.
Implement every addressable fix, inspect the complete diff, and rerun
proportionate verification. Do not silently weaken semantics, expand authority,
force a workflow switch, lower the review bar, or treat review count as
permission to claim final-strict acceptance.

```text
MAX_REVIEW_CALLS: 2
REVIEW_CALLS_USED: 2
REVIEW_STATUS: review-exhausted
NEXT_REVIEW_ALLOWED: no
PARENT_RECOVERY: reconcile-fix-verify
FINAL_STATUS: parent-completed | blocked-external-boundary
ASSURANCE_STATUS: final-strict-not-achieved
USER_DECISION_REQUIRED: no
```

Use `parent-completed` when the authorized acceptance criteria are met after
parent recovery. This is an explicit assurance result, not a silent downgrade
or reviewer `ship`. Do not reset the counter or rename the same unchanged batch
to evade the cap. Continue all safe reversible work, but never invent authority
to deploy, merge, release, move real money, execute a destructive migration, or
perform another protected external action. Leave such an action unexecuted and
report `blocked-external-boundary` only for that boundary.

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
execution. Spawn a fresh reviewer only when the expected runtime is available,
capacity permits it, and call 2 has not already been consumed.

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

If a protected boundary arrives before the declared batch end, move the final
gate forward for the accumulated relevant change or stop. The user may redefine
the remaining batch after that gate; do not silently continue under a stale
ledger.
