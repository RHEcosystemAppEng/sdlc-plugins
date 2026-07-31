# Step 4 -- Root Cause Analysis: ACME-520

## Root Cause

**What is broken**: The `compute_risk_score()` function in `modules/risk/src/score.rs` divides `total_deps / vulnerable_deps` instead of `vulnerable_deps / total_deps`. The numerator and denominator are swapped, producing inflated risk scores. For example, an SBOM with 100 total dependencies and 5 vulnerable ones yields a risk score of 20.0 instead of 0.05.

**Why it is broken**: The division operands are reversed in the function body. The function signature correctly accepts `(total_deps, vulnerable_deps)` but the body computes `total_deps as f64 / vulnerable_deps as f64` instead of the intended `vulnerable_deps as f64 / total_deps as f64`.

**Where it is broken**:
- **Primary defect**: `modules/risk/src/score.rs` -- `compute_risk_score()` function
- **Persistence path**: `modules/risk/src/assessment.rs` -- `create_assessment()` persists the buggy value to `assessments.risk_score` via `diesel::insert_into`
- **Serving path**: `modules/risk/src/endpoints.rs` -- `get_assessment()` returns the persisted (incorrect) value without recomputation

**How to verify the fix**: A reproducer test should call `compute_risk_score(100, 5)` (where total != vulnerable) and assert the result is `0.05`, not `20.0`. This test will fail before the fix (confirming the bug) and pass after the fix (confirming the correction). Additionally, existing assessments in the database must be verified to have their `risk_score` values corrected by a data migration.

## Persistence Impact

The buggy output is persisted to the `assessments` table, `risk_score` column, at ingestion time. The value is written once during `create_assessment()` and is never recomputed on read. All existing assessments contain incorrect (inflated) risk scores. A data migration is required to recompute and correct the `risk_score` for all existing records.

## Decomposition Guard (Step 6)

This bug has a single root cause (swapped division operands in `compute_risk_score()`) that manifests in one code path. The persistence impact is a direct consequence of the same defect, not an independent issue. A single Task is appropriate -- no decomposition needed.

## Affects Version Resolution (Step 4.5)

The Environment / Version section states "Not specified." No version pattern can be extracted. A comment would be posted on the Bug:

> "Affects Version could not be determined from the bug description -- please set manually."
