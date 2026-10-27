# Root Cause Analysis -- Step 4

## Root Cause

The `compute_risk_score()` function in `modules/risk/src/score.rs` has its division
operands swapped. It computes `total_deps / vulnerable_deps` instead of the correct
`vulnerable_deps / total_deps`.

This produces inflated risk scores for all assessments. For example, an SBOM with
100 total dependencies and 5 vulnerable dependencies yields a risk score of 20.0
instead of 0.05.

## What is broken

The division expression in `compute_risk_score()`:

```rust
total_deps as f64 / vulnerable_deps as f64
```

The numerator and denominator are reversed. The correct expression is:

```rust
vulnerable_deps as f64 / total_deps as f64
```

## Why it is broken

The operands were written in the wrong order. The function divides the total
dependency count by the vulnerable dependency count, when the risk score should
represent the fraction of dependencies that are vulnerable (vulnerable / total).

## Where it is broken

- **Primary defect**: `modules/risk/src/score.rs` -- function `compute_risk_score()`
- **Persistence path**: `modules/risk/src/assessment.rs` -- function `create_assessment()`
  persists the incorrect score to the `assessments` table, `risk_score` column
- **Read path**: `modules/risk/src/endpoints.rs` -- function `get_assessment()` serves
  the incorrect persisted value without recomputation

## How to verify the fix (Reproducer Strategy)

1. Write a test in `modules/risk/tests/score_test.rs` that calls
   `compute_risk_score(total_deps, vulnerable_deps)` with values where
   `total_deps != vulnerable_deps` (e.g., `total_deps = 100, vulnerable_deps = 5`).
2. Assert that the result equals `vulnerable_deps / total_deps` (e.g., `0.05`),
   NOT `total_deps / vulnerable_deps` (e.g., `20.0`).
3. This test should fail before the fix (demonstrating the bug) and pass after the
   fix (confirming the correction).
4. The existing test `test_risk_score_all_vulnerable` uses equal values (10, 10)
   and passes regardless of operand order -- it does not catch this bug.

## Affected Files

- `modules/risk/src/score.rs` -- `compute_risk_score()`
- `modules/risk/src/assessment.rs` -- `create_assessment()`
- `modules/risk/src/endpoints.rs` -- `get_assessment()`
- `modules/risk/tests/score_test.rs` -- existing test file (inadequate coverage)

## Suggested Approach

1. Fix the division operand order in `compute_risk_score()`.
2. Add a reproducer test with asymmetric inputs to catch the regression.
3. Create a data migration to recompute and update existing `risk_score` values in
   the `assessments` table using the corrected formula.
