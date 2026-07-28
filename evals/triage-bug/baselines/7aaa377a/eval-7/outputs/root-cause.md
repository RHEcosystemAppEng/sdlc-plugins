# Root Cause Analysis — ACME-520 (Step 4)

## Root Cause

**What is broken:** `compute_risk_score()` in `modules/risk/src/score.rs` returns an
inverted risk score. The function is supposed to compute `vulnerable_deps / total_deps`
(the fraction of dependencies that are vulnerable), but instead computes
`total_deps / vulnerable_deps` (the inverse ratio).

**Why it is broken:** The division operands are transposed. The expression
`total_deps as f64 / vulnerable_deps as f64` has the numerator and denominator swapped
relative to the intended formula. For a real-world input such as 100 total / 5 vulnerable,
the bug produces `20.0` where the correct value is `0.05` — a 400× inflation.

**Where it is broken:**

| Location | Symbol | Defect |
|----------|--------|--------|
| `modules/risk/src/score.rs` | `compute_risk_score()` | Operands reversed in division |
| `modules/risk/src/assessment.rs` | `create_assessment()` | Persists the wrong value to `assessments.risk_score` |

**Why existing tests did not catch it:** The only test in
`modules/risk/tests/score_test.rs` calls `compute_risk_score(10, 10)`. When
`total == vulnerable`, both orderings of division yield `1.0`, so the test passes
regardless of which operand is in the numerator. The degenerate equal-input case
masks the logic error completely.

## Affected Files

- **`modules/risk/src/score.rs`** — `compute_risk_score()`: the defective expression
- **`modules/risk/src/assessment.rs`** — `create_assessment()`: persists the stale value
- **`modules/risk/tests/score_test.rs`** — existing test suite: gap in coverage

## Persistence Impact

The incorrect score is written to the `assessments` table (`risk_score` column) at
assessment creation time. The read endpoint (`get_assessment()` in
`modules/risk/src/endpoints.rs`) reads the stored value directly without recomputing.
All existing assessment rows created while the bug was active carry inflated
`risk_score` values. A code fix alone does not correct them — a data migration is
required.

## Suggested Approach

1. **Fix the code**: swap the operands in `compute_risk_score()` so the expression
   reads `vulnerable_deps as f64 / total_deps as f64`.
2. **Add a reproducer test**: in `modules/risk/tests/score_test.rs`, add a test that
   calls `compute_risk_score(100, 5)` and asserts the result is approximately `0.05`.
   This test will fail against the current code and pass after the fix.
3. **Write a data migration**: create
   `migration/2026-07-28-000004_fix_risk_score_values/up.sql` to update existing
   `assessments` rows. Since the bug is a pure operand swap, the correct value for any
   row is the reciprocal of its stored value:
   ```sql
   UPDATE assessments
   SET risk_score = 1.0 / risk_score
   WHERE risk_score != 0;
   ```
   Provide a corresponding `down.sql` that re-inverts the values (applying the same
   reciprocal transform restores the previous state).

## Reproducer Strategy

- **Trigger**: call `compute_risk_score(100, 5)` directly, or call `create_assessment()`
  with an SBOM that has 100 total and 5 vulnerable dependencies.
- **Pre-fix assertion**: result equals `20.0` (or `risk_score` in the database is `20.0`).
- **Post-fix assertion**: result equals `0.05` (within floating-point tolerance,
  e.g., `(score - 0.05).abs() < 1e-9`).
- **Existing test to update**: `test_risk_score_all_vulnerable` in
  `modules/risk/tests/score_test.rs` should be supplemented with a new test that
  uses asymmetric inputs.

## Decomposition Guard

Single root cause: one transposed expression in one function, with a cascading
persistence side effect that requires a migration. No independent issues.
A single Task is appropriate.
