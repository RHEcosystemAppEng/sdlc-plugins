# Step 4 -- Root Cause Analysis: ACME-520

## Root Cause

The `compute_risk_score()` function in `modules/risk/src/score.rs` has its division
operands swapped. It computes `total_deps / vulnerable_deps` instead of the correct
`vulnerable_deps / total_deps`. This produces inflated (reciprocal) risk scores for
all assessments where the number of vulnerable dependencies differs from the total.

## What is broken

The division in `compute_risk_score()` uses `total_deps as f64 / vulnerable_deps as f64`.
The numerator and denominator are reversed, so instead of a fractional ratio
(e.g., 0.05 for 5 out of 100), the function produces an inflated value (e.g., 20.0).

## Why it is broken

The function arguments `total_deps` and `vulnerable_deps` are in the correct
parameter order, but the division expression reverses them. The developer likely
placed the larger value as the numerator by mistake. The existing unit test
(`test_risk_score_all_vulnerable`) did not catch this because it uses equal values
(10/10 = 1.0), which produces the same result regardless of operand order.

## Where it is broken

- **Primary defect**: `modules/risk/src/score.rs` -- `compute_risk_score()` function,
  the division expression on line with `total_deps as f64 / vulnerable_deps as f64`
- **Persistence of incorrect data**: `modules/risk/src/assessment.rs` --
  `create_assessment()` writes the incorrect score to the `assessments` table,
  `risk_score` column, at ingestion time

## Persistence impact

The incorrect `risk_score` values are persisted to the `assessments` table at
creation time and are never recomputed on read. All existing assessments retain
inflated risk scores. A data migration is required alongside the code fix to
correct existing records.

## How to verify the fix (reproducer strategy)

A reproducer test should:

1. Call `compute_risk_score(100, 5)` -- where total != vulnerable to expose the
   asymmetry.
2. Assert the result is `0.05` (vulnerable / total), not `20.0` (total / vulnerable).
3. Also test edge cases: `compute_risk_score(10, 0)` for zero-vulnerability handling
   and `compute_risk_score(10, 10)` to confirm the identity case still passes.

## Suggested approach

1. Fix the division in `compute_risk_score()`: change to `vulnerable_deps as f64 / total_deps as f64`
2. Add a reproducer test with asymmetric inputs that would fail before the fix
3. Create a data migration to correct existing `risk_score` values in the `assessments` table
4. Verify the GET endpoint returns correct values for both new and migrated assessments

## Affects Version resolution (Step 4.5)

The Environment / Version section states "Not specified." No version information
can be extracted. The Affects Version field cannot be set -- a gap comment would
be posted on the Bug issue:

> "Affects Version could not be determined from the bug description -- please set manually."
