# Step 4 -- Root Cause Analysis: ACME-520

## Root Cause

The `compute_risk_score()` function in `modules/risk/src/score.rs` has its division
operands reversed. It computes `total_deps / vulnerable_deps` instead of
`vulnerable_deps / total_deps`, producing inflated risk scores that grow larger as
the proportion of vulnerable dependencies shrinks.

For the scenario in the bug report (100 total deps, 5 vulnerable), the function
returns `20.0` instead of the correct `0.05` -- a 400x error.

## What Is Broken

The division operands in `compute_risk_score()` are swapped:

```rust
// Current (buggy):
total_deps as f64 / vulnerable_deps as f64

// Correct:
vulnerable_deps as f64 / total_deps as f64
```

## Why It Is Broken

The numerator and denominator were accidentally transposed. The function signature
lists `total_deps` first and `vulnerable_deps` second, and the implementation
divides them in parameter order rather than in the correct mathematical order
(vulnerable / total).

The existing test (`test_risk_score_all_vulnerable`) uses equal values (10, 10),
which produces `1.0` regardless of operand order -- so the bug was never caught
by tests.

## Where It Is Broken

| File | Symbol | Defect |
|------|--------|--------|
| `modules/risk/src/score.rs` | `compute_risk_score()` | Division operands reversed |

### Persistence impact (secondary defect location)

| File | Symbol | Impact |
|------|--------|--------|
| `modules/risk/src/assessment.rs` | `create_assessment()` | Persists the incorrect score to `assessments.risk_score` at ingestion time |
| `modules/risk/src/endpoints.rs` | `get_assessment()` | Reads the stale persisted value without recomputation |

All existing assessment records in the `assessments` table contain incorrect
`risk_score` values. A data migration is required alongside the code fix.

## How to Verify the Fix

A reproducer test should:

1. Call `compute_risk_score(100, 5)` and assert the result is `0.05` (not `20.0`).
2. Test additional cases where `total_deps != vulnerable_deps` to ensure the
   formula is correct across a range of inputs.
3. Verify that the existing test `test_risk_score_all_vulnerable` (10, 10 = 1.0)
   still passes (no regression).

For the persistence fix:

4. After running the data migration, verify that existing assessment records
   have corrected `risk_score` values.

## Reproducer Strategy

- **Test file**: `modules/risk/tests/score_test.rs` (add new test alongside existing)
- **Key assertion**: `compute_risk_score(100, 5)` should equal `0.05`
- **Before fix**: test fails (returns `20.0`)
- **After fix**: test passes (returns `0.05`)

## Affects Version Resolution

The Environment / Version section states "Not specified." No version information
can be extracted. Affects Version could not be determined from the bug description
and should be set manually.
