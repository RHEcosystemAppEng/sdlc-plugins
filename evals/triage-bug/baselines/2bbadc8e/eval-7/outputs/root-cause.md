# Step 4 -- Root Cause Analysis: ACME-520

## Root Cause

The `compute_risk_score()` function in `modules/risk/src/score.rs` has its division operands swapped. It computes `total_deps / vulnerable_deps` instead of `vulnerable_deps / total_deps`, producing inflated risk scores for all assessments where total dependencies differs from vulnerable dependencies.

The existing test (`test_risk_score_all_vulnerable` in `modules/risk/tests/score_test.rs`) uses equal values (`compute_risk_score(10, 10)`) and therefore passes regardless of operand order, masking the bug.

## What is broken

The division in `compute_risk_score()` reverses numerator and denominator:

- **Buggy**: `total_deps as f64 / vulnerable_deps as f64` (e.g., 100/5 = 20.0)
- **Correct**: `vulnerable_deps as f64 / total_deps as f64` (e.g., 5/100 = 0.05)

## Why it is broken

The operands were placed in the wrong order in the division expression. The function signature receives `(total_deps, vulnerable_deps)` but the body divides `total_deps / vulnerable_deps` instead of `vulnerable_deps / total_deps`. No test with asymmetric inputs existed to catch the mistake.

## Where it is broken

- **Primary defect**: `modules/risk/src/score.rs` -- `compute_risk_score()` function
- **Persistence caller**: `modules/risk/src/assessment.rs` -- `create_assessment()` writes the incorrect score to the `assessments.risk_score` column at ingestion time
- **Read path**: `modules/risk/src/endpoints.rs` -- `get_assessment()` returns the persisted (incorrect) value without recomputation

## Persistence impact

The buggy risk score is persisted to the `assessments` table (`risk_score` column) at ingestion time via `diesel::insert_into`. It is NOT recomputed on read. All existing assessments have inflated `risk_score` values. A data migration is required to correct existing records.

## How to verify the fix

A reproducer test should:

1. Call `compute_risk_score()` with asymmetric inputs (e.g., `total_deps=100, vulnerable_deps=5`)
2. Assert the result equals `0.05` (vulnerable / total), not `20.0` (total / vulnerable)
3. Additionally test edge cases: `vulnerable_deps=0` (should handle gracefully), `total_deps == vulnerable_deps` (should return `1.0`)

## Affects Version Resolution (Step 4.5)

The Environment / Version section states "Not specified." No version information can be extracted. Affects Version cannot be determined from the bug description. This would be flagged with a comment on the Bug issue per Step 4.5.6.
