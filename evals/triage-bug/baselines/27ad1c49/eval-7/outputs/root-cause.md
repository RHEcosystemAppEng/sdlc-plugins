# Step 4 -- Root Cause Analysis

## Root Cause

The `compute_risk_score()` function in `modules/risk/src/score.rs` has its division
operands reversed. It computes `total_deps / vulnerable_deps` instead of
`vulnerable_deps / total_deps`.

This produces the mathematical reciprocal of the intended risk score. For example,
with 100 total dependencies and 5 vulnerable ones, the function returns `20.0`
instead of `0.05`. The bug produces inflated scores that grow larger as the
actual risk decreases, completely inverting the intended semantics.

## What is broken

The division expression in `compute_risk_score()`:
```rust
total_deps as f64 / vulnerable_deps as f64
```
Should be:
```rust
vulnerable_deps as f64 / total_deps as f64
```

## Why it is broken

The numerator and denominator were swapped when the function was originally
written. The existing test (`test_risk_score_all_vulnerable`) uses equal values
for both parameters (`10, 10`), so it passes regardless of operand order and
did not catch the defect.

## Where it is broken

- **Primary defect**: `modules/risk/src/score.rs` -- `compute_risk_score()` function
- **Persistence caller**: `modules/risk/src/assessment.rs` -- `create_assessment()` function persists the incorrect value to the `assessments` table, `risk_score` column
- **Read path**: `modules/risk/src/endpoints.rs` -- `get_assessment()` returns the persisted incorrect value without recomputation

## Persistence impact

The incorrect risk score is persisted to the `assessments` table at ingestion time
and is never recomputed on read. All existing assessments contain incorrect
`risk_score` values. A data migration is required to correct historical data
alongside the code fix.

## How to verify the fix (reproducer strategy)

A reproducer test should:

1. Call `compute_risk_score()` with asymmetric values where `total_deps != vulnerable_deps` (e.g., `total_deps = 100`, `vulnerable_deps = 5`)
2. Assert that the result equals `0.05` (vulnerable / total), NOT `20.0` (total / vulnerable)
3. This test will fail before the fix (returns `20.0`) and pass after the fix (returns `0.05`)

Additional verification:
- Existing test `test_risk_score_all_vulnerable` should continue to pass (no regression)
- An integration-level test could verify that `create_assessment()` persists the correct score
