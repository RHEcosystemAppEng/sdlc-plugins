<!-- Jira API metadata block: parameters for jira.create_issue -->
<!--
  project: ACME
  issuetype: Task
  labels: ["ai-generated-jira"]
  summary: "Fix risk score computation and migrate existing incorrect assessments"
-->

## Repository
acme-backend

## Target Branch
main

## Description
Fix the swapped division operands in `compute_risk_score()` that produce inflated risk scores, and create a data migration to correct all existing assessments that have incorrect persisted values. Fixes ACME-520.

## Files to Modify
- `modules/risk/src/score.rs` -- swap division operands in `compute_risk_score()` from `total_deps / vulnerable_deps` to `vulnerable_deps / total_deps`

## Files to Create
- `migration/2024-XX-XX-000004_fix_risk_scores/up.sql` -- data migration to recompute `risk_score` for all existing assessments using the correct formula (`vulnerable_deps / total_deps`); follow the Diesel migration naming convention established by existing migrations (e.g., `2024-03-10-000003_add_severity_column/`)
- `migration/2024-XX-XX-000004_fix_risk_scores/down.sql` -- reverse migration (revert scores to the old incorrect formula, or no-op if irreversible)

## Implementation Notes
The bug is in `modules/risk/src/score.rs`, in the `compute_risk_score()` function. The current implementation:

```rust
pub fn compute_risk_score(total_deps: u32, vulnerable_deps: u32) -> f64 {
    total_deps as f64 / vulnerable_deps as f64  // BUG: operands are swapped
}
```

Must be changed to:

```rust
pub fn compute_risk_score(total_deps: u32, vulnerable_deps: u32) -> f64 {
    vulnerable_deps as f64 / total_deps as f64  // CORRECT: vulnerable / total
}
```

**Persistence impact**: The incorrect scores are persisted to the `assessments` table, `risk_score` column, at ingestion time by `create_assessment()` in `modules/risk/src/assessment.rs`. The `GET /api/v2/assessments/{id}` endpoint in `modules/risk/src/endpoints.rs` reads the persisted value directly -- it does not recompute. Fixing the code alone only corrects future assessments; existing records retain the wrong score.

**Data migration**: Create a Diesel migration in the `migration/` directory following the existing naming convention (`YYYY-MM-DD-NNNNNN_description/{up.sql,down.sql}`). The `up.sql` should recompute `risk_score` for all existing assessments by joining against the source SBOM data to obtain `total_deps` and `vulnerable_deps`, then updating the column with the correct ratio (`vulnerable_deps::double precision / total_deps::double precision`). Ensure the migration handles the edge case where `total_deps = 0` to avoid division by zero.

**Reproducer test guidance**: Add a test in `modules/risk/tests/score_test.rs` alongside the existing `test_risk_score_all_vulnerable` test. Use unequal values for `total_deps` and `vulnerable_deps` (e.g., `compute_risk_score(100, 5)`). Before the fix, this returns `20.0` (total / vulnerable). After the fix, this should return `0.05` (vulnerable / total). The existing test with equal values (10, 10) passes regardless of operand order and does not catch the bug.

**Existing test patterns**: The existing test in `modules/risk/tests/score_test.rs` uses `assert_eq!` for exact floating-point comparison. Follow the same pattern for the reproducer test. Consider using `assert!((score - expected).abs() < f64::EPSILON)` for floating-point tolerance if needed.

## Reuse Candidates
- `modules/risk/tests/score_test.rs::test_risk_score_all_vulnerable` -- existing test structure and assertion pattern for `compute_risk_score()`; add the reproducer test in this file
- `migration/2024-03-10-000003_add_severity_column/` -- latest Diesel migration; use as a template for the migration file naming and structure

## Acceptance Criteria
- [ ] Reproducer test: a test calling `compute_risk_score(100, 5)` asserts the result is `0.05` (fails before the fix returning `20.0`, passes after the fix)
- [ ] `compute_risk_score()` correctly computes `vulnerable_deps / total_deps` instead of `total_deps / vulnerable_deps`
- [ ] Data migration corrects the `risk_score` column for all existing records in the `assessments` table by recomputing with the correct formula
- [ ] No regression in existing tests (including `test_risk_score_all_vulnerable`)

## Test Requirements
- [ ] Reproducer test: add a test in `modules/risk/tests/score_test.rs` that calls `compute_risk_score(100, 5)` and asserts the result is `0.05`; this test should fail before the fix (returns `20.0`) and pass after the fix (returns `0.05`)
- [ ] Test that `compute_risk_score(10, 10)` continues to return `1.0` (no regression on existing test case)
- [ ] Test that `compute_risk_score(50, 0)` handles the zero-vulnerable-deps edge case without panicking (division by zero was possible with the old formula when `vulnerable_deps = 0`)
- [ ] Test that the data migration SQL executes without errors and correctly updates existing assessment records

## Verification Commands
- `cargo test --package risk` -- run risk module tests including the new reproducer test
- `diesel migration run` -- apply the data migration and verify it completes without errors

## Bug Context

- **Bug**: [ACME-520](https://mock-jira.example.com/browse/ACME-520)
- **Steps to Reproduce**: Ingest an SBOM with 100 total dependencies (5 vulnerable), create a risk assessment, retrieve it via `GET /api/v2/assessments/{id}`, and inspect the `risk_score` field.
- **Expected Result**: The risk score should be `5 / 100 = 0.05` (vulnerable / total).
- **Actual Result**: The risk score is `100 / 5 = 20.0` (total / vulnerable). The numerator and denominator are swapped.
- **Root Cause**: `compute_risk_score()` in `modules/risk/src/score.rs` divides `total_deps / vulnerable_deps` instead of `vulnerable_deps / total_deps`. The incorrect value is persisted to the `assessments` table at ingestion time, so existing records retain the wrong score even after the code is fixed.
