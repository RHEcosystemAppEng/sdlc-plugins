# Jira API Metadata

Parameters for `jira.create_issue`:

- **Project key**: ACME
- **Issue type**: Task
- **Labels**: ["ai-generated-jira"]

---

## Repository
acme-backend

## Target Branch
main

## Description
Fix the swapped division operands in `compute_risk_score()` that produce inflated risk scores, and add a data migration to correct existing assessment records that were persisted with incorrect values. Fixes ACME-520.

## Files to Modify
- `modules/risk/src/score.rs` -- fix the division order in `compute_risk_score()` from `total_deps / vulnerable_deps` to `vulnerable_deps / total_deps`

## Files to Create
- `migration/2024-XX-XX-000004_fix_risk_score_values/up.sql` -- data migration to correct existing `risk_score` values in the `assessments` table by computing the reciprocal (`1.0 / risk_score`) for all rows where `risk_score != 0`
- `migration/2024-XX-XX-000004_fix_risk_score_values/down.sql` -- reverse migration to restore the original (incorrect) values by computing the reciprocal again

## Implementation Notes
The root cause is in `modules/risk/src/score.rs`, function `compute_risk_score()`. The division operands are swapped: the function computes `total_deps as f64 / vulnerable_deps as f64` but should compute `vulnerable_deps as f64 / total_deps as f64`.

The incorrect score is persisted at ingestion time by `create_assessment()` in `modules/risk/src/assessment.rs`, which writes the result of `compute_risk_score()` to the `assessments.risk_score` column via Diesel `insert_into`. The GET endpoint in `modules/risk/src/endpoints.rs` reads the persisted value directly without recomputing, so fixing the function alone only corrects future assessments -- existing records retain the inflated score.

**Data migration**: Follow the existing Diesel migration convention in the `migration/` directory (format: `YYYY-MM-DD-NNNNNN_description/up.sql`). The most recent migration is `2024-03-10-000003_add_severity_column/`. The new migration should update all rows in the `assessments` table where `risk_score != 0` by setting `risk_score = 1.0 / risk_score` (the reciprocal reverses the swapped division). The `down.sql` applies the same reciprocal transformation to roll back.

**Reproducer test**: Use the existing test file at `modules/risk/tests/score_test.rs` and follow the pattern of the existing `test_risk_score_all_vulnerable` test. The existing test uses `compute_risk_score(10, 10)` which always returns `1.0` regardless of operand order. The reproducer must use unequal values (e.g., `compute_risk_score(100, 5)`) to expose the bug.

No `CONVENTIONS.md` was found in the repository root.

## Reuse Candidates
- `modules/risk/tests/score_test.rs::test_risk_score_all_vulnerable` -- existing test pattern to follow for the reproducer test; uses `compute_risk_score()` directly and asserts the returned score

## Acceptance Criteria
- [ ] A reproducer test calls `compute_risk_score(100, 5)` and asserts the result is `0.05` (this test fails before the fix and passes after)
- [ ] `compute_risk_score()` divides `vulnerable_deps / total_deps` (not the reverse)
- [ ] A data migration corrects existing `assessments.risk_score` values by computing the reciprocal for all non-zero rows
- [ ] No regression in existing tests (including `test_risk_score_all_vulnerable`)

## Test Requirements
- [ ] Reproducer test: `compute_risk_score(100, 5)` returns `0.05` (vulnerable / total). Before the fix, this returns `20.0` (total / vulnerable). After the fix, it returns `0.05`. Place this test in `modules/risk/tests/score_test.rs` alongside the existing test.
- [ ] Edge case test: `compute_risk_score(100, 0)` handles the zero-vulnerable-deps case without panicking (division by zero guard)
- [ ] Existing test `test_risk_score_all_vulnerable` continues to pass

## Verification Commands
- `cargo test -p risk` -- all risk module tests pass, including the new reproducer test
- `diesel migration run` -- data migration applies successfully
- `diesel migration redo` -- migration is reversible (down.sql then up.sql)

## Bug Context

- **Bug**: [ACME-520](https://mock-jira.example.com/browse/ACME-520)
- **Steps to Reproduce**: Ingest an SBOM with 100 total dependencies (5 vulnerable), create a risk assessment, retrieve it via `GET /api/v2/assessments/{id}`, and inspect the `risk_score` field.
- **Expected Result**: Risk score is `5 / 100 = 0.05` (vulnerable / total).
- **Actual Result**: Risk score is `100 / 5 = 20.0` (total / vulnerable). Numerator and denominator are swapped.
- **Root Cause**: `compute_risk_score()` in `modules/risk/src/score.rs` divides `total_deps / vulnerable_deps` instead of `vulnerable_deps / total_deps`, and the incorrect value is persisted to the `assessments.risk_score` column at ingestion time.
