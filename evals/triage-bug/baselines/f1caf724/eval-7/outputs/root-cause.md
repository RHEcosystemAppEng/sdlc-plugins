# Root Cause Analysis — ACME-520

## What is broken

The `compute_risk_score()` function in `modules/risk/src/score.rs` divides `total_deps` by `vulnerable_deps` instead of `vulnerable_deps` by `total_deps`. This produces inflated risk scores (e.g., 20.0 instead of 0.05 for an SBOM with 100 total and 5 vulnerable dependencies).

## Why it is broken

The numerator and denominator in the division are swapped. The function performs:

```rust
total_deps as f64 / vulnerable_deps as f64   // WRONG: 100 / 5 = 20.0
```

when it should perform:

```rust
vulnerable_deps as f64 / total_deps as f64   // CORRECT: 5 / 100 = 0.05
```

The existing test (`test_risk_score_all_vulnerable`) did not catch this because it uses equal values for both arguments (10, 10), making the division commutative in that case.

## Where it is broken

- **Primary defect**: `modules/risk/src/score.rs` — `compute_risk_score()` function, the division expression
- **Persistence propagation**: `modules/risk/src/assessment.rs` — `create_assessment()` persists the incorrect score to the `assessments` table, `risk_score` column, at ingestion time
- **Read path (unaffected code, but surfaces the bug)**: `modules/risk/src/endpoints.rs` — `get_assessment()` returns the persisted (incorrect) score without recomputation

## How to verify the fix (reproducer strategy)

A reproducer test should:

1. Call `compute_risk_score(100, 5)` — inputs where total != vulnerable, exposing the operand swap
2. Assert the result equals `0.05` (5 / 100), NOT `20.0` (100 / 5)
3. This test will FAIL before the fix (returns 20.0) and PASS after the fix (returns 0.05)

Additional verification:
- Ensure existing test `test_risk_score_all_vulnerable` still passes (no regression)
- Verify the data migration correctly recomputes `risk_score` for all existing records in the `assessments` table

## Suggested Approach

1. Fix the division in `compute_risk_score()` to use `vulnerable_deps as f64 / total_deps as f64`
2. Add a data migration to recompute `risk_score` for all existing rows in the `assessments` table using the corrected formula
3. Add edge-case handling for `total_deps == 0` (division by zero guard)

## Jira Comment (would be posted to ACME-520)

**Root Cause**: The `compute_risk_score()` function in `modules/risk/src/score.rs` has its division operands swapped — it divides `total_deps / vulnerable_deps` instead of `vulnerable_deps / total_deps`, producing inflated risk scores.

**Affected Files**:
- `modules/risk/src/score.rs` — `compute_risk_score()` (primary defect)
- `modules/risk/src/assessment.rs` — `create_assessment()` (persists the incorrect score)

**Suggested Approach**: Swap the division operands in `compute_risk_score()` and add a data migration to correct all existing `assessments.risk_score` values.

**Reproducer Strategy**: Call `compute_risk_score(100, 5)` and assert the result is `0.05`. This test fails before the fix (returns 20.0) and passes after.
