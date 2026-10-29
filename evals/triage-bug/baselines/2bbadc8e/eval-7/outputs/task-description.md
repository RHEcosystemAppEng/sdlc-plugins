# Jira API Metadata

Parameters for `jira.create_issue`:

- **Project key**: ACME
- **Issue type**: Task
- **Labels**: `["ai-generated-jira"]`

---

## Repository
acme-backend

## Target Branch
main

## Description
Fix swapped division operands in `compute_risk_score()` and add a data migration to correct existing assessments with inflated risk scores. The function currently computes `total_deps / vulnerable_deps` instead of `vulnerable_deps / total_deps`, producing values that are the reciprocal of the correct score. Because the result is persisted to the `assessments.risk_score` column at ingestion time and never recomputed on read, all existing assessments carry incorrect values. Fixes ACME-520.

## Files to Modify
- `modules/risk/src/score.rs` -- Fix the division operand order in `compute_risk_score()` to compute `vulnerable_deps / total_deps` instead of `total_deps / vulnerable_deps`

## Files to Create
- `modules/risk/tests/score_regression_test.rs` -- Reproducer test for ACME-520 that calls `compute_risk_score()` with asymmetric inputs and asserts the correct result
- `migration/2026-10-29-000001_fix_risk_score_values/up.sql` -- Data migration to correct existing `risk_score` values in the `assessments` table
- `migration/2026-10-29-000001_fix_risk_score_values/down.sql` -- Rollback migration

## Implementation Notes
### Bug fix

In `modules/risk/src/score.rs`, swap the division operands in `compute_risk_score()`:

- **Current (buggy)**: `total_deps as f64 / vulnerable_deps as f64`
- **Correct**: `vulnerable_deps as f64 / total_deps as f64`

The function signature `compute_risk_score(total_deps: u32, vulnerable_deps: u32) -> f64` does not change.

### Reproducer test

Create a test in `modules/risk/tests/score_regression_test.rs` following the pattern in the existing test file `modules/risk/tests/score_test.rs`. The reproducer must use asymmetric inputs where `total_deps != vulnerable_deps` to detect the operand swap:

- Input: `compute_risk_score(100, 5)` (100 total deps, 5 vulnerable)
- **Incorrect output (before fix)**: `20.0` (total / vulnerable)
- **Correct output (after fix)**: `0.05` (vulnerable / total)
- The test should assert `score == 0.05` (or use approximate float comparison)

Additional test cases to consider:
- `compute_risk_score(10, 10)` should return `1.0` (the existing test case, for regression)
- `compute_risk_score(200, 1)` should return `0.005`

### Data migration

A data migration is needed to correct existing `risk_score` values in the `assessments` table. Existing migration files follow the Diesel naming convention `YYYY-MM-DD-NNNNNN_description/up.sql` in the `migration/` directory. The most recent migration is `2024-03-10-000003_add_severity_column`.

The migration must recalculate `risk_score` for all existing assessments. Since the buggy formula computed `total / vulnerable` instead of `vulnerable / total`, the correct value is the reciprocal of the stored value: `1.0 / risk_score`. The migration SQL should:

```sql
-- up.sql: Correct existing risk_score values by computing the reciprocal
-- The bug computed total_deps/vulnerable_deps instead of vulnerable_deps/total_deps
-- so the correct value = 1.0 / current_value
UPDATE assessments
SET risk_score = 1.0 / risk_score
WHERE risk_score != 0 AND risk_score IS NOT NULL;
```

```sql
-- down.sql: Reverse the correction (apply the reciprocal again to restore original values)
UPDATE assessments
SET risk_score = 1.0 / risk_score
WHERE risk_score != 0 AND risk_score IS NOT NULL;
```

Note: The reciprocal is self-inverse (`1/(1/x) = x`), so the down migration uses the same formula. The `WHERE risk_score != 0` guard prevents division by zero for any edge-case rows.

Alternatively, if the source SBOM data (total and vulnerable dependency counts) is accessible via a JOIN to the `sboms` table, a more precise migration could recompute from source:

```sql
UPDATE assessments a
SET risk_score = s.vulnerable_deps::double precision / s.total_deps::double precision
FROM sboms s
WHERE a.sbom_id = s.id AND s.total_deps > 0;
```

Use whichever approach matches the available schema -- the reciprocal approach requires no schema knowledge beyond the `assessments` table itself.

### Traceability

Fixes ACME-520.

## Reuse Candidates
- `modules/risk/tests/score_test.rs::test_risk_score_all_vulnerable` -- Existing test pattern for `compute_risk_score()` assertions; follow the same structure for the reproducer test

## Acceptance Criteria
- [ ] A reproducer test calls `compute_risk_score()` with asymmetric inputs (e.g., `total_deps=100, vulnerable_deps=5`) and asserts the result is `0.05` (not `20.0`). This test fails before the fix and passes after.
- [ ] Existing assessments with incorrect `risk_score` values are corrected by the data migration (the migration recalculates all stored scores)
- [ ] `compute_risk_score()` returns `vulnerable_deps / total_deps` for all inputs
- [ ] No regression in existing tests (`test_risk_score_all_vulnerable` continues to pass)

## Test Requirements
- [ ] Reproducer test: call `compute_risk_score(100, 5)` and assert the result equals `0.05`. This test must fail before the fix (returning `20.0`) and pass after the fix. Place in `modules/risk/tests/score_regression_test.rs` following the pattern in `modules/risk/tests/score_test.rs`.
- [ ] Additional edge case tests: `compute_risk_score(200, 1)` returns `0.005`; `compute_risk_score(10, 10)` returns `1.0`
- [ ] Verify the data migration runs without error and correctly updates existing `risk_score` values in the `assessments` table

## Verification Commands
- `cargo test --package risk` -- All risk module tests pass, including the new reproducer test
- `diesel migration run` -- Data migration executes successfully

## Bug Context

- **Bug**: [ACME-520](https://mock-jira.example.com/browse/ACME-520)
- **Steps to Reproduce**: Ingest an SBOM with 100 total dependencies (5 vulnerable), create a risk assessment, retrieve it via `GET /api/v2/assessments/{id}`, and inspect the `risk_score` field.
- **Expected Result**: Risk score should be `5 / 100 = 0.05` (vulnerable / total).
- **Actual Result**: Risk score is `100 / 5 = 20.0` (total / vulnerable). The numerator and denominator are swapped.
- **Root Cause**: `compute_risk_score()` in `modules/risk/src/score.rs` divides `total_deps / vulnerable_deps` instead of `vulnerable_deps / total_deps`. The result is persisted to `assessments.risk_score` at ingestion time and never recomputed on read, so all existing assessments carry incorrect values.
