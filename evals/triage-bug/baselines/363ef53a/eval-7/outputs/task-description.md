<!-- Jira API metadata — jira.create_issue parameters -->
<!-- project: ACME -->
<!-- issuetype: { "id": "10142" } -->
<!-- labels: ["ai-generated-jira", "bug-fix", "data-migration"] -->
<!-- linked issue: ACME-520 (link type: Blocks) -->

## Repository
acme-backend

## Target Branch
main

## Description
Fix the swapped division operands in `compute_risk_score()` and create a data migration to correct all existing assessment records that were persisted with incorrect risk scores. The function currently computes `total_deps / vulnerable_deps` instead of the correct `vulnerable_deps / total_deps`, producing inflated scores. Because the score is persisted at assessment creation time and never recomputed on read, all existing rows in the `assessments` table contain incorrect values.

## Files to Modify
- `modules/risk/src/score.rs` -- swap the division operands in `compute_risk_score()` so it returns `vulnerable_deps / total_deps`

## Files to Create
- `migration/YYYY-MM-DD-NNNNNN_fix_risk_scores/up.sql` -- data migration to correct existing `risk_score` values in the `assessments` table (follow the Diesel naming convention used by existing migrations, e.g. `migration/2024-10-07-000004_fix_risk_scores/up.sql`)
- `migration/YYYY-MM-DD-NNNNNN_fix_risk_scores/down.sql` -- reversible migration (restore original values by inverting again)
- `modules/risk/tests/score_regression_test.rs` -- reproducer test for the bug

## Implementation Notes
- **Code fix**: In `modules/risk/src/score.rs`, change `total_deps as f64 / vulnerable_deps as f64` to `vulnerable_deps as f64 / total_deps as f64`.
- **Data migration**: Write an `up.sql` that updates all rows in the `assessments` table. The corrected score is the reciprocal of the current value: `UPDATE assessments SET risk_score = 1.0 / risk_score WHERE risk_score != 0;`. This works because swapping numerator and denominator is equivalent to taking the reciprocal. Add a guard for `risk_score != 0` to avoid division-by-zero. Also handle the edge case where `risk_score IS NULL` (skip those rows).
- **Diesel migration convention**: Existing migrations use the pattern `YYYY-MM-DD-NNNNNN_description/` with `up.sql` and `down.sql`. Follow the same convention.
- **Existing test gap**: The current test in `modules/risk/tests/score_test.rs` (`test_risk_score_all_vulnerable`) uses equal values for total and vulnerable deps (10, 10), which passes regardless of operand order. The new reproducer test must use asymmetric values.

## Reuse Candidates
- `modules/risk/tests/score_test.rs::test_risk_score_all_vulnerable` -- existing test structure to follow for the new reproducer test

## Acceptance Criteria
- [ ] A reproducer test exists that fails with the current (buggy) code and passes with the fix, using asymmetric values for `total_deps` and `vulnerable_deps`
- [ ] Existing assessments with incorrect persisted `risk_score` values are corrected by the data migration
- [ ] `compute_risk_score(100, 5)` returns `0.05`, not `20.0`
- [ ] `compute_risk_score(10, 10)` still returns `1.0` (existing behavior preserved for symmetric case)
- [ ] The data migration handles edge cases: `risk_score = 0` rows are skipped, `NULL` rows are skipped
- [ ] New assessments created after the fix have correct scores
- [ ] The `down.sql` migration can reverse the data fix

## Test Requirements
- [ ] Reproducer test: `compute_risk_score(100, 5)` must return `0.05` (vulnerable_deps / total_deps), not `20.0` (total_deps / vulnerable_deps)
- [ ] Regression test: `compute_risk_score(200, 1)` must return `0.005`
- [ ] Boundary test: `compute_risk_score(N, 0)` must handle zero vulnerable deps gracefully (no division by zero)
- [ ] Existing test `test_risk_score_all_vulnerable` continues to pass

## Verification Commands
- `cargo test -p risk` -- all risk module tests pass, including the new reproducer test
- `diesel migration run` -- migration applies without errors
- `diesel migration redo` -- down.sql + up.sql round-trips correctly

## Bug Context
- **Bug Key**: ACME-520
- **Steps to Reproduce**:
  1. Ingest an SBOM with 100 total dependencies, 5 of which are vulnerable.
  2. Create a risk assessment for the ingested SBOM.
  3. Retrieve the risk assessment via `GET /api/v2/assessments/{id}`.
  4. Inspect the `risk_score` field.
- **Expected Result**: The risk score should be `5 / 100 = 0.05` (vulnerable / total).
- **Actual Result**: The risk score is `100 / 5 = 20.0` (total / vulnerable). The numerator and denominator are swapped.
- **Root Cause**: The division operands in `compute_risk_score()` (`modules/risk/src/score.rs`) are reversed -- it computes `total_deps / vulnerable_deps` instead of `vulnerable_deps / total_deps`. The incorrect value is persisted to the `assessments` table at creation time and never recomputed on read, so all existing records contain wrong scores.
