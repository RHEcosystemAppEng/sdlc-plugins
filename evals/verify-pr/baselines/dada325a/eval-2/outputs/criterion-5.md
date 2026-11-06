# Criterion 5 — FAIL

**Criterion:** Response includes a `threshold_applied` boolean field indicating whether filtering is active

## What was checked

- The `AdvisorySummary` values built in the diff.
- Whether the PR changes the model file (`modules/fundamental/src/advisory/model/summary.rs`).

## Findings

- The `AdvisorySummary` literal in the handler sets only `critical`, `high`, `medium`, `low` and `total`. There is no `threshold_applied` field.
- The PR does not change `advisory/model/summary.rs`, and the diff does not add the field to the struct anywhere else.
- Neither the `None` arm nor the `Some` arm sets any flag showing whether filtering happened.
- The string `threshold_applied` does not appear anywhere in the diff.

## Verdict

FAIL. The `threshold_applied` field was not implemented.
