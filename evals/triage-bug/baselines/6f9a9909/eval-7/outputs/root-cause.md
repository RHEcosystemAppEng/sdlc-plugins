# Root Cause Analysis: ACME-520

## Root Cause

The `compute_risk_score()` function in `modules/risk/src/score.rs` has its numerator and denominator swapped. It computes `total_deps / vulnerable_deps` instead of the correct `vulnerable_deps / total_deps`.

This produces inflated risk scores for any assessment where `total_deps > vulnerable_deps`. For example, an SBOM with 100 total dependencies and 5 vulnerable ones produces a score of 20.0 instead of the expected 0.05.

## Persistence Impact

The bug is compounded by the persistence architecture:

1. `create_assessment()` in `modules/risk/src/assessment.rs` calls `compute_risk_score()` and writes the result to the `assessments` table via `diesel::insert_into(assessments::table)` into the `risk_score` column.
2. `get_assessment()` in `modules/risk/src/endpoints.rs` reads the persisted `risk_score` directly from the database -- it does NOT recompute the score.
3. Therefore, **all existing assessments** in the database have incorrect `risk_score` values permanently stored.

Fixing the code alone is insufficient. A data migration is required to recompute and correct the `risk_score` values for all existing rows in the `assessments` table.

## Why Existing Tests Did Not Catch This

The sole existing test (`test_risk_score_all_vulnerable`) calls `compute_risk_score(10, 10)`, which produces `1.0` regardless of operand order. No test case exercises inputs where `total_deps != vulnerable_deps`, so the swapped operands were never detected.

## Fix Requirements

1. **Code fix**: Swap the operands in `compute_risk_score()` so it returns `vulnerable_deps as f64 / total_deps as f64`.
2. **Data migration**: Create a migration (`migration/YYYY-MM-DD-NNNNNN_fix_risk_score_values/up.sql`) to update all existing rows: `UPDATE assessments SET risk_score = vulnerable_deps / total_deps` (correcting the persisted values by joining against the sboms table or using the stored dependency counts).
3. **Reproducer test**: Add a test with `total_deps != vulnerable_deps` (e.g., `compute_risk_score(100, 5)`) that asserts the correct result `0.05`.
