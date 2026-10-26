# Root Cause Analysis — ACME-520

## Root Cause

The `compute_risk_score()` function in `modules/risk/src/score.rs` has its division
operands reversed. It computes `total_deps / vulnerable_deps` instead of
`vulnerable_deps / total_deps`. This produces inflated risk scores for all
assessments where total dependencies differ from vulnerable dependencies.

For example, with 100 total dependencies and 5 vulnerable:
- **Expected**: 5 / 100 = 0.05
- **Actual**: 100 / 5 = 20.0

## What is Broken

The division expression in `compute_risk_score()` has swapped numerator and
denominator: `total_deps as f64 / vulnerable_deps as f64` instead of
`vulnerable_deps as f64 / total_deps as f64`.

## Why it is Broken

The operands of the division were written in the wrong order. The existing test
(`test_risk_score_all_vulnerable`) uses symmetric inputs (10, 10) where the
bug is invisible because `10/10 = 1.0` regardless of order, so the defect was
never caught by tests.

## Where it is Broken

- **Primary defect**: `modules/risk/src/score.rs` — `compute_risk_score()` function
- **Persistence caller**: `modules/risk/src/assessment.rs` — `create_assessment()`
  persists the incorrect value via `diesel::insert_into(assessments::table)`
- **Read endpoint**: `modules/risk/src/endpoints.rs` — `get_assessment()` reads the
  persisted (incorrect) value directly without recomputation

## Persistence Impact

The incorrect risk_score is written to the `assessments` table, `risk_score` column,
at ingestion time (assessment creation). It is NOT recomputed on read. All existing
assessments contain inflated risk_score values. Fixing the code alone only corrects
future assessments — a data migration is required to recompute and update existing
risk_score values.

## How to Verify the Fix

A reproducer test should call `compute_risk_score()` with asymmetric inputs where
`total_deps != vulnerable_deps` (e.g., `total_deps=100, vulnerable_deps=5`) and
assert the result equals `0.05` (vulnerable / total), not `20.0` (total / vulnerable).

### Reproducer Strategy

1. Add a test in `modules/risk/tests/score_test.rs` that calls
   `compute_risk_score(100, 5)`.
2. Assert the result equals `0.05` (5 / 100).
3. This test should fail before the fix (returning 20.0) and pass after.

## Suggested Approach

1. Fix the division in `compute_risk_score()`: change `total_deps as f64 / vulnerable_deps as f64`
   to `vulnerable_deps as f64 / total_deps as f64`.
2. Add a data migration to recompute and update all existing `risk_score` values in
   the `assessments` table using source data from the `sboms` table.
3. Add the reproducer test with asymmetric inputs.

## Affected Files

- `modules/risk/src/score.rs` — `compute_risk_score()` (fix division)
- `modules/risk/tests/score_test.rs` — add reproducer test
- `modules/risk/src/assessment.rs` — no code change needed, but relevant for understanding the persistence chain
- `migration/` — new migration directory for data correction
