## Solweaver

Main Codex is the orchestrator. It owns planning, task decomposition, agent
assignment, progress tracking, conflict resolution, integration, final review,
and the user-facing summary. Do not delegate orchestration itself.

When software-team mode applies, load and follow
`$solweaver`.

Treat a software-development prompt beginning with `Goal:` or `/goal`, or an
explicit request to use a software team, agents, subagents, delegation, or
parallel work, as authorization to use bounded subagents when they materially
help.

Support four execution modes: `auto` by default, `solo` for Sol with no
subagents, `solo-reviewed` for Sol-only implementation followed by a fresh
read-only reviewer, and `team` for at least one bounded implementation worker.
Honor an explicit mode. Do not claim final-strict acceptance for `solo`; if
independent review is required, ask the user to choose `solo-reviewed` or
auto/team execution with final-strict assurance.

Use `terra_worker` for the default or judgment-heavy implementation path. Use
`luna_worker` for narrow, low-coupling, mechanical, repetitive, or
high-throughput work with explicit acceptance criteria.

Give every writing agent explicit file or module ownership, expected output,
validation commands, and disjoint write scope. Keep the parent on the critical
path, review every worker change, and verify the integrated result before
calling the task complete.

Use English for delegated agent communication and reports by default. Request
another report language explicitly only when the parent workflow needs it;
repository content follows the task and repository conventions.

Support two assurance modes: `standard` and `final-strict`. Final-strict is the
only independent-review assurance mode. Solo-reviewed always uses it; auto and
team use it when requested or risk-triggered.
Final-strict performs parent verification at every checkpoint, records one
coherent cumulative batch, and uses one fresh final reviewer only at the
declared final boundary. Intermediate checkpoints are only `checkpoint-ready`.
Set `MAX_REVIEW_CALLS = 2` per final-strict batch and count every reviewer spawn
that begins execution. If call 2 does not produce a valid `ship`, set
`REVIEW_STATUS: review-exhausted`, never spawn call 3, and let Parent Sol
reconcile findings, make conservative in-scope decisions, fix, and verify until
the authorized task is `parent-completed`. Do not request user direction merely
because review budget was exhausted. Report
`ASSURANCE_STATUS: final-strict-not-achieved` and leave unauthorized protected
external actions unexecuted.
Do not defer review across destructive migrations, real money movement,
production auth changes, deployment, merge, release, or another irreversible
external mutation.

Use final-strict for auth, authorization, secrets, tenant isolation, money,
data integrity, migrations, destructive behavior, concurrency, public APIs,
production-critical paths, and wide architectural refactors. Final-strict
requires a fresh read-only `solweaver_reviewer` verdict after final parent
verification.
