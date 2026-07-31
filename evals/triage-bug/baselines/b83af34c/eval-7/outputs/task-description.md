# Jira API Metadata

Parameters for `jira.create_issue`:

- **Project key**: ACME
- **Issue type**: Task
- **Labels**: ai-generated-jira

---

## Repository
acme-backend

## Target Branch
main

## Description
Fix the swapped division operands in `compute_risk_score()` that produce inflated risk scores for all assessments, and add a data migration to correct existing persisted values. The function currently computes `total_deps / vulnerable_deps` instead of `vulnerable_deps / total_deps`, and the incorrect result is persisted to the `assessments.risk_score` column at ingestion time. Fixes ACME-520.

## Files to Modify
- `modules/risk/src/score.rs` -- Fix the swapped operands in `compute_risk_score()`: change `total_deps as f64 / vulnerable_deps as f64` to `vulnerable_deps as f64 / total_deps as f64`

## Files to Create
- `modules/risk/tests/score_regression_test.rs` -- Reproducer test for ACME-520 that verifies correct risk score computation when total_deps != vulnerable_deps
- `migration/2026-07-31-000001_fix_risk_scores/up.sql` -- Data migration to recompute and correct existing assessments' risk_score values
- `migration/2026-07-31-000001_fix_risk_scores/down.sql` -- Rollback migration for the risk_score correction

## Implementation Notes

### Reproducer test (implement first)

Write a reproducer test in `modules/risk/tests/score_regression_test.rs` that validates the fix for ACME-520. The test should:

1. Call `compute_risk_score(100, 5)` -- an input where total_deps != vulnerable_deps, which exposes the swapped-operand bug.
2. Assert the result equals `0.05` (vulnerable / total = 5 / 100), not `20.0` (total / vulnerable = 100 / 5).
3. This test will fail before the fix (confirming the bug exists) and pass after the fix.

Follow the existing test pattern in `modules/risk/tests/score_test.rs`:
```rust
#[test]
fn test_risk_score_all_vulnerable() {
    let score = compute_risk_score(10, 10);
    assert_eq!(score, 1.0);
}
```

Additional test cases to include:
- `compute_risk_score(100, 0)` -- edge case: no vulnerable dependencies (handle division by zero)
- `compute_risk_score(0, 0)` -- edge case: no dependencies at all
- `compute_risk_score(50, 25)` -- verify result is `0.5`, not `2.0`

### Code fix

In `modules/risk/src/score.rs`, swap the operands in the `compute_risk_score()` function body:

- **Before (buggy)**: `total_deps as f64 / vulnerable_deps as f64`
- **After (correct)**: `vulnerable_deps as f64 / total_deps as f64`

### Data migration

A data migration is required because `risk_score` is persisted at ingestion time in `create_assessment()` (in `modules/risk/src/assessment.rs`) and is NOT recomputed on read. All existing assessments in the database contain incorrect (inflated) risk score values.

Create a migration following the existing Diesel convention in the `migration/` directory (pattern: `YYYY-MM-DD-NNNNNN_description/up.sql`). The last existing migration is `2024-03-10-000003_add_severity_column`.

**up.sql** -- Recompute and update existing `risk_score` values:
- The current (buggy) scores were computed as `total_deps / vulnerable_deps`.
- The correct scores should be `vulnerable_deps / total_deps`.
- To correct: for each assessment, the new risk_score = `1.0 / (old_risk_score * old_risk_score)` is NOT reliable due to floating-point precision. Instead, join the `assessments` table with the `sboms` table (via `sbom_id`) to retrieve the original `total_deps` and `vulnerable_deps` counts, then recompute: `UPDATE assessments SET risk_score = vulnerable_deps::double precision / total_deps::double precision FROM sboms WHERE assessments.sbom_id = sboms.id AND total_deps > 0`.
- Handle the edge case where `total_deps = 0` (set risk_score to 0 or NULL as appropriate).

**down.sql** -- Reverse the migration by restoring the old (buggy) values. Since the original values cannot be precisely recovered from the corrected ones, the down migration should recompute using the original (buggy) formula: `UPDATE assessments SET risk_score = total_deps::double precision / vulnerable_deps::double precision FROM sboms WHERE assessments.sbom_id = sboms.id AND vulnerable_deps > 0`.

## Reuse Candidates
- `modules/risk/tests/score_test.rs::test_risk_score_all_vulnerable` -- Existing test pattern for risk score assertions; follow this style for the reproducer test
- `modules/risk/src/assessment.rs::create_assessment` -- Caller of compute_risk_score; reference to understand the persistence path, no changes needed in this file

## Acceptance Criteria
- [ ] A reproducer test calls `compute_risk_score(100, 5)` and asserts the result is `0.05` (not `20.0`). The test fails before the fix and passes after.
- [ ] Existing assessments in the database with incorrect persisted `risk_score` values are corrected by the data migration (`migration/2026-07-31-000001_fix_risk_scores/up.sql`)
- [ ] `compute_risk_score()` returns `vulnerable_deps / total_deps` (correct formula) for all inputs
- [ ] The `GET /api/v2/assessments/{id}` endpoint returns the correct risk score for both new and previously-existing assessments
- [ ] No regression in existing tests (including `modules/risk/tests/score_test.rs::test_risk_score_all_vulnerable`)

## Test Requirements
- [ ] Reproducer test: `compute_risk_score(100, 5)` must return `0.05`. Before the fix, this will return `20.0` (confirming the bug). After the fix, it returns `0.05`. Place in `modules/risk/tests/score_regression_test.rs`.
- [ ] Edge case test: `compute_risk_score(100, 0)` must handle division by zero gracefully (no panic)
- [ ] Edge case test: `compute_risk_score(0, 0)` must handle zero-total-dependencies gracefully
- [ ] Asymmetry test: `compute_risk_score(50, 25)` must return `0.5`, not `2.0`
- [ ] Existing test `test_risk_score_all_vulnerable` must continue to pass (score of `1.0` for equal inputs)
- [ ] Migration test: verify that running `up.sql` against a database with pre-existing buggy assessments corrects the `risk_score` values

## Verification Commands
- `cargo test --package risk` -- Run all risk module tests, expected: all pass including the new reproducer test
- `diesel migration run` -- Apply the data migration to correct existing risk_score values

## Bug Context

- **Bug**: [ACME-520](https://mock-jira.example.com/browse/ACME-520)
- **Steps to Reproduce**: Ingest an SBOM with 100 total dependencies (5 vulnerable), create a risk assessment, retrieve it via `GET /api/v2/assessments/{id}`, and inspect the `risk_score` field.
- **Expected Result**: risk_score = 0.05 (vulnerable / total = 5 / 100)
- **Actual Result**: risk_score = 20.0 (total / vulnerable = 100 / 5) -- numerator and denominator are swapped
- **Root Cause**: The `compute_risk_score()` function in `modules/risk/src/score.rs` divides `total_deps / vulnerable_deps` instead of `vulnerable_deps / total_deps`. The incorrect result is persisted to the `assessments` table at ingestion time and is never recomputed, so all existing assessments contain inflated risk scores.
