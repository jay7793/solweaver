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
5. Invoke final-strict mode on a controlled batch with at least two
   intermediate checkpoints. Confirm Sol records the exact base and declared
   final boundary, verifies every checkpoint, updates the batch ledger, reports
   only `checkpoint-ready`, and does not spawn `solweaver_reviewer` yet.
6. At the final-strict boundary, confirm Sol inspects the complete cumulative
   diff from the recorded base, reconciles all checkpoints, reruns integration
   or acceptance evidence, and sends the whole batch to one fresh reviewer.
7. Confirm final-strict does not defer review across a protected irreversible
   or production boundary. The relevant accumulated change must pass the
   final-strict gate before that boundary is crossed.
8. Confirm Sol remains the parent orchestrator, inspects the complete diff, and
   verifies the integrated result. Confirm no worker orchestrates another
   agent.
9. At the final-strict gate, confirm a fresh `solweaver_reviewer` inspects the
   actual complete change and returns exactly `ship`, `fix-first`, or `rethink`
   without editing files.
10. Before accepting that verdict, inspect the reviewer `turn_context` and
   require `model == "gpt-5.6-sol"` and `effort == "max"`.
11. Confirm missing or mismatched worker metadata does not trigger an automatic
    rollback of shared-worktree changes, and missing or mismatched reviewer
    metadata does not count as final-strict-review evidence but does consume a
    review call after the reviewer begins execution.
12. Confirm a model-generated self-report, task label, or UI name is not used as
    runtime proof. The runtime gate evaluates only model and effort.
13. Exercise the two-call hard gate only with a controlled fixture. Confirm call
    1 returning `fix-first` produces a closure matrix and call 2 uses a fresh
    reviewer over the complete cumulative diff.
14. Make call 2 return a non-`ship` verdict or fail its runtime gate. Confirm Sol
    sets `REVIEW_STATUS: review-exhausted`, never spawns call 3, and enters
    parent-owned completion without requesting user direction. Confirm Sol
    reconciles findings, applies addressable fixes, verifies the complete diff,
    and reports `FINAL_STATUS: parent-completed` with
    `ASSURANCE_STATUS: final-strict-not-achieved` when acceptance criteria pass.
15. Confirm parent-owned completion leaves unauthorized deploy, merge, release,
    real-money, destructive-migration, and other protected external actions
    unexecuted while completing all safe reversible work.

## Record

Record the parent model and effort, each child `turn_context.model` and
`turn_context.effort`, agent names, call order, execution and assurance modes,
worker status, reviewer verdict, changed fixture files, verification commands,
final-strict base and boundary, checkpoint ledger, reviewer call counts,
`MAX_REVIEW_CALLS`, `REVIEW_CALLS_USED`, exhaustion status, re-review rounds,
parent recovery decisions, final and assurance status, protected actions left
unexecuted, and any UI or runtime limitations. Remove or discard only throwaway
artifacts created by this test.

Call Solweaver runtime-certified only when every applicable observation passes.
Otherwise report the exact gap as configured, unverified, mismatched, or
failed. A focused routing smoke is not full implementation end-to-end proof.
