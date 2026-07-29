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
Fix the swapped division operands in `compute_risk_score()` that produce inflated risk scores, and create a data migration to correct existing `risk_score` values persisted in the `assessments` table. Fixes ACME-520.

## Files to Modify
- `modules/risk/src/score.rs` -- fix the division in `compute_risk_score()` to use `vulnerable_deps / total_deps` instead of `total_deps / vulnerable_deps`

## Files to Create
- `modules/risk/tests/score_test.rs` -- add reproducer test (or extend the existing test file) with a case where `total_deps != vulnerable_deps`
- `migration/2026-07-29-000004_fix_risk_score_values/up.sql` -- Diesel migration to correct existing `risk_score` values in the `assessments` table
- `migration/2026-07-29-000004_fix_risk_score_values/down.sql` -- reverse migration (restore original values if needed)

## Implementation Notes
The bug is in `modules/risk/src/score.rs`, function `compute_risk_score()`. The current implementation:

```rust
pub fn compute_risk_score(total_deps: u32, vulnerable_deps: u32) -> f64 {
    total_deps as f64 / vulnerable_deps as f64
}
```

Must be changed to:

```rust
pub fn compute_risk_score(total_deps: u32, vulnerable_deps: u32) -> f64 {
    vulnerable_deps as f64 / total_deps as f64
}
```

### Reproducer test guidance

The existing test in `modules/risk/tests/score_test.rs` uses `compute_risk_score(10, 10)` which returns `1.0` regardless of operand order, so it does not catch the bug. The reproducer test must use unequal values:

- Input: `compute_risk_score(100, 5)`
- Before fix (fails): returns `20.0` (total / vulnerable)
- After fix (passes): returns `0.05` (vulnerable / total)

Follow the existing test pattern in `modules/risk/tests/score_test.rs` for assertion style.

### Data migration

The incorrect `risk_score` values are persisted in the `assessments` table, `risk_score` column (type `DOUBLE PRECISION`), written at ingestion time by `create_assessment()` in `modules/risk/src/assessment.rs` via `diesel::insert_into(assessments::table)`. The GET endpoint reads these values directly and does not recompute them.

The migration file must follow the Diesel convention used in the existing `migration/` directory (format: `YYYY-MM-DD-NNNNNN_description/up.sql`). Existing migrations for reference:
- `migration/2024-01-15-000001_create_sboms/`
- `migration/2024-02-20-000002_create_assessments/`
- `migration/2024-03-10-000003_add_severity_column/`

The `up.sql` migration should correct existing `risk_score` values by joining the `assessments` table with the `sboms` table to access the original `total_deps` and `vulnerable_deps` source data and recompute the score as `vulnerable_deps::double precision / total_deps::double precision`. If direct source columns are not available on the `sboms` table, an alternative approach is to take the reciprocal: `UPDATE assessments SET risk_score = 1.0 / risk_score WHERE risk_score > 0`. The `down.sql` should reverse the migration by applying the inverse transformation.

Fixes ACME-520.

## Acceptance Criteria
- [ ] Reproducer test: a test calling `compute_risk_score()` with `total_deps != vulnerable_deps` (e.g., `compute_risk_score(100, 5)`) asserts the result is `0.05` -- fails before fix, passes after
- [ ] The division in `compute_risk_score()` is corrected to `vulnerable_deps / total_deps`
- [ ] Existing `risk_score` records in the `assessments` table are corrected by the data migration
- [ ] No regression in existing tests (including `test_risk_score_all_vulnerable`)

## Test Requirements
- [ ] Reproducer test: `test_risk_score_partial_vulnerable` -- call `compute_risk_score(100, 5)`, assert result equals `0.05` (vulnerable / total). This test must fail on the current code and pass after the fix.
- [ ] Edge case test: `test_risk_score_zero_vulnerable` -- call `compute_risk_score(100, 0)`, verify behavior when no dependencies are vulnerable (handle division by zero if applicable)
- [ ] Existing test `test_risk_score_all_vulnerable` continues to pass after the fix

## Verification Commands
- `cargo test -p risk` -- all risk module tests pass, including the new reproducer test
- `diesel migration run` -- migration applies without errors
- `diesel migration redo` -- migration is reversible

## Bug Context

- **Bug**: [ACME-520](https://mock-jira.example.com/browse/ACME-520)
- **Steps to Reproduce**: Ingest an SBOM with 100 total deps (5 vulnerable), create a risk assessment, retrieve via `GET /api/v2/assessments/{id}`, inspect `risk_score`
- **Expected Result**: Risk score is `5 / 100 = 0.05` (vulnerable / total)
- **Actual Result**: Risk score is `100 / 5 = 20.0` (total / vulnerable) -- numerator and denominator are swapped
- **Root Cause**: `compute_risk_score()` in `modules/risk/src/score.rs` divides `total_deps / vulnerable_deps` instead of `vulnerable_deps / total_deps`. The incorrect value is persisted to `assessments.risk_score` at ingestion time and never recomputed.
