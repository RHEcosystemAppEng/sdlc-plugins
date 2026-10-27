<!-- Jira API metadata block -->
<!-- jira.create_issue parameters:
  project: ACME
  issue_type: Task
  labels: ["ai-generated-jira"]
-->

## Repository
acme-backend

## Target Branch
main

## Description
Fix the swapped operands in `compute_risk_score()` that produce inflated risk scores, add a reproducer test to prevent regression, and create a data migration to correct existing persisted `risk_score` values in the `assessments` table. Fixes ACME-520.

## Files to Modify
- `modules/risk/src/score.rs` -- Fix the division operand order in `compute_risk_score()`: change `total_deps as f64 / vulnerable_deps as f64` to `vulnerable_deps as f64 / total_deps as f64`
- `modules/risk/tests/score_test.rs` -- Add a reproducer test with asymmetric inputs (total_deps != vulnerable_deps)

## Files to Create
- `migration/YYYY-MM-DD-NNNNNN_fix_risk_scores/up.sql` -- Data migration to recompute and update existing `risk_score` values in the `assessments` table using the corrected formula (following existing Diesel migration naming convention: `YYYY-MM-DD-NNNNNN_description/up.sql`)
- `migration/YYYY-MM-DD-NNNNNN_fix_risk_scores/down.sql` -- Rollback migration (reverses the risk score correction)

## Implementation Notes
### Reproducer test guidance

The reproducer test must use asymmetric input values where `total_deps != vulnerable_deps` to expose the operand swap. For example:

- **Input**: `compute_risk_score(100, 5)` (100 total deps, 5 vulnerable)
- **Incorrect output (before fix)**: `100.0 / 5.0 = 20.0` -- this is what the buggy code produces
- **Correct output (after fix)**: `5.0 / 100.0 = 0.05` -- this is what the test should assert

The existing test `test_risk_score_all_vulnerable` in `modules/risk/tests/score_test.rs` uses `compute_risk_score(10, 10)` which returns `1.0` regardless of operand order and therefore does not catch this bug. Follow the same test file and assertion pattern (`assert_eq!`) used in that existing test.

### Code fix

In `modules/risk/src/score.rs`, change the function body of `compute_risk_score()` from:

```rust
total_deps as f64 / vulnerable_deps as f64
```

to:

```rust
vulnerable_deps as f64 / total_deps as f64
```

This corrects future assessments. The `create_assessment()` function in `modules/risk/src/assessment.rs` calls `compute_risk_score()` and persists its return value via `diesel::insert_into(assessments::table)` into the `risk_score` column. No changes are needed in `create_assessment()` or `get_assessment()` -- fixing the computation function is sufficient for new data.

### Data migration

A data migration is required to correct existing records. The `risk_score` column in the `assessments` table was written at ingestion time by `create_assessment()` and is never recomputed on read. All existing rows contain incorrect (inflated) values.

The migration should:
1. Join the `assessments` table with the source data to obtain the original `total_deps` and `vulnerable_deps` values for each assessment.
2. Recompute the correct risk score as `vulnerable_deps::double precision / total_deps::double precision`.
3. Update the `risk_score` column for all existing rows with the corrected value.

Follow the existing Diesel migration convention discovered in the repository:
- Directory structure: `migration/YYYY-MM-DD-NNNNNN_description/up.sql` (and `down.sql`)
- Existing examples: `migration/2024-01-15-000001_create_sboms/`, `migration/2024-02-20-000002_create_assessments/`, `migration/2024-03-10-000003_add_severity_column/`

Fixes ACME-520.

## Reuse Candidates
- `modules/risk/tests/score_test.rs::test_risk_score_all_vulnerable` -- Existing test in the same file; follow its assertion pattern (`assert_eq!`) for the reproducer test

## Acceptance Criteria
- [ ] A reproducer test exists that calls `compute_risk_score()` with asymmetric inputs (e.g., `total_deps=100, vulnerable_deps=5`), asserts the correct result (`0.05`), fails before the fix, and passes after the fix
- [ ] Existing assessments with incorrect persisted `risk_score` values are corrected by the data migration
- [ ] `compute_risk_score()` returns `vulnerable_deps / total_deps` (not the inverse) for all inputs
- [ ] The data migration file follows the existing Diesel naming convention (`YYYY-MM-DD-NNNNNN_fix_risk_scores/up.sql`)
- [ ] No regression in existing tests (including `test_risk_score_all_vulnerable`)

## Test Requirements
- [ ] Reproducer test: add a test in `modules/risk/tests/score_test.rs` that calls `compute_risk_score(100, 5)` and asserts the result equals `0.05`. This test must fail with the current (buggy) code and pass after the fix. Use the same `assert_eq!` pattern as the existing `test_risk_score_all_vulnerable` test.
- [ ] Verify that the existing `test_risk_score_all_vulnerable` test continues to pass after the fix (score of `1.0` when all deps are vulnerable).

## Verification Commands
- `cargo test --package risk` -- All tests in the risk module pass, including the new reproducer test
- `diesel migration run` -- Data migration executes successfully and corrects existing risk_score values

## Bug Context

- **Bug**: [ACME-520](https://mock-jira.example.com/browse/ACME-520)
- **Steps to Reproduce**: Ingest an SBOM with 100 total dependencies (5 vulnerable), create a risk assessment, retrieve it via `GET /api/v2/assessments/{id}`, and inspect the `risk_score` field.
- **Expected Result**: Risk score should be `5 / 100 = 0.05` (vulnerable / total).
- **Actual Result**: Risk score is `100 / 5 = 20.0` (total / vulnerable). The numerator and denominator are swapped.
- **Root Cause**: The `compute_risk_score()` function in `modules/risk/src/score.rs` divides `total_deps / vulnerable_deps` instead of `vulnerable_deps / total_deps`. The incorrect result is persisted to the `assessments` table at ingestion time and never recomputed on read.
