# Solweaver contracts

Use these packets to keep delegated work bounded and reviewable. Replace every
placeholder; do not assume a fresh agent inherited parent context.

## Worker task packet

```text
ROLE
Act as the assigned implementation worker. You are not alone in the codebase.
Preserve unrelated edits and own only the scope below.

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

## Runtime evidence language

- Say **observed `<role/model/effort>`** only when current runtime or spawn
  metadata exposes it.
- Say **configured `<role/model/effort>`** when a validated agent TOML pins it
  but runtime metadata is unavailable.
- Say **unverified** when neither source establishes it.
- A UI label, task title, prompt, or agent self-report is never model telemetry.
