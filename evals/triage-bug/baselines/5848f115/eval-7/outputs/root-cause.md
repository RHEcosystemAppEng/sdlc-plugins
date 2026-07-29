# Step 4 -- Root Cause Analysis: ACME-520

## Root Cause

The `compute_risk_score()` function in `modules/risk/src/score.rs` has its division
operands reversed. It computes `total_deps / vulnerable_deps` instead of
`vulnerable_deps / total_deps`. This produces inflated risk scores for all
assessments where `total_deps > vulnerable_deps` (the common case).

The bug is a simple logic error: the numerator and denominator are swapped in the
division expression.

## Affected Files

| File | Symbol | Defect |
|------|--------|--------|
| `modules/risk/src/score.rs` | `compute_risk_score()` | Division operands swapped: `total_deps / vulnerable_deps` instead of `vulnerable_deps / total_deps` |
| `modules/risk/src/assessment.rs` | `create_assessment()` | Not itself buggy, but persists the incorrect score to `assessments.risk_score` at ingestion time |

## Persistence Impact

The incorrect risk score is persisted to the `assessments` table (`risk_score`
column) at ingestion time via `diesel::insert_into(assessments::table)` in
`create_assessment()`. The `GET /api/v2/assessments/{id}` endpoint reads the
persisted value directly -- it does not recompute the score. Therefore:

- **Future assessments**: will be corrected by fixing `compute_risk_score()`
- **Existing assessments**: retain the inflated `risk_score` values and require
  a data migration to correct

## Suggested Approach

1. **Fix the division**: swap the operands in `compute_risk_score()` to
   `vulnerable_deps as f64 / total_deps as f64`.
2. **Data migration**: create a Diesel migration to correct existing `risk_score`
   values in the `assessments` table by recomputing from the linked SBOM data.
3. **Reproducer test**: add a test with `total_deps != vulnerable_deps` to catch
   the swapped operands.

## Reproducer Strategy

Write a test that calls `compute_risk_score()` with distinct values for `total_deps`
and `vulnerable_deps` (e.g., `total_deps = 100, vulnerable_deps = 5`).

- **Before fix**: `compute_risk_score(100, 5)` returns `20.0` (wrong)
- **After fix**: `compute_risk_score(100, 5)` returns `0.05` (correct)

The existing test `test_risk_score_all_vulnerable` uses equal values (10, 10) which
masks the bug. The reproducer must use unequal values to expose it.

## Affects Version Resolution (Step 4.5)

The **Environment / Version** section states "Not specified." No version information
can be extracted from the bug description. The Affects Version field on ACME-520
is not populated. A comment would be posted to the Bug:

> "Affects Version could not be determined from the bug description -- please set
> manually."
