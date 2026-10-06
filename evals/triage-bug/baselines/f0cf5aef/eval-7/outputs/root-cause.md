# Step 4 -- Root Cause Analysis: ACME-520

## Root Cause

The `compute_risk_score()` function in `modules/risk/src/score.rs` has its division operands reversed. It computes `total_deps / vulnerable_deps` instead of `vulnerable_deps / total_deps`, producing inflated risk scores. For example, an SBOM with 100 total dependencies and 5 vulnerable ones yields a score of 20.0 instead of the correct 0.05.

## Affected Files

- **`modules/risk/src/score.rs`** -- `compute_risk_score()`: the division operands (`total_deps as f64 / vulnerable_deps as f64`) are swapped. Should be `vulnerable_deps as f64 / total_deps as f64`.
- **`modules/risk/src/assessment.rs`** -- `create_assessment()`: persists the incorrect score to the `assessments` table at ingestion time. The score is never recomputed on read.
- **`modules/risk/tests/score_test.rs`** -- existing test only checks the `total == vulnerable` case (10/10 = 1.0), which passes regardless of operand order. No test covers the asymmetric case.

## Suggested Approach

1. **Fix the formula**: In `compute_risk_score()`, swap the operands so the function computes `vulnerable_deps as f64 / total_deps as f64`.
2. **Add a data migration**: Create a new Diesel migration to recompute and update the `risk_score` column for all existing rows in the `assessments` table, using the correct formula based on each row's associated SBOM data.
3. **Add a reproducer test**: Write a test with asymmetric inputs (e.g., `total_deps=100, vulnerable_deps=5`) that asserts the correct result (`0.05`), ensuring the swapped-operand bug cannot regress.

## Reproducer Strategy

Write a unit test in `modules/risk/tests/score_test.rs` that calls `compute_risk_score(100, 5)` and asserts the result equals `0.05`. This test:
- **Before fix**: fails, because the function returns `20.0` (operands reversed).
- **After fix**: passes, confirming the correct computation `5 / 100 = 0.05`.

The asymmetric inputs are critical -- equal-value inputs (like the existing 10/10 test) cannot detect the operand swap.

## Affects Version Resolution (Step 4.5)

The **Environment / Version** section contains "Not specified." -- no version information can be extracted. The `affectsVersions` field is not populated on the bug.

**Gap flagged**: Affects Version could not be determined from the bug description. A comment would be posted on ACME-520:

> Affects Version could not be determined from the bug description -- please set manually.

## Decomposition Guard (Step 6)

This bug has a **single root cause** (reversed division operands in `compute_risk_score()`). Although the fix involves both a code change and a data migration, they address the same defect. No decomposition is needed -- a single Task is appropriate.
