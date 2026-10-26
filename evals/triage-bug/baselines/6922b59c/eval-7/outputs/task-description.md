# Jira API Metadata

```
jira.create_issue(
  project_key: "ACME",
  issue_type: "Task",
  labels: ["ai-generated-jira"],
  summary: "Fix swapped numerator/denominator in compute_risk_score() and migrate existing data"
)
```

- **Project key**: ACME
- **Issue type**: Task
- **Labels**: ai-generated-jira

---

## Repository
acme-backend

## Target Branch
main

## Description
Fix the swapped numerator/denominator in `compute_risk_score()` which produces inflated
risk scores for all assessments, and create a data migration to correct existing persisted
values. Fixes ACME-520.

The function currently computes `total_deps / vulnerable_deps` instead of
`vulnerable_deps / total_deps`. Since the result is persisted to the `assessments` table
at ingestion time and is never recomputed on read, all existing assessments contain
incorrect risk_score values that must be corrected via a data migration.

## Files to Modify
- `modules/risk/src/score.rs` — fix the division operands in `compute_risk_score()`: change `total_deps as f64 / vulnerable_deps as f64` to `vulnerable_deps as f64 / total_deps as f64`
- `modules/risk/tests/score_test.rs` — add reproducer test with asymmetric inputs

## Files to Create
- `migration/YYYY-MM-DD-000004_fix_risk_score_values/up.sql` — data migration to recompute and update existing risk_score values in the assessments table (follow the Diesel naming convention `YYYY-MM-DD-NNNNNN_description/up.sql` as used by existing migrations in `migration/`)
- `migration/YYYY-MM-DD-000004_fix_risk_score_values/down.sql` — rollback migration

## Implementation Notes
### Code fix
Swap the division operands in `compute_risk_score()` in `modules/risk/src/score.rs`:

**Before:** `total_deps as f64 / vulnerable_deps as f64`
**After:** `vulnerable_deps as f64 / total_deps as f64`

### Data migration
The `risk_score` column in the `assessments` table is written at ingestion time by
`create_assessment()` in `modules/risk/src/assessment.rs` via
`diesel::insert_into(assessments::table)`. The value is NOT recomputed on read (the
GET endpoint in `modules/risk/src/endpoints.rs` reads the persisted value directly).
Therefore, all existing assessments contain incorrect (inflated) risk_score values.

The migration must recompute and update existing `risk_score` values in the `assessments`
table. The migration SQL should join `assessments` with the source data (sboms table or
related vulnerability counts) to recalculate the correct score as
`vulnerable_deps / total_deps` for each existing assessment row.

Example migration logic for `up.sql`:
```sql
UPDATE assessments
SET risk_score = (
    SELECT CAST(s.vulnerable_dep_count AS DOUBLE PRECISION) / CAST(s.total_dep_count AS DOUBLE PRECISION)
    FROM sboms s
    WHERE s.id = assessments.sbom_id
)
WHERE EXISTS (
    SELECT 1 FROM sboms s WHERE s.id = assessments.sbom_id
);
```

Follow the existing Diesel migration naming convention discovered in the repository:
`YYYY-MM-DD-NNNNNN_description/up.sql` (e.g., `2024-01-15-000001_create_sboms/up.sql`).

### Reproducer test
Add a test in `modules/risk/tests/score_test.rs` following the existing test pattern.
The reproducer must use asymmetric inputs where `total_deps != vulnerable_deps` so that
the operand order matters:

- Input: `compute_risk_score(100, 5)` (100 total deps, 5 vulnerable)
- Expected (correct): `0.05` (5 / 100 = vulnerable / total)
- Actual (before fix): `20.0` (100 / 5 = total / vulnerable)

The existing test `test_risk_score_all_vulnerable` uses `compute_risk_score(10, 10)` which
passes regardless of operand order — this is why the bug was not caught.

Fixes ACME-520.

## Reuse Candidates
- `modules/risk/tests/score_test.rs::test_risk_score_all_vulnerable` — existing test structure and assertion pattern for `compute_risk_score()`; follow this pattern for the reproducer test

## Acceptance Criteria
- [ ] A reproducer test exists that calls `compute_risk_score()` with asymmetric inputs (e.g., `total_deps=100, vulnerable_deps=5`), asserts the result is `0.05`, and would fail against the current (unfixed) code which returns `20.0`
- [ ] Existing assessments with incorrect persisted risk_score values are corrected by the data migration (the migration recomputes `vulnerable_deps / total_deps` for all rows in the `assessments` table)
- [ ] `compute_risk_score()` returns `vulnerable_deps / total_deps` (not `total_deps / vulnerable_deps`)
- [ ] New assessments created after the fix have correct risk_score values
- [ ] No regression in existing tests (including `test_risk_score_all_vulnerable`)

## Test Requirements
- [ ] Reproducer test: add `test_risk_score_asymmetric_inputs` in `modules/risk/tests/score_test.rs` that calls `compute_risk_score(100, 5)` and asserts the result equals `0.05`. This test must fail before the fix (returning `20.0`) and pass after
- [ ] Verify the data migration correctly updates existing risk_score values by running the migration against a test database with known assessment records
- [ ] Existing test `test_risk_score_all_vulnerable` continues to pass after the fix

## Bug Context

- **Bug**: [ACME-520](https://mock-jira.example.com/browse/ACME-520)
- **Steps to Reproduce**: Ingest SBOM with 100 total deps / 5 vulnerable, create assessment, retrieve via GET /api/v2/assessments/{id}, inspect risk_score field
- **Expected Result**: risk_score = 5 / 100 = 0.05 (vulnerable / total)
- **Actual Result**: risk_score = 100 / 5 = 20.0 (total / vulnerable) — numerator and denominator are swapped
- **Root Cause**: `compute_risk_score()` in `modules/risk/src/score.rs` divides `total_deps / vulnerable_deps` instead of `vulnerable_deps / total_deps`. The incorrect value is persisted to the `assessments` table at ingestion time and is never recomputed on read, so all existing assessments contain inflated risk_score values.
