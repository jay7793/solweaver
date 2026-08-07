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

## Strict review packet

Send this only after the parent has inspected the diff and rerun verification.
The reviewer must remain behaviorally read-only even if the host grants broader
filesystem permissions.

```text
ROLE
Act as a fresh read-only reviewer. Do not edit files, implement fixes, commit,
push, or orchestrate other agents.

EXECUTION MODE
<auto | solo-reviewed | team>

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

After a `fix-first` verdict, close that reviewer. The responsible worker, or
Sol in solo-reviewed execution, implements the bounded changes. Sol then
inspects the full diff, verifies the result, and completes this matrix before
spawning a fresh reviewer:

| Prior finding | Exact changed files | Intended behavior | Direct tests | Evidence class | Known limitations |
| --- | --- | --- | --- | --- | --- |
| <finding identity> | <paths> | <observable change> | <commands/tests and results> | <one class> | <remaining gap or none> |

Send the neutral matrix with the next strict review packet as accountability
evidence. Do not send the prior reviewer conversation, disposition, or an
expected verdict. The fresh reviewer must inspect the complete diff
independently and may reject a claimed closure or identify new problems.

## Design/acceptance reconciliation

After two consecutive `fix-first` verdicts, pause before spawning a third
reviewer. Reconcile every remaining issue as one of:

1. implementation defect;
2. evidence defect;
3. unresolved product or architecture decision; or
4. mismatch between stated acceptance criteria and reviewer expectations.

Record the classification, supporting facts, exact missing proof or decision,
and proposed next action. When the issue is consequential or ambiguous, state
the guarantee precisely, present viable choices with guarantees and
limitations, and request user direction. Do not silently weaken semantics,
force a workflow switch, lower the review bar, or treat review count as
permission to ship. A later strict acceptance still requires `ship` from a
fresh runtime-verified reviewer.

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

When the reviewer gate fails, reject the verdict and do not claim strict
acceptance. Spawn a fresh reviewer only after the expected runtime is available
and capacity permits it.

Do not hard-code an expected model for optional platform specialists such as
`code_mapper`, `tester`, `reviewer`, or `security_reviewer`; Solweaver does not
own those definitions. Report their runtime evidence honestly and enforce an
exact pair only when the user explicitly requires one.
