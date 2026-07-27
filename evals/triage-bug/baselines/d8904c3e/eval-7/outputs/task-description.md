# Jira API Metadata

Parameters for `jira.create_issue`:

- **Project key**: ACME
- **Issue type**: Task
- **Labels**: `ai-generated-jira`, `bug-fix`

---

## Repository
acme-backend

## Target Branch
main

## Description
Fix the swapped operands in `compute_risk_score()` that produce inflated risk scores, and add a data migration to correct existing assessment records that persisted the incorrect values. The function currently computes `total_deps / vulnerable_deps` instead of `vulnerable_deps / total_deps`, and the result is written to the `assessments.risk_score` column at ingestion time. Fixing the code alone only corrects future assessments -- existing rows retain the wrong score and must be migrated.

Fixes ACME-520.

## Files to Modify
- `modules/risk/src/score.rs` -- swap the division operands in `compute_risk_score()` from `total_deps / vulnerable_deps` to `vulnerable_deps / total_deps`

## Files to Create
- `migration/2024-04-01-000004_fix_risk_scores/up.sql` -- data migration to recompute `risk_score` for all existing rows in the `assessments` table using the corrected formula
- `migration/2024-04-01-000004_fix_risk_scores/down.sql` -- reversibility migration (revert to the old formula, or no-op if data loss is acceptable)
- `modules/risk/tests/score_regression_test.rs` -- reproducer test with asymmetric inputs to verify the fix and prevent regression

## Implementation Notes
The fix has two parts: a code fix and a data migration.

**Code fix**: In `modules/risk/src/score.rs`, change the `compute_risk_score()` function body from:

```rust
total_deps as f64 / vulnerable_deps as f64
```

to:

```rust
vulnerable_deps as f64 / total_deps as f64
```

**Data migration**: Create a new Diesel migration following the existing convention in `migration/`. Existing migrations use the naming pattern `YYYY-MM-DD-NNNNNN_description/` with `up.sql` and `down.sql` files. The `up.sql` should recompute the `risk_score` column for all existing rows in the `assessments` table. The corrected score can be derived from the source SBOM data by joining with the `sboms` table to obtain the total and vulnerable dependency counts:

```sql
UPDATE assessments
SET risk_score = (
    SELECT CAST(s.vulnerable_deps AS DOUBLE PRECISION) / CAST(s.total_deps AS DOUBLE PRECISION)
    FROM sboms s
    WHERE s.id = assessments.sbom_id
)
WHERE EXISTS (
    SELECT 1 FROM sboms s WHERE s.id = assessments.sbom_id AND s.total_deps > 0
);
```

The exact column names for vulnerable and total dependency counts on the `sboms` table should be verified during implementation.

**Reproducer test**: The existing test `test_risk_score_all_vulnerable` in `modules/risk/tests/score_test.rs` uses equal inputs (10, 10) and passes regardless of operand order. The reproducer test must use asymmetric inputs (e.g., `total_deps=100, vulnerable_deps=5`) to distinguish between the correct and incorrect formulas.

**Existing test pattern**: Follow the assertion style used in `modules/risk/tests/score_test.rs`.

## Acceptance Criteria
- [ ] Reproducer test: a test calling `compute_risk_score(100, 5)` asserts that the result is `0.05` (vulnerable / total). This test must fail before the fix (producing `20.0`) and pass after.
- [ ] The `compute_risk_score()` function in `modules/risk/src/score.rs` computes `vulnerable_deps / total_deps` (not the inverse)
- [ ] A data migration corrects the `risk_score` column for all existing rows in the `assessments` table by recomputing the score using the corrected formula
- [ ] The `GET /api/v2/assessments/{id}` endpoint returns the corrected score for both new and previously-existing assessments
- [ ] No regression in existing tests (`test_risk_score_all_vulnerable` continues to pass)

## Test Requirements
- [ ] Reproducer test: call `compute_risk_score(100, 5)` and assert the result equals `0.05`. With the buggy code this returns `20.0` (100/5), so the test fails before the fix and passes after. Also test the edge case `compute_risk_score(100, 0)` to verify division-by-zero handling.
- [ ] Verify that the existing test `test_risk_score_all_vulnerable` (which uses equal inputs 10, 10) continues to pass after the fix
- [ ] Verify the data migration produces correct scores for existing assessment records

## Verification Commands
- `cargo test --package risk` -- run all risk module tests including the reproducer
- `diesel migration run` -- apply the data migration to correct existing assessment records

## Bug Context
- **Bug**: [ACME-520](https://mock-jira.example.com/browse/ACME-520)
- **Steps to Reproduce**:
  1. Ingest an SBOM with 100 total dependencies, 5 of which are vulnerable
  2. Create a risk assessment for the ingested SBOM
  3. Retrieve the risk assessment via `GET /api/v2/assessments/{id}`
  4. Inspect the `risk_score` field
- **Expected Result**: The risk score should be `5 / 100 = 0.05` (vulnerable / total)
- **Actual Result**: The risk score is `100 / 5 = 20.0` (total / vulnerable). The numerator and denominator are swapped.
- **Root Cause**: The `compute_risk_score()` function in `modules/risk/src/score.rs` divides `total_deps / vulnerable_deps` instead of `vulnerable_deps / total_deps`. The incorrect score is persisted to the `assessments.risk_score` column at ingestion time and is never recomputed on read, so all existing assessments retain the inflated value.
