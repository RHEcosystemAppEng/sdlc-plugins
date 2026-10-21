# Jira API Metadata

```
jira.create_issue(
  project_key: "ACME",
  issue_type: "Task",
  labels: ["ai-generated-jira"],
  summary: "Fix swapped numerator/denominator in compute_risk_score() and migrate existing assessments"
)
```

- **Project key**: ACME
- **Issue type**: Task
- **Labels**: ai-generated-jira

---

## Repository
acme-backend

## Target Branch
main

## Description
Fix the swapped division operands in `compute_risk_score()` which produces inflated risk scores (total/vulnerable instead of vulnerable/total), and create a data migration to correct all existing assessment records that were persisted with incorrect values. Fixes ACME-520.

## Files to Modify
- `modules/risk/src/score.rs` -- fix the division in `compute_risk_score()` to use `vulnerable_deps / total_deps` instead of `total_deps / vulnerable_deps`
- `modules/risk/tests/score_test.rs` -- add reproducer test with asymmetric inputs that fails before the fix and passes after

## Files to Create
- `migration/YYYY-MM-DD-000004_fix_risk_score_values/up.sql` -- data migration to correct existing `risk_score` values in the `assessments` table
- `migration/YYYY-MM-DD-000004_fix_risk_score_values/down.sql` -- rollback migration to reverse the correction

## Implementation Notes
The root cause is in `modules/risk/src/score.rs`, function `compute_risk_score()`. The current implementation is:

```rust
total_deps as f64 / vulnerable_deps as f64
```

This must be changed to:

```rust
vulnerable_deps as f64 / total_deps as f64
```

**Reproducer test guidance**: The existing test `test_risk_score_all_vulnerable` in `modules/risk/tests/score_test.rs` uses equal inputs (10, 10) which masks the bug. The reproducer test must use asymmetric inputs where `total != vulnerable` to expose the swapped operands. For example, `compute_risk_score(100, 5)` should return `0.05`, not `20.0`. Follow the existing test pattern in `modules/risk/tests/score_test.rs`.

**Data migration**: Because `compute_risk_score()` output is persisted to the `assessments` table, `risk_score` column via `create_assessment()` in `modules/risk/src/assessment.rs` at ingestion time (not recomputed on read), all existing assessment records contain incorrect inflated values. The migration must correct these values.

The migration SQL should join the `assessments` table with the `sboms` table to recompute the score from source data:

```sql
UPDATE assessments a
SET risk_score = s.vulnerable_deps::double precision / s.total_deps::double precision
FROM sboms s
WHERE a.sbom_id = s.id
  AND s.total_deps > 0;
```

Follow the existing Diesel migration convention in the `migration/` directory: `YYYY-MM-DD-NNNNNN_description/up.sql` (see existing migrations `2024-01-15-000001_create_sboms`, `2024-02-20-000002_create_assessments`, `2024-03-10-000003_add_severity_column` for the pattern).

Fixes ACME-520.

## Acceptance Criteria
- [ ] A reproducer test exists that calls `compute_risk_score()` with asymmetric inputs (e.g., total=100, vulnerable=5), asserts the result is `0.05` (vulnerable/total), and would fail with the original swapped formula
- [ ] Existing assessments with incorrect persisted `risk_score` values are corrected by the data migration
- [ ] `compute_risk_score()` returns `vulnerable_deps / total_deps` (not the inverse) for all inputs
- [ ] The `GET /api/v2/assessments/{id}` endpoint returns correct risk scores for both newly created and migrated assessments
- [ ] No regression in existing tests (including `test_risk_score_all_vulnerable`)

## Test Requirements
- [ ] Reproducer test: call `compute_risk_score(100, 5)` and assert the result equals `0.05`; this test must fail before the fix (returning `20.0`) and pass after (returning `0.05`)
- [ ] Edge case test: call `compute_risk_score(10, 0)` and verify graceful handling of zero vulnerable dependencies (no division by zero)
- [ ] Identity case: confirm `compute_risk_score(10, 10)` still returns `1.0`

## Verification Commands
- `cargo test --package risk` -- all risk module tests pass, including the new reproducer test
- `diesel migration run` -- data migration executes successfully against the database

## Bug Context

- **Bug**: [ACME-520](https://mock-jira.example.com/browse/ACME-520)
- **Steps to Reproduce**: Ingest an SBOM with 100 total dependencies (5 vulnerable), create a risk assessment, retrieve it via GET /api/v2/assessments/{id}, and inspect the risk_score field.
- **Expected Result**: Risk score should be 5 / 100 = 0.05 (vulnerable / total).
- **Actual Result**: Risk score is 100 / 5 = 20.0 (total / vulnerable). Numerator and denominator are swapped.
- **Root Cause**: `compute_risk_score()` in `modules/risk/src/score.rs` divides `total_deps / vulnerable_deps` instead of `vulnerable_deps / total_deps`, producing inflated reciprocal values. The incorrect scores are persisted to the `assessments` table at ingestion time and never recomputed, requiring a data migration to correct existing records.
