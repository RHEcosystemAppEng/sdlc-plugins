# Jira API Metadata

Parameters for `jira.create_issue`:

| Parameter | Value |
|-----------|-------|
| Project key | ACME |
| Issue type | Task |
| Labels | ai-generated-jira |

```
jira.create_issue(
  project_key: "ACME",
  issue_type: "Task",
  summary: "Fix swapped operands in compute_risk_score() and migrate existing assessment data",
  labels: ["ai-generated-jira"],
  description: <see below>
)
```

---

## Repository
acme-backend

## Target Branch
main

## Description
Fix the swapped division operands in `compute_risk_score()` that produce inflated risk scores (reciprocal of the correct value), and add a data migration to correct all existing assessment records that were persisted with the incorrect scores. Fixes ACME-520.

## Files to Modify
- `modules/risk/src/score.rs` -- swap the division operands in `compute_risk_score()` from `total_deps / vulnerable_deps` to `vulnerable_deps / total_deps`

## Files to Create
- `modules/risk/tests/score_test.rs` -- add reproducer test `test_risk_score_unequal_deps` (file exists; add new test function alongside existing `test_risk_score_all_vulnerable`)
- `migration/2026-10-15-000001_fix_risk_score_values/up.sql` -- data migration to correct existing assessments with inflated risk_score values
- `migration/2026-10-15-000001_fix_risk_score_values/down.sql` -- rollback migration

## Implementation Notes

### Code fix

In `modules/risk/src/score.rs`, function `compute_risk_score()`, change:

```rust
total_deps as f64 / vulnerable_deps as f64
```

to:

```rust
vulnerable_deps as f64 / total_deps as f64
```

This is the only code change required. The caller `create_assessment()` in `modules/risk/src/assessment.rs` passes the return value directly to `diesel::insert_into(assessments::table)`, so fixing the function corrects all future assessments.

### Reproducer test

Add a new test in `modules/risk/tests/score_test.rs` alongside the existing `test_risk_score_all_vulnerable` test. The reproducer must use unequal values for `total_deps` and `vulnerable_deps` to expose the operand swap:

```rust
#[test]
fn test_risk_score_unequal_deps() {
    // With 100 total deps and 5 vulnerable, score should be 5/100 = 0.05
    let score = compute_risk_score(100, 5);
    assert!((score - 0.05).abs() < f64::EPSILON,
        "Expected risk score 0.05, got {}", score);
}
```

This test fails before the fix (returns `20.0`) and passes after (returns `0.05`). The existing test `test_risk_score_all_vulnerable` uses equal values (`10, 10`), which produces `1.0` regardless of operand order and therefore cannot detect the bug.

### Data migration

The `risk_score` column in the `assessments` table stores the value computed at assessment creation time. It is NOT recomputed on read (`GET /api/v2/assessments/{id}` reads the persisted value directly from `modules/risk/src/endpoints.rs`). All existing assessments created while the bug was present have inflated scores.

Create a migration following the Diesel convention used by existing migrations in `migration/` (e.g., `2024-03-10-000003_add_severity_column/up.sql`):

**`migration/2026-10-15-000001_fix_risk_score_values/up.sql`**:

The migration should recompute `risk_score` for all existing assessments by joining on the `sboms` table to obtain the original `total_deps` and `vulnerable_deps` values, then applying the correct formula (`vulnerable_deps::double precision / total_deps::double precision`). A safe approach:

```sql
UPDATE assessments
SET risk_score = s.vulnerable_deps::double precision / s.total_deps::double precision
FROM sboms s
WHERE assessments.sbom_id = s.id
  AND s.total_deps > 0;
```

This recalculates from the source data rather than attempting to invert the existing values, which is more robust against edge cases (e.g., zero values or floating-point precision loss).

**`migration/2026-10-15-000001_fix_risk_score_values/down.sql`**:

The down migration is a no-op or a comment, since reverting to incorrect data is not desirable:

```sql
-- No rollback: reverting to incorrect risk_score values is not meaningful.
```

### Traceability

Fixes [ACME-520](https://mock-jira.example.com/browse/ACME-520).

## Reuse Candidates
- `modules/risk/tests/score_test.rs::test_risk_score_all_vulnerable` -- existing test pattern for `compute_risk_score()`, use as the model for the reproducer test structure and imports

## Acceptance Criteria
- [ ] A reproducer test (`test_risk_score_unequal_deps`) demonstrates the bug by calling `compute_risk_score()` with unequal values (e.g., total=100, vulnerable=5); it fails before the fix (returning 20.0) and passes after (returning 0.05)
- [ ] `compute_risk_score()` returns `vulnerable_deps / total_deps` instead of `total_deps / vulnerable_deps`
- [ ] A data migration corrects all existing `assessments.risk_score` values by recomputing from source data in the `sboms` table
- [ ] No regression in existing tests (including `test_risk_score_all_vulnerable`)

## Test Requirements
- [ ] Reproducer test: `test_risk_score_unequal_deps` in `modules/risk/tests/score_test.rs` -- calls `compute_risk_score(100, 5)` and asserts the result is approximately `0.05` (vulnerable / total), not `20.0` (total / vulnerable)
- [ ] Edge case test: `test_risk_score_zero_vulnerable` -- calls `compute_risk_score(100, 0)` and asserts the result is `0.0` (no vulnerable dependencies should produce a zero risk score)
- [ ] Existing test `test_risk_score_all_vulnerable` continues to pass with `compute_risk_score(10, 10)` returning `1.0`

## Verification Commands
- `cargo test -p risk` -- all tests in the risk module pass, including the new reproducer test
- `diesel migration run` -- the data migration applies successfully without errors

## Bug Context

- **Bug**: [ACME-520](https://mock-jira.example.com/browse/ACME-520)
- **Steps to Reproduce**: Ingest an SBOM with 100 total dependencies (5 vulnerable), create a risk assessment, retrieve via `GET /api/v2/assessments/{id}`, inspect the `risk_score` field
- **Expected Result**: Risk score should be `5 / 100 = 0.05` (vulnerable / total)
- **Actual Result**: Risk score is `100 / 5 = 20.0` (total / vulnerable) -- numerator and denominator are swapped
- **Root Cause**: `compute_risk_score()` in `modules/risk/src/score.rs` divides `total_deps / vulnerable_deps` instead of `vulnerable_deps / total_deps`, and the incorrect result is persisted to `assessments.risk_score` at ingestion time via `create_assessment()` in `modules/risk/src/assessment.rs`
