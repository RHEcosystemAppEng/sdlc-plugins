<!-- Jira API metadata
jira.create_issue:
  project: ACME
  issueType: Task
  labels:
    - ai-generated-jira
-->

## Repository
acme-backend

## Target Branch
main

## Description
Fix the swapped numerator/denominator in `compute_risk_score()` and create a data migration to correct all existing assessment records that have incorrect persisted `risk_score` values.

The `compute_risk_score()` function in `modules/risk/src/score.rs` computes `total_deps / vulnerable_deps` instead of `vulnerable_deps / total_deps`, producing inflated risk scores. Because `create_assessment()` persists the computed score to the `assessments.risk_score` column at ingestion time and the read path (`get_assessment()`) does not recompute it, all existing assessments in the database have incorrect values. Both a code fix and a data migration are required.

## Files to Modify
- `modules/risk/src/score.rs` -- fix the swapped operands in `compute_risk_score()`: change `total_deps as f64 / vulnerable_deps as f64` to `vulnerable_deps as f64 / total_deps as f64`

## Files to Create
- `migration/YYYY-MM-DD-NNNNNN_fix_risk_score_values/up.sql` -- data migration to recompute and update existing `risk_score` values in the `assessments` table (following the Diesel naming convention used by existing migrations)
- `migration/YYYY-MM-DD-NNNNNN_fix_risk_score_values/down.sql` -- rollback migration
- `modules/risk/tests/score_test.rs` -- add reproducer test (or add to existing test file)

## Implementation Notes
- **Code fix**: In `modules/risk/src/score.rs`, swap the operands in `compute_risk_score()` so it returns `vulnerable_deps as f64 / total_deps as f64` instead of `total_deps as f64 / vulnerable_deps as f64`.
- **Data migration**: The `up.sql` migration must recompute and update existing `risk_score` values in the `assessments` table. The migration logic should perform: `UPDATE assessments SET risk_score = vulnerable_deps::double precision / total_deps::double precision` (correcting the swapped operands). The exact column references depend on whether `total_deps` and `vulnerable_deps` are stored on the `assessments` table or need to be joined from a related table (e.g., `sboms`). Follow the Diesel migration convention observed in the existing migrations: `migration/YYYY-MM-DD-NNNNNN_description/up.sql`.
- **Existing migration reference**: The last migration is `migration/2024-03-10-000003_add_severity_column/`. The new migration should follow the same naming scheme with the next sequence number.
- **Reproducer test**: The existing test `test_risk_score_all_vulnerable` in `modules/risk/tests/score_test.rs` uses `compute_risk_score(10, 10)` which returns 1.0 regardless of operand order. The reproducer test must use inputs where `total_deps != vulnerable_deps` (e.g., `compute_risk_score(100, 5)` should return `0.05`).

## Acceptance Criteria
- [ ] A reproducer test is added that calls `compute_risk_score()` with `total_deps != vulnerable_deps` (e.g., `compute_risk_score(100, 5)`) and asserts the correct result (`0.05`); this test fails before the fix and passes after
- [ ] A data migration (`migration/YYYY-MM-DD-NNNNNN_fix_risk_score_values/up.sql`) is created that recomputes and updates all existing `risk_score` values in the `assessments` table, correcting the previously persisted incorrect values
- [ ] The `compute_risk_score()` function in `modules/risk/src/score.rs` is fixed to return `vulnerable_deps as f64 / total_deps as f64` (correct operand order)
- [ ] The existing test `test_risk_score_all_vulnerable` continues to pass
- [ ] Creating a new assessment after the fix produces the correct risk score (e.g., 100 total deps and 5 vulnerable produces `0.05`)
- [ ] Retrieving an existing assessment that was affected by the bug now returns the corrected `risk_score` (verified via `GET /api/v2/assessments/{id}`)

## Test Requirements
- [ ] Unit test: `compute_risk_score(100, 5)` returns `0.05` (reproducer for the swapped operands)
- [ ] Unit test: `compute_risk_score(50, 0)` handles the zero-vulnerable-deps edge case appropriately (no division by zero)
- [ ] Integration test: creating an assessment and retrieving it produces a consistent and correct `risk_score`

## Verification Commands
- `cargo test --package risk` -- all risk module tests pass, including the new reproducer test
- `diesel migration run` -- the data migration executes successfully
- `diesel migration redo` -- the migration is reversible

## Bug Context
- **Bug Key**: ACME-520
- **Summary**: Risk scores are computed with wrong denominator, producing inflated values
- **Steps to Reproduce**:
  1. Ingest an SBOM with 100 total dependencies, 5 of which are vulnerable.
  2. Create a risk assessment for the ingested SBOM.
  3. Retrieve the risk assessment via `GET /api/v2/assessments/{id}`.
  4. Inspect the `risk_score` field.
- **Expected Result**: The risk score should be `5 / 100 = 0.05` (vulnerable / total).
- **Actual Result**: The risk score is `100 / 5 = 20.0` (total / vulnerable). The numerator and denominator are swapped.
- **Root Cause**: `compute_risk_score()` in `modules/risk/src/score.rs` divides `total_deps / vulnerable_deps` instead of `vulnerable_deps / total_deps`. The incorrect value is persisted to the `assessments.risk_score` column at creation time and is never recomputed on read, so all existing assessments have wrong scores stored in the database.
