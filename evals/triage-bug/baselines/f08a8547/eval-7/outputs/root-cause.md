# Step 4 -- Root Cause Analysis

## Root Cause

The `compute_risk_score()` function in `modules/risk/src/score.rs` divides `total_deps`
by `vulnerable_deps` instead of dividing `vulnerable_deps` by `total_deps`. The
numerator and denominator are swapped:

```rust
// Current (buggy):
total_deps as f64 / vulnerable_deps as f64

// Correct:
vulnerable_deps as f64 / total_deps as f64
```

This produces risk scores that are the reciprocal of the correct value. For an SBOM
with 100 total dependencies and 5 vulnerable, the score is computed as `100 / 5 = 20.0`
instead of the correct `5 / 100 = 0.05`. The bug produces inflated scores for all
assessments where `total_deps != vulnerable_deps`.

## Affected Files

| File                                  | Symbol                  | Defect                                    |
|---------------------------------------|-------------------------|-------------------------------------------|
| `modules/risk/src/score.rs`           | `compute_risk_score()`  | Swapped division operands (primary defect) |
| `modules/risk/src/assessment.rs`      | `create_assessment()`   | Persists incorrect score to `assessments.risk_score` |

## Suggested Approach

1. **Fix the division** in `compute_risk_score()`: swap the operands so the function
   returns `vulnerable_deps as f64 / total_deps as f64`.
2. **Add a data migration** to correct existing `assessments.risk_score` values. Since
   the current stored value equals `total / vulnerable` (the reciprocal), the migration
   can recompute correct scores by joining against the SBOM source data to obtain the
   original `total_deps` and `vulnerable_deps`, then applying the corrected formula.
   Alternatively, if the source dependency counts are not directly available in the
   assessments table, the migration could invert the stored value (`1.0 / risk_score`)
   as an approximation, but joining against source data is preferred for accuracy.
3. **Add a zero-divisor guard**: handle the edge case where `total_deps == 0` to avoid
   division by zero (return 0.0 or an appropriate sentinel).

## Reproducer Strategy

Write a test in `modules/risk/tests/score_test.rs` that uses asymmetric inputs where
`total_deps != vulnerable_deps` (e.g., `total=100, vulnerable=5`):

- **Before fix**: the test asserts the score equals `0.05` and fails (actual is `20.0`),
  confirming the bug exists.
- **After fix**: the test passes, confirming the bug is resolved.

The existing test `test_risk_score_all_vulnerable` uses symmetric inputs (`10, 10`)
that produce 1.0 regardless of operand order, so it does not catch this bug.
Additionally, add an integration test that creates an assessment via `create_assessment()`
and verifies the persisted `risk_score` is correct.

## Affects Version Resolution (Step 4.5)

The Environment / Version section states "Not specified." No version information can
be extracted. The `affectsVersions` field on the Bug issue is not populated.

Action: Post a comment on ACME-520 flagging that the Affects Version could not be
determined from the bug description and should be set manually.
