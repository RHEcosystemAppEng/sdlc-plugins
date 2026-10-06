<!-- Jira API Metadata -->
<!-- jira.create_issue parameters: -->
<!-- project: ACME -->
<!-- issue_type: Task -->
<!-- labels: ["ai-generated-jira"] -->
<!-- summary: Fix reversed division operands in compute_risk_score and migrate existing data -->
<!-- link: ACME-NEW blocks ACME-520 (link_type: Blocks) -->

## Repository
acme-backend

## Target Branch
main

## Description
Fix the reversed division operands in `compute_risk_score()` that produce inflated risk scores for all assessments. The function currently computes `total_deps / vulnerable_deps` instead of `vulnerable_deps / total_deps`, yielding values like 20.0 instead of 0.05. Because the incorrect score is persisted to the `assessments` table at ingestion time and never recomputed on read, a data migration is also required to correct all existing records. Fixes ACME-520.

## Files to Modify
- `modules/risk/src/score.rs` -- swap the division operands in `compute_risk_score()` so it returns `vulnerable_deps as f64 / total_deps as f64`
- `modules/risk/tests/score_test.rs` -- add a reproducer test with asymmetric inputs to prevent regression

## Files to Create
- `migration/YYYY-MM-DD-000004_fix_risk_score_values/up.sql` -- data migration to recompute and correct `risk_score` for all existing rows in the `assessments` table
- `migration/YYYY-MM-DD-000004_fix_risk_score_values/down.sql` -- reversal migration (note: reverting to incorrect values is lossy; document this)

## Implementation Notes
The root cause is in `modules/risk/src/score.rs`, function `compute_risk_score()`:

```rust
// CURRENT (buggy): total_deps as f64 / vulnerable_deps as f64
// CORRECT:         vulnerable_deps as f64 / total_deps as f64
```

The function is called by `create_assessment()` in `modules/risk/src/assessment.rs`, which persists the result to `assessments.risk_score` via Diesel's `insert_into`. The read endpoint `get_assessment()` in `modules/risk/src/endpoints.rs` returns the persisted value directly -- it does NOT recompute the score.

**Reproducer test guidance**: The existing test in `modules/risk/tests/score_test.rs` uses equal inputs (`compute_risk_score(10, 10)`) which produce 1.0 regardless of operand order. The reproducer must use asymmetric inputs where `total_deps != vulnerable_deps` (e.g., `compute_risk_score(100, 5)`) to detect the swap. The test should assert `score == 0.05` (i.e., `5/100`), which fails before the fix (returns `20.0`) and passes after.

**Data migration**: Follow the existing Diesel migration convention in the `migration/` directory (format: `YYYY-MM-DD-NNNNNN_description/up.sql`). The most recent migration is `2024-03-10-000003_add_severity_column`. The new migration should:
1. Join `assessments` with `sboms` to access `total_deps` and `vulnerable_deps` source values.
2. Recompute `risk_score` as `vulnerable_deps::double precision / total_deps::double precision`.
3. Update all rows in the `assessments` table with the corrected values.
4. Handle the edge case where `total_deps = 0` to avoid division by zero (set `risk_score = 0` or `NULL`).

**Existing patterns**: The `assessment.rs` file uses Diesel ORM with `PgConnection`. The `score_test.rs` file uses standard `#[test]` annotations with `assert_eq!` assertions.

No CONVENTIONS.md was found in the repository.

## Reuse Candidates
- `modules/risk/src/score.rs::compute_risk_score` -- the function to fix; swap its operands
- `modules/risk/tests/score_test.rs` -- add the reproducer test alongside the existing `test_risk_score_all_vulnerable` test
- `modules/risk/src/assessment.rs::create_assessment` -- verify the caller correctly passes the fixed score (no change needed in the caller itself)

## Acceptance Criteria
- [ ] A reproducer test with asymmetric inputs (e.g., `total_deps=100, vulnerable_deps=5`) is added that asserts `risk_score == 0.05`; this test fails before the fix and passes after
- [ ] `compute_risk_score()` computes `vulnerable_deps / total_deps` (not `total_deps / vulnerable_deps`)
- [ ] A data migration corrects the `risk_score` column for all existing rows in the `assessments` table by recomputing the value with the correct formula
- [ ] The data migration handles edge cases (e.g., `total_deps = 0`) without causing division-by-zero errors
- [ ] No regression in existing tests (`test_risk_score_all_vulnerable` continues to pass)

## Test Requirements
- [ ] Reproducer unit test: call `compute_risk_score(100, 5)` and assert the result equals `0.05` (vulnerable / total). This test must fail before the code fix is applied and pass after. Place in `modules/risk/tests/score_test.rs` alongside the existing test.
- [ ] Additional edge case test: call `compute_risk_score(100, 0)` and verify it handles zero vulnerable dependencies gracefully (expected result: `0.0`)
- [ ] Additional edge case test: call `compute_risk_score(0, 0)` and verify it handles zero total dependencies without panicking (division by zero guard)
- [ ] Verify the data migration correctly updates existing assessment records by checking `risk_score` values before and after migration

## Verification Commands
- `cargo test --package risk` -- all unit tests pass, including the new reproducer test
- `diesel migration run` -- the data migration executes without errors
- `diesel migration redo` -- the migration can be reversed and re-applied cleanly

## Bug Context

- **Bug**: [ACME-520](https://mock-jira.example.com/browse/ACME-520)
- **Steps to Reproduce**: Ingest an SBOM with 100 total dependencies (5 vulnerable), create a risk assessment, retrieve it via `GET /api/v2/assessments/{id}`, and inspect the `risk_score` field.
- **Expected Result**: Risk score should be `5 / 100 = 0.05` (vulnerable / total).
- **Actual Result**: Risk score is `100 / 5 = 20.0` (total / vulnerable). Numerator and denominator are swapped.
- **Root Cause**: `compute_risk_score()` in `modules/risk/src/score.rs` divides `total_deps / vulnerable_deps` instead of `vulnerable_deps / total_deps`. The incorrect value is persisted to `assessments.risk_score` at ingestion time and never recomputed on read.
