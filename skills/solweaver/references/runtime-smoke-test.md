# Solweaver runtime smoke test

Run this test after restarting Codex or opening a new task following any change
to the skill, agents, configuration, or global routing. Use a throwaway
repository or safe documentation-only fixture. Do not use production data or
authorize external actions.

## Observe

1. Start Codex with `gpt-5.6-sol` and `Max` reasoning.
2. Confirm current session `turn_context` reports `model == "gpt-5.6-sol"` and
   `effort == "max"`. Configuration alone is not observed runtime evidence.
3. Invoke `$solweaver` in team mode with one bounded Terra assignment. Inspect
   the child `turn_context` and require `model == "gpt-5.6-terra"` and
   `effort == "max"` before counting the worker lane.
4. Repeat with one disjoint bounded Luna assignment. Require
   `model == "gpt-5.6-luna"` and `effort == "max"` before counting the lane.
5. Confirm Sol remains the parent orchestrator, inspects the complete diff, and
   verifies the integrated result. Confirm no worker orchestrates another
   agent.
6. Invoke strict mode after parent verification. Confirm a fresh
   `solweaver_reviewer` inspects the actual change and returns exactly `ship`,
   `fix-first`, or `rethink` without editing files.
7. Before accepting that verdict, inspect the reviewer `turn_context` and
   require `model == "gpt-5.6-sol"` and `effort == "max"`.
8. Confirm missing or mismatched worker metadata does not trigger an automatic
   rollback of shared-worktree changes, and missing or mismatched reviewer
   metadata does not count as strict-review evidence.
9. Confirm a model-generated self-report, task label, or UI name is not used as
   runtime proof. The runtime gate evaluates only model and effort.
10. Exercise the `fix-first` path only with a controlled fixture. Confirm Sol
    closes each reviewer, records the closure matrix, uses a fresh reviewer for
    each round, and pauses for design/acceptance reconciliation after two
    consecutive `fix-first` verdicts instead of starting a third review
    automatically.

## Record

Record the parent model and effort, each child `turn_context.model` and
`turn_context.effort`, agent names, call order, execution and assurance modes,
worker status, reviewer verdict, changed fixture files, verification commands,
reviewer call counts, re-review rounds, reconciliation decisions, and any UI or
runtime limitations. Remove or discard only throwaway artifacts created by
this test.

Call Solweaver runtime-certified only when every applicable observation passes.
Otherwise report the exact gap as configured, unverified, mismatched, or
failed. A focused routing smoke is not full implementation end-to-end proof.
