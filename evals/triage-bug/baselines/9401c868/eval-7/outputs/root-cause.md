# Step 4 -- Root Cause Analysis: ACME-520

## Root Cause

The `compute_risk_score()` function in `modules/risk/src/score.rs` computes the risk score with **swapped operands** in the division. It calculates `total_deps / vulnerable_deps` instead of `vulnerable_deps / total_deps`. This produces inflated risk scores for all assessments where the number of vulnerable dependencies differs from the total.

For example, with 100 total dependencies and 5 vulnerable, the function returns `100 / 5 = 20.0` instead of the correct `5 / 100 = 0.05`.

## Why it is broken

The numerator and denominator in the division expression are reversed. The function body is:

```rust
total_deps as f64 / vulnerable_deps as f64
```

It should be:

```rust
vulnerable_deps as f64 / total_deps as f64
```

## Affected Files

| File | Symbol | Defect |
|------|--------|--------|
| `modules/risk/src/score.rs` | `compute_risk_score()` | Division operands swapped |
| `modules/risk/src/assessment.rs` | `create_assessment()` | Persists the incorrect score to the `assessments` table at ingestion time |

## Persistence Impact

The incorrect risk score is written to the `assessments.risk_score` column at ingestion time by `create_assessment()`. The GET endpoint (`get_assessment()` in `modules/risk/src/endpoints.rs`) reads the persisted value directly without recomputing. Therefore:

- Fixing the code alone corrects only **future** assessments.
- **Existing** assessment records retain the inflated score.
- A **data migration** is required to correct existing records (the corrected value is the reciprocal: `1.0 / risk_score` for non-zero scores).

## Suggested Approach

1. Fix the division order in `compute_risk_score()` to `vulnerable_deps / total_deps`.
2. Add a data migration to correct existing `risk_score` values in the `assessments` table.
3. Add proper test coverage: a reproducer test with `total_deps != vulnerable_deps` to prevent regression.

## Reproducer Strategy

Write a test that calls `compute_risk_score(100, 5)` and asserts the result is `0.05`. This test:
- **Before fix**: fails with actual value `20.0` (proving the bug exists)
- **After fix**: passes with correct value `0.05` (proving the bug is fixed)

The existing test `test_risk_score_all_vulnerable` in `modules/risk/tests/score_test.rs` uses equal values (`10, 10`) and passes regardless of operand order, so it does not detect this bug.

## Affects Version Resolution (Step 4.5)

The **Environment / Version** section states "Not specified." No version pattern can be extracted. A comment would be posted on ACME-520:

> Affects Version could not be determined from the bug description -- please set manually.

## Comment that would be posted to ACME-520

The root cause analysis above would be posted as an ADF-formatted comment on ACME-520, with the following sections: Root Cause, Affected Files, Suggested Approach, and Reproducer Strategy. The Comment Footnote (with sdlc-workflow/triage-bug version and link) would be appended.
