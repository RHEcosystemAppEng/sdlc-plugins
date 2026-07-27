# Step 4: Root Cause Analysis

This is the comment that would be posted on Bug ACME-520.

---

## Root Cause

### What is broken

The `compute_risk_score()` function in `modules/risk/src/score.rs` divides `total_deps / vulnerable_deps` instead of `vulnerable_deps / total_deps`. The numerator and denominator are swapped, producing inflated risk scores. For example, an SBOM with 100 total dependencies and 5 vulnerable ones yields a score of `20.0` instead of the correct `0.05`.

### Why it is broken

The division operands in `compute_risk_score()` are reversed. The function performs `total_deps as f64 / vulnerable_deps as f64` when it should perform `vulnerable_deps as f64 / total_deps as f64`. The existing test (`test_risk_score_all_vulnerable`) uses equal inputs (`10, 10`), so it passes regardless of operand order and does not detect the inversion.

### Where it is broken

- **Buggy function**: `modules/risk/src/score.rs` -- `compute_risk_score()`, the division expression
- **Persistence site**: `modules/risk/src/assessment.rs` -- `create_assessment()`, which writes the incorrect score to the `assessments` table (`risk_score` column) at ingestion time
- **Read path**: `modules/risk/src/endpoints.rs` -- `get_assessment()`, which returns the persisted (incorrect) score without recomputation

### Persistence impact

The incorrect risk score is persisted to the `assessments.risk_score` column at ingestion time (when the assessment is first created). The GET endpoint reads this value directly from the database without recomputing it. Fixing the computation alone will only correct future assessments -- all existing assessment records retain the inflated score. A data migration is required to recompute and correct the `risk_score` column for existing rows.

### How to verify the fix

1. Write a reproducer test that calls `compute_risk_score()` with asymmetric inputs (e.g., `total_deps=100, vulnerable_deps=5`).
2. Assert that the result is `0.05` (vulnerable / total), not `20.0` (total / vulnerable).
3. Verify that existing assessments are corrected by running the data migration and checking that persisted scores match the recomputed values.

### Suggested approach

1. Swap the operands in `compute_risk_score()`: change `total_deps as f64 / vulnerable_deps as f64` to `vulnerable_deps as f64 / total_deps as f64`.
2. Add a data migration to recompute `risk_score` for all existing rows in the `assessments` table using the corrected formula.
3. Add a reproducer test with asymmetric inputs to prevent regression.
