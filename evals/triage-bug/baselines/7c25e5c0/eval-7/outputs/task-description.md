<!-- Jira API metadata -->
<!-- jira.create_issue parameters: -->
<!-- project: ACME -->
<!-- issueType: Task -->
<!-- labels: ["ai-generated-jira"] -->

## Repository
acme-backend

## Target Branch
main

## Description
Fix the swapped numerator/denominator in `compute_risk_score()` and create a data
migration to correct all existing assessments that have incorrect persisted
`risk_score` values.

The `compute_risk_score()` function in `modules/risk/src/score.rs` currently divides
`total_deps / vulnerable_deps` instead of `vulnerable_deps / total_deps`, producing
inflated risk scores. Because `create_assessment()` persists the computed score to
the `assessments.risk_score` column at ingestion time and the read endpoint does not
recompute it, all existing assessments in the database contain incorrect values. Both
a code fix and a data migration are required.

## Files to Modify
- `modules/risk/src/score.rs` -- swap the division operands in `compute_risk_score()` to `vulnerable_deps as f64 / total_deps as f64`

## Files to Create
- `migration/YYYY-MM-DD-NNNNNN_fix_risk_scores/up.sql` -- data migration to recompute and update all existing `risk_score` values in the `assessments` table
- `migration/YYYY-MM-DD-NNNNNN_fix_risk_scores/down.sql` -- reversibility migration (revert to old formula if needed)
- `modules/risk/tests/score_test.rs` -- add reproducer test (or add to existing test file)

## Implementation Notes
- In `modules/risk/src/score.rs`, change the `compute_risk_score()` body from
  `total_deps as f64 / vulnerable_deps as f64` to
  `vulnerable_deps as f64 / total_deps as f64`.
- The data migration must update existing rows in the `assessments` table. Since the
  `assessments` table stores only the computed `risk_score` and not the original
  `total_deps` / `vulnerable_deps` inputs, the migration will need to join against
  the source data (the `sboms` table or related vulnerability counts) to recompute
  the correct score. The migration SQL should follow this pattern:
  ```sql
  UPDATE assessments
  SET risk_score = (vulnerable_deps::double precision / total_deps::double precision)
  FROM sboms
  WHERE assessments.sbom_id = sboms.id
    AND total_deps > 0;
  ```
  Adjust column names based on where `total_deps` and `vulnerable_deps` are stored.
- Follow the existing Diesel migration convention observed in the repository:
  `YYYY-MM-DD-NNNNNN_description/up.sql` (e.g., `2024-11-02-000004_fix_risk_scores/up.sql`).
  See existing migrations in `migration/` for reference.
- Handle the edge case where `total_deps = 0` to avoid division by zero (return 0.0).

## Acceptance Criteria
- [ ] A reproducer test is added that fails before the fix and passes after (e.g., `compute_risk_score(100, 5)` asserts `0.05`)
- [ ] Existing assessments with incorrect persisted `risk_score` values are corrected by the data migration
- [ ] `compute_risk_score()` returns `vulnerable_deps / total_deps` for all new assessments
- [ ] The existing test `test_risk_score_all_vulnerable` continues to pass
- [ ] Division by zero is handled when `total_deps = 0`

## Test Requirements
- [ ] Reproducer test: call `compute_risk_score(100, 5)` and assert the result equals `0.05` -- this test must fail before the fix and pass after
- [ ] Edge case test: call `compute_risk_score(0, 0)` and verify no panic (division by zero is handled)
- [ ] Existing test `test_risk_score_all_vulnerable` (equal values case) continues to pass
- [ ] Integration test: verify that a newly created assessment persists the correct risk score

## Verification Commands
- `cargo test -p risk` -- all risk module tests pass
- `diesel migration run` -- data migration applies without error
- `diesel migration redo` -- migration is reversible

## Bug Context
- **Bug Key**: ACME-520
- **Steps to Reproduce**:
  1. Ingest an SBOM with 100 total dependencies, 5 of which are vulnerable.
  2. Create a risk assessment for the ingested SBOM.
  3. Retrieve the risk assessment via `GET /api/v2/assessments/{id}`.
  4. Inspect the `risk_score` field.
- **Expected Result**: The risk score should be `5 / 100 = 0.05` (vulnerable / total).
- **Actual Result**: The risk score is `100 / 5 = 20.0` (total / vulnerable). The numerator and denominator are swapped.
- **Root Cause**: The numerator and denominator are swapped in `compute_risk_score()` in `modules/risk/src/score.rs` -- the function computes `total_deps / vulnerable_deps` instead of `vulnerable_deps / total_deps`.
