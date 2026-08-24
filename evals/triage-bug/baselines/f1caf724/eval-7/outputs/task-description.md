<!-- Jira API Metadata Block -->
<!--
jira.create_issue parameters:
  project:      ACME
  issue_type:   Task
  labels:       ["ai-generated-jira"]
  summary:      "Fix swapped division operands in compute_risk_score() and migrate existing data"
  link:         ACME-520 (link_type: Blocks, inward: <created-task>, outward: ACME-520)
-->

## Repository
acme-backend

## Target Branch
main

## Description
Fix the swapped numerator/denominator in `compute_risk_score()` that produces inflated risk scores, and add a data migration to correct all existing assessment records that were persisted with incorrect values. Fixes ACME-520.

## Files to Modify
- `modules/risk/src/score.rs` — Swap division operands in `compute_risk_score()` so it returns `vulnerable_deps / total_deps` instead of `total_deps / vulnerable_deps`

## Files to Create
- `modules/risk/tests/score_regression_test.rs` — Reproducer test that verifies the correct risk score computation with unequal inputs
- `migration/2026-08-24-000004_fix_risk_scores/up.sql` — Data migration to recompute and correct all existing `risk_score` values in the `assessments` table
- `migration/2026-08-24-000004_fix_risk_scores/down.sql` — Rollback migration (reverses the correction, though the old values are inherently wrong)

## Implementation Notes
**Fixes ACME-520.**

### Reproducer test guidance
The reproducer test must exercise `compute_risk_score()` with inputs where `total_deps != vulnerable_deps` to expose the operand swap:

- **Input**: `compute_risk_score(100, 5)` — 100 total dependencies, 5 vulnerable
- **Before fix (incorrect)**: Returns `100 / 5 = 20.0` — test should initially demonstrate this failure
- **After fix (correct)**: Returns `5 / 100 = 0.05` — test asserts this value

Follow the existing test pattern in `modules/risk/tests/score_test.rs`, which uses `assert_eq!` for score verification.

### Code fix
In `modules/risk/src/score.rs`, function `compute_risk_score()`:

- **Current (buggy)**: `total_deps as f64 / vulnerable_deps as f64`
- **Correct**: `vulnerable_deps as f64 / total_deps as f64`

Also consider adding a guard for `total_deps == 0` to prevent division by zero, returning `0.0` in that case.

### Data migration
Since `compute_risk_score()` output is persisted to the `assessments` table at ingestion time (written once by `create_assessment()` in `modules/risk/src/assessment.rs` via `diesel::insert_into(assessments::table)`), all existing records have incorrect `risk_score` values. The risk score is NOT recomputed on read — `get_assessment()` in `modules/risk/src/endpoints.rs` returns the persisted value directly.

The migration must recompute `risk_score` for all existing rows. The `assessments` table stores `sbom_id`, which can be used to join back to the source data and retrieve the correct `total_deps` and `vulnerable_deps` counts. The migration SQL should:

1. Join `assessments` with the SBOM dependency data to get the correct counts
2. Recompute `risk_score` as `vulnerable_deps::double precision / total_deps::double precision`
3. Update each row's `risk_score` column with the corrected value
4. Handle the `total_deps = 0` edge case (set `risk_score = 0.0`)

Follow the existing Diesel migration convention in the `migration/` directory:
- Directory naming: `YYYY-MM-DD-NNNNNN_description/` (e.g., `2026-08-24-000004_fix_risk_scores/`)
- Files: `up.sql` (forward migration) and `down.sql` (rollback)
- Reference existing migrations: `2024-01-15-000001_create_sboms/`, `2024-02-20-000002_create_assessments/`, `2024-03-10-000003_add_severity_column/`

### Key symbols and code paths
- `compute_risk_score()` in `modules/risk/src/score.rs` — the buggy function
- `create_assessment()` in `modules/risk/src/assessment.rs` — persists the result via `diesel::insert_into(assessments::table)`
- `get_assessment()` in `modules/risk/src/endpoints.rs` — reads persisted `risk_score` without recomputation
- `test_risk_score_all_vulnerable` in `modules/risk/tests/score_test.rs` — existing test (does not catch the bug due to equal inputs)

## Reuse Candidates
- `modules/risk/tests/score_test.rs::test_risk_score_all_vulnerable` — existing test pattern showing how to call `compute_risk_score()` and assert with `assert_eq!`; use as a template for the reproducer test
- `modules/risk/src/score.rs::compute_risk_score` — the function under test; the fix is a single-line operand swap

## Acceptance Criteria
- [ ] A reproducer test calls `compute_risk_score(100, 5)` and asserts the result is `0.05` (vulnerable / total); this test fails before the fix and passes after
- [ ] `compute_risk_score()` returns `vulnerable_deps / total_deps` (not the reverse)
- [ ] Division by zero is handled when `total_deps == 0` (returns `0.0`)
- [ ] Existing records in the `assessments` table with incorrect `risk_score` values are corrected by the data migration
- [ ] No regression in existing tests (`test_risk_score_all_vulnerable` continues to pass)

## Test Requirements
- [ ] Reproducer test: call `compute_risk_score(100, 5)` and assert result equals `0.05`; call `compute_risk_score(50, 10)` and assert result equals `0.2` — these cases expose the operand swap because `total != vulnerable`
- [ ] Edge case test: call `compute_risk_score(0, 0)` and verify no panic (division by zero guard returns `0.0`)
- [ ] Regression test: verify `compute_risk_score(10, 10)` still returns `1.0` (existing behavior preserved)

## Verification Commands
- `cargo test --package risk -- score` — run score-related tests, expect all to pass after fix
- `diesel migration run` — apply the data migration to correct existing records
- `diesel migration redo` — verify the migration is reversible

## Bug Context

- **Bug**: [ACME-520](https://mock-jira.example.com/browse/ACME-520)
- **Steps to Reproduce**: Ingest an SBOM with 100 total / 5 vulnerable dependencies, create a risk assessment, retrieve it via GET /api/v2/assessments/{id}, inspect the risk_score field
- **Expected Result**: Risk score is `5 / 100 = 0.05` (vulnerable / total)
- **Actual Result**: Risk score is `100 / 5 = 20.0` (total / vulnerable) -- numerator and denominator are swapped
- **Root Cause**: `compute_risk_score()` in `modules/risk/src/score.rs` divides `total_deps / vulnerable_deps` instead of `vulnerable_deps / total_deps`; the incorrect value is persisted to `assessments.risk_score` at ingestion time and never recomputed on read
