# Step 4 -- Root Cause Analysis: ACME-520

## Root Cause

The `compute_risk_score()` function in `modules/risk/src/score.rs` has its division operands swapped. It computes `total_deps / vulnerable_deps` instead of `vulnerable_deps / total_deps`, producing inflated risk scores that grow larger as the ratio of total to vulnerable dependencies increases.

The buggy expression:

```rust
total_deps as f64 / vulnerable_deps as f64   // produces 100/5 = 20.0
```

Should be:

```rust
vulnerable_deps as f64 / total_deps as f64   // produces 5/100 = 0.05
```

## What is broken

The division expression in `compute_risk_score()` reverses the numerator and denominator. For an SBOM with 100 total dependencies and 5 vulnerable ones, the function returns 20.0 instead of 0.05 -- a factor-of-400 error.

## Why it is broken

The function parameters are passed in the order `(total_deps, vulnerable_deps)`, but the division uses `total_deps` as the numerator and `vulnerable_deps` as the denominator, which is the inverse of the intended formula. The existing test (`test_risk_score_all_vulnerable`) uses equal values (10, 10) where the swap is invisible (10/10 = 1.0 either way), so the bug was never caught by automated tests.

## Where it is broken

- **Primary defect**: `modules/risk/src/score.rs`, function `compute_risk_score()` -- the division operands are swapped
- **Persistence path**: `modules/risk/src/assessment.rs`, function `create_assessment()` -- writes the incorrect score to `assessments.risk_score` at ingestion time
- **Read path**: `modules/risk/src/endpoints.rs`, function `get_assessment()` -- serves the persisted incorrect value without recomputation

## How to verify the fix

A reproducer test should:

1. Call `compute_risk_score(100, 5)` with asymmetric values where `total != vulnerable`
2. Assert the result is `0.05` (vulnerable / total), not `20.0` (total / vulnerable)
3. Additional edge cases: `compute_risk_score(100, 0)` should handle division by zero gracefully

## Persistence impact

The incorrect risk scores are persisted to the `assessments` table at ingestion time. Fixing the function corrects future assessments, but existing records retain the inflated scores. A data migration is needed to recompute `risk_score` for all existing rows.

## Affects Version Resolution (Step 4.5)

The `affectsVersions` field on ACME-520 is not populated. The Environment / Version section in the bug description states "Not specified." -- no version identifier can be extracted.

**Action**: Flag gap. A comment would be posted on ACME-520:

> Affects Version could not be determined from the bug description -- please set manually.
