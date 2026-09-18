# Jira API Metadata

```
jira.create_issue(
  project_key: "ACME",
  issue_type: "Task",
  labels: ["ai-generated-jira"],
  summary: "Fix swapped risk score division and migrate existing assessments"
)
```

| Parameter     | Value                                                       |
|---------------|-------------------------------------------------------------|
| Project key   | ACME                                                        |
| Issue type    | Task                                                        |
| Labels        | ai-generated-jira                                           |
| Summary       | Fix swapped risk score division and migrate existing assessments |
| Link          | Blocks ACME-520                                             |

---

## Repository
acme-backend

## Target Branch
main

## Description
Fix the swapped numerator/denominator in `compute_risk_score()` that produces inflated risk scores for all assessments, and add a data migration to correct the incorrect values already persisted in the `assessments` table. Fixes ACME-520.

The `compute_risk_score()` function divides `total_deps / vulnerable_deps` instead of `vulnerable_deps / total_deps`, producing scores that are the reciprocal of the correct value (e.g., 20.0 instead of 0.05 for 5 vulnerable out of 100 total dependencies). Because the score is persisted at ingestion time in `create_assessment()` and never recomputed on read, all existing assessment records in the database contain incorrect values.

## Files to Modify
- `modules/risk/src/score.rs` -- fix the swapped division operands in `compute_risk_score()`
- `modules/risk/tests/score_test.rs` -- add reproducer test with asymmetric inputs

## Files to Create
- `migration/YYYY-MM-DD-000004_fix_risk_scores/up.sql` -- data migration to correct existing `assessments.risk_score` values using the correct formula
- `migration/YYYY-MM-DD-000004_fix_risk_scores/down.sql` -- reverse migration to restore previous (incorrect) values if needed

Follow the existing Diesel migration naming convention: `YYYY-MM-DD-NNNNNN_description/up.sql`. Existing migrations are in the `migration/` directory with sequential numbering (000001, 000002, 000003), so use 000004 as the next sequence number. Use the current date for the date prefix.

## Implementation Notes
### Code fix
In `modules/risk/src/score.rs`, swap the division operands in `compute_risk_score()`:

**Current (buggy):**
```rust
total_deps as f64 / vulnerable_deps as f64
```

**Correct:**
```rust
vulnerable_deps as f64 / total_deps as f64
```

Also add a zero-divisor guard: if `total_deps == 0`, return `0.0` to avoid division by zero.

### Data migration
Create a SQL migration in `migration/YYYY-MM-DD-000004_fix_risk_scores/up.sql` that recalculates the `risk_score` for all existing rows in the `assessments` table. The migration should join against the `sboms` table (linked via `assessments.sbom_id`) to retrieve the original `total_deps` and `vulnerable_deps` values, then recompute the score using the corrected formula (`vulnerable_deps::double precision / total_deps::double precision`).

If the sboms table contains the dependency counts, the migration query should be:
```sql
UPDATE assessments
SET risk_score = s.vulnerable_deps::double precision / s.total_deps::double precision
FROM sboms s
WHERE assessments.sbom_id = s.id
  AND s.total_deps > 0;
```

The `down.sql` should reverse the migration by restoring the original (incorrect) formula:
```sql
UPDATE assessments
SET risk_score = s.total_deps::double precision / s.vulnerable_deps::double precision
FROM sboms s
WHERE assessments.sbom_id = s.id
  AND s.vulnerable_deps > 0;
```

Follow the pattern established by existing migrations in the `migration/` directory (Diesel convention with `up.sql` and `down.sql`).

### Reproducer test
Add a test in `modules/risk/tests/score_test.rs` following the pattern of the existing `test_risk_score_all_vulnerable` test. The reproducer must use asymmetric inputs where `total_deps != vulnerable_deps` to expose the operand swap:

- Input: `total_deps = 100`, `vulnerable_deps = 5`
- Expected output: `0.05` (vulnerable / total)
- Bug behavior: `20.0` (total / vulnerable)

The existing test (`test_risk_score_all_vulnerable`) uses symmetric inputs (10, 10) that produce 1.0 regardless of operand order, which is why it did not catch this bug.

### Reference
- Buggy function: `modules/risk/src/score.rs::compute_risk_score()`
- Caller persisting result: `modules/risk/src/assessment.rs::create_assessment()`
- Query endpoint (reads persisted value): `modules/risk/src/endpoints.rs::get_assessment()`
- Database table: `assessments`, column: `risk_score` (DOUBLE PRECISION)
- Existing test file: `modules/risk/tests/score_test.rs`

## Acceptance Criteria
- [ ] A reproducer test with asymmetric inputs (e.g., total=100, vulnerable=5) is added that asserts `compute_risk_score(100, 5) == 0.05`; this test fails before the fix and passes after
- [ ] `compute_risk_score()` is fixed to divide `vulnerable_deps` by `total_deps` (not the reverse)
- [ ] A zero-divisor guard is added for the case where `total_deps == 0`
- [ ] A data migration is created that corrects all existing `assessments.risk_score` values by recomputing them with the correct formula
- [ ] The data migration follows the existing Diesel migration convention in the `migration/` directory
- [ ] Existing tests continue to pass (including `test_risk_score_all_vulnerable`)

## Test Requirements
- [ ] Reproducer test: `test_risk_score_asymmetric` (or similar) in `modules/risk/tests/score_test.rs` -- calls `compute_risk_score(100, 5)` and asserts the result is `0.05` (not `20.0`). This test must fail before the code fix and pass after.
- [ ] Zero-divisor test: `test_risk_score_zero_total` -- calls `compute_risk_score(0, 0)` and asserts the result is `0.0` (no panic or infinity)
- [ ] Existing test `test_risk_score_all_vulnerable` continues to pass with score `1.0` for inputs (10, 10)
- [ ] Integration test (if feasible): create an assessment via `create_assessment()` with known inputs and verify the persisted `risk_score` value is correct

## Bug Context

- **Bug**: [ACME-520](https://mock-jira.example.com/browse/ACME-520)
- **Steps to Reproduce**: Ingest an SBOM with 100 total dependencies (5 vulnerable), create a risk assessment, retrieve it via `GET /api/v2/assessments/{id}`, and inspect the `risk_score` field.
- **Expected Result**: Risk score should be `5 / 100 = 0.05` (vulnerable / total).
- **Actual Result**: Risk score is `100 / 5 = 20.0` (total / vulnerable). Numerator and denominator are swapped.
- **Root Cause**: `compute_risk_score()` in `modules/risk/src/score.rs` divides `total_deps` by `vulnerable_deps` instead of `vulnerable_deps` by `total_deps`. The score is persisted at ingestion time in `create_assessment()` and never recomputed, so all existing assessment records contain incorrect values.
