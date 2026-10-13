<!-- Jira API Metadata -->
<!-- jira.create_issue parameters: -->
<!-- project: ACME -->
<!-- issue_type: Task -->
<!-- labels: ["ai-generated-jira"] -->

## Repository
acme-backend

## Target Branch
main

## Description
Fix swapped numerator/denominator in `compute_risk_score()` and migrate existing assessments with incorrect persisted risk scores. The function currently computes `total_deps / vulnerable_deps` instead of `vulnerable_deps / total_deps`, producing inflated risk scores that are the reciprocal of the correct value. Because the score is persisted at ingestion time and never recomputed on read, all existing assessments in the database contain incorrect values. Fixes ACME-520.

## Files to Modify
- `modules/risk/src/score.rs` -- swap division operands in `compute_risk_score()` to `vulnerable_deps as f64 / total_deps as f64`

## Files to Create
- `modules/risk/tests/score_regression_test.rs` -- reproducer test for ACME-520 that verifies correct risk score computation with asymmetric inputs
- `migration/2024-04-01-000004_fix_risk_score_values/up.sql` -- data migration to recompute and correct all existing `risk_score` values in the `assessments` table
- `migration/2024-04-01-000004_fix_risk_score_values/down.sql` -- rollback migration to reverse the correction

## Implementation Notes
### Code fix
In `modules/risk/src/score.rs`, change the `compute_risk_score()` function body from:
```rust
total_deps as f64 / vulnerable_deps as f64
```
to:
```rust
vulnerable_deps as f64 / total_deps as f64
```

### Reproducer test
Translate the Steps to Reproduce into a unit test in `modules/risk/tests/score_regression_test.rs`:
- Call `compute_risk_score(100, 5)` (100 total deps, 5 vulnerable)
- **Before fix**: returns `20.0` (incorrect -- total/vulnerable)
- **After fix**: returns `0.05` (correct -- vulnerable/total)
- Assert: `assert!((score - 0.05).abs() < f64::EPSILON)`
- Reference existing test pattern in `modules/risk/tests/score_test.rs` for structure and imports

Also add a test with `vulnerable_deps = 0` to verify division-by-zero handling, and a test with `total_deps = vulnerable_deps` to ensure the result is `1.0`.

### Data migration
The `risk_score` column in the `assessments` table contains incorrect values written at ingestion time by `create_assessment()` in `modules/risk/src/assessment.rs`. The incorrect value is the reciprocal of the correct value (`total/vulnerable` instead of `vulnerable/total`), so the migration can correct existing rows by inverting the stored value.

Follow the existing Diesel migration convention observed in the `migration/` directory (format: `YYYY-MM-DD-NNNNNN_description/up.sql`).

**up.sql** should contain:
```sql
-- Correct risk_score values that were stored with swapped numerator/denominator.
-- The incorrect value is the reciprocal of the correct value, so we invert it.
-- Guard against division by zero for any rows where risk_score = 0.
UPDATE assessments
SET risk_score = 1.0 / risk_score
WHERE risk_score != 0;
```

**down.sql** should reverse the migration by applying the same inversion (since inverting a reciprocal yields the original value):
```sql
UPDATE assessments
SET risk_score = 1.0 / risk_score
WHERE risk_score != 0;
```

### Existing patterns
- Existing test file: `modules/risk/tests/score_test.rs` -- follow the same test structure and assertion style
- Existing migration examples: `migration/2024-01-15-000001_create_sboms/`, `migration/2024-02-20-000002_create_assessments/`, `migration/2024-03-10-000003_add_severity_column/`

## Acceptance Criteria
- [ ] A reproducer test calls `compute_risk_score(100, 5)` and asserts the result is `0.05` (vulnerable / total), not `20.0` (total / vulnerable). This test fails before the fix and passes after.
- [ ] Existing assessments with incorrect `risk_score` values are corrected by the data migration (`migration/2024-04-01-000004_fix_risk_score_values/up.sql`).
- [ ] `compute_risk_score()` returns `vulnerable_deps / total_deps` for all inputs.
- [ ] The `GET /api/v2/assessments/{id}` endpoint returns the correct risk score for both new and previously-created assessments.
- [ ] No regression in existing tests (including `test_risk_score_all_vulnerable` in `modules/risk/tests/score_test.rs`).

## Test Requirements
- [ ] Reproducer test: `test_risk_score_swapped_operands` -- calls `compute_risk_score(100, 5)`, asserts result equals `0.05`. Fails before fix (returns `20.0`), passes after. Place in `modules/risk/tests/score_regression_test.rs`.
- [ ] Edge case test: `test_risk_score_zero_vulnerable` -- calls `compute_risk_score(100, 0)`, verifies no panic or division by zero, asserts result is `0.0`.
- [ ] Symmetry test: `test_risk_score_all_deps_vulnerable` -- calls `compute_risk_score(10, 10)`, asserts result is `1.0`.
- [ ] Verify existing test `test_risk_score_all_vulnerable` continues to pass unchanged.
- [ ] Migration test: verify that running the up.sql migration against a database with known incorrect values produces the corrected values.

## Verification Commands
- `cargo test -p risk` -- all risk module tests pass, including the new reproducer test
- `diesel migration run` -- data migration executes successfully
- `diesel migration redo` -- migration is reversible (down.sql + up.sql round-trips correctly)

## Bug Context

- **Bug**: [ACME-520](https://mock-jira.example.com/browse/ACME-520)
- **Steps to Reproduce**: Ingest an SBOM with 100 total dependencies (5 vulnerable), create a risk assessment, retrieve it via GET /api/v2/assessments/{id}, and inspect the risk_score field.
- **Expected Result**: Risk score should be `5 / 100 = 0.05` (vulnerable / total).
- **Actual Result**: Risk score is `100 / 5 = 20.0` (total / vulnerable) -- numerator and denominator are swapped.
- **Root Cause**: `compute_risk_score()` in `modules/risk/src/score.rs` divides `total_deps / vulnerable_deps` instead of `vulnerable_deps / total_deps`. The incorrect score is persisted to the `assessments` table at ingestion time and never recomputed on read, so all existing assessments contain incorrect values.
