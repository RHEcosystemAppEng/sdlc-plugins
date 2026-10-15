# Step 4 -- Root Cause Analysis: ACME-520

## Root Cause

The `compute_risk_score()` function in `modules/risk/src/score.rs` has its division
operands reversed. It computes `total_deps / vulnerable_deps` instead of
`vulnerable_deps / total_deps`, producing inflated risk scores that are the
reciprocal of the correct value.

For example, an SBOM with 100 total dependencies and 5 vulnerable ones produces a
risk score of `20.0` instead of `0.05`.

## Affected Files

| File | Symbol | Defect |
|------|--------|--------|
| `modules/risk/src/score.rs` | `compute_risk_score()` | Division operands are swapped: `total_deps as f64 / vulnerable_deps as f64` should be `vulnerable_deps as f64 / total_deps as f64` |
| `modules/risk/src/assessment.rs` | `create_assessment()` | Persistence boundary: writes the incorrect score to `assessments.risk_score` via `diesel::insert_into` at ingestion time |

## Suggested Approach

1. **Fix the division** in `compute_risk_score()`: swap the operands so the function
   returns `vulnerable_deps as f64 / total_deps as f64`.
2. **Add a data migration** to correct all existing `assessments.risk_score` values
   that were persisted with the wrong calculation. The migration should recompute
   the score from the source data in the `sboms` table (joined via `sbom_id`).
3. **Add a reproducer test** that exercises the function with unequal values
   (e.g., `total=100, vulnerable=5`) and asserts the expected result of `0.05`.

## Reproducer Strategy

Write a unit test in `modules/risk/tests/score_test.rs` that calls
`compute_risk_score(100, 5)` and asserts the result equals `0.05`. This test will:

- **Fail before the fix**: the function returns `20.0` (total / vulnerable)
- **Pass after the fix**: the function returns `0.05` (vulnerable / total)

The existing test `test_risk_score_all_vulnerable` with equal values (10, 10) is
not sufficient because `10/10 = 1.0` regardless of operand order. The reproducer
must use unequal values to expose the swap.

## Affects Version Resolution (Step 4.5)

The Environment / Version section contains "Not specified." No version information
can be extracted. The `affectsVersions` field is empty.

**Action**: Flag gap -- Affects Version could not be determined from the bug
description. A comment would be posted on ACME-520:

> Affects Version could not be determined from the bug description -- please set manually.

## Decomposition Guard (Step 6)

This bug has a single root cause (swapped operands in `compute_risk_score()`) that
manifests through a single code path. Although the fix involves both a code change
and a data migration, these are two aspects of the same defect -- not independent
issues. A single Task is appropriate. No decomposition needed.
