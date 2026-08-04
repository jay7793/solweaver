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

Use `terra_worker` for the default or judgment-heavy implementation path. Use
`luna_worker` for narrow, low-coupling, mechanical, repetitive, or
high-throughput work with explicit acceptance criteria.

Give every writing agent explicit file or module ownership, expected output,
validation commands, and disjoint write scope. Keep the parent on the critical
path, review every worker change, and verify the integrated result before
calling the task complete.

Use Solweaver strict mode for auth, authorization, secrets, tenant isolation,
money, data integrity, migrations, destructive behavior, concurrency, public
APIs, production-critical paths, and wide architectural refactors. Strict mode
requires a fresh read-only `solweaver_reviewer` verdict after parent
verification.
