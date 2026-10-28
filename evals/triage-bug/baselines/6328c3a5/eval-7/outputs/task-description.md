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
Fix the swapped division operands in `compute_risk_score()` that produce inflated risk scores, and add a data migration to correct existing persisted assessments. The function currently computes `total_deps / vulnerable_deps` instead of `vulnerable_deps / total_deps`, producing values that are the inverse of the intended risk score. Because the result is persisted to the `assessments.risk_score` column at ingestion time and never recomputed, all existing assessment records contain incorrect scores. Fixes ACME-520.

## Files to Modify
- `modules/risk/src/score.rs` -- swap the division operands in `compute_risk_score()` to compute `vulnerable_deps / total_deps`

## Files to Create
- `modules/risk/tests/score_test.rs` -- add reproducer test (file exists; add new test function)
- `migration/2024-XX-XX-000004_fix_risk_score_values/up.sql` -- data migration to recompute risk_score for all existing assessments
- `migration/2024-XX-XX-000004_fix_risk_score_values/down.sql` -- reversal migration (note: the original incorrect values cannot be precisely restored)

## Implementation Notes

### Reproducer test

Translate the Steps to Reproduce into a test that fails before the fix and passes after:

- **Triggering input**: Call `compute_risk_score(100, 5)` -- an SBOM with 100 total dependencies and 5 vulnerable ones.
- **Incorrect output (before fix)**: The function returns `20.0` (`100 / 5`). The reproducer should initially observe this value to confirm the bug.
- **Correct output (after fix)**: The function should return `0.05` (`5 / 100`). Assert `assert_eq!(compute_risk_score(100, 5), 0.05)`.
- **Existing test reference**: `modules/risk/tests/score_test.rs` contains `test_risk_score_all_vulnerable` which uses `compute_risk_score(10, 10)` and asserts `1.0`. Follow this assertion pattern for the new reproducer test.
- Additional edge case: consider adding a test for `compute_risk_score(200, 1)` to exercise extreme ratios.

### Code fix

In `modules/risk/src/score.rs`, function `compute_risk_score()`:

- Change `total_deps as f64 / vulnerable_deps as f64` to `vulnerable_deps as f64 / total_deps as f64`.
- Consider adding a guard for `total_deps == 0` to avoid division by zero.

### Data migration

Step 3's persistence-impact analysis found that `compute_risk_score()` output is persisted to the `assessments` table, `risk_score` column, at ingestion time via `create_assessment()` in `modules/risk/src/assessment.rs`. The score is never recomputed on read. Existing records contain the inverted value.

- **Table**: `assessments`
- **Column**: `risk_score`
- **Migration logic**: For each row where `risk_score > 0`, set `risk_score = 1.0 / risk_score`. This inverts the incorrectly-swapped ratio back to the correct value. (Since `total/vulnerable` was stored instead of `vulnerable/total`, the reciprocal restores the correct value.)
- **Migration file naming**: Follow the Diesel convention observed in the repository. Existing migrations use the pattern `YYYY-MM-DD-NNNNNN_description/up.sql`. The next sequential number is `000004`. Use a descriptive name such as `fix_risk_score_values`.
- **Example up.sql**:
  ```sql
  UPDATE assessments
  SET risk_score = 1.0 / risk_score
  WHERE risk_score > 0;
  ```
- **down.sql**: The same inversion operation reverses the migration:
  ```sql
  UPDATE assessments
  SET risk_score = 1.0 / risk_score
  WHERE risk_score > 0;
  ```

## Reuse Candidates
- `modules/risk/tests/score_test.rs::test_risk_score_all_vulnerable` -- existing test pattern to follow for the reproducer test assertion style
- `modules/risk/src/assessment.rs::create_assessment` -- reference for understanding the persistence path; the migration must correct the same column this function writes

## Acceptance Criteria
- [ ] A reproducer test calls `compute_risk_score()` with asymmetric inputs (e.g., total=100, vulnerable=5) and asserts the correct result (0.05); the test fails before the code fix and passes after
- [ ] `compute_risk_score()` returns `vulnerable_deps / total_deps` instead of `total_deps / vulnerable_deps`
- [ ] Existing records in the `assessments` table with incorrect `risk_score` values are corrected by the data migration
- [ ] No regression in existing tests (including `test_risk_score_all_vulnerable`)

## Test Requirements
- [ ] Reproducer test: `test_risk_score_asymmetric` calls `compute_risk_score(100, 5)` and asserts result equals `0.05` (not `20.0`). This test must fail on the current code and pass after the fix.
- [ ] Verify existing test `test_risk_score_all_vulnerable` (total=10, vulnerable=10, expected=1.0) continues to pass
- [ ] Edge case test: `compute_risk_score(200, 1)` returns `0.005`, confirming extreme ratios are handled correctly

## Verification Commands
- `cargo test -p risk` -- all risk module tests pass, including the new reproducer test
- `diesel migration run` -- the data migration executes without errors

## Bug Context

- **Bug**: [ACME-520](https://mock-jira.example.com/browse/ACME-520)
- **Steps to Reproduce**: Ingest an SBOM with 100 total dependencies (5 vulnerable), create a risk assessment, retrieve it via `GET /api/v2/assessments/{id}`, and inspect the `risk_score` field.
- **Expected Result**: Risk score is `5 / 100 = 0.05` (vulnerable / total).
- **Actual Result**: Risk score is `100 / 5 = 20.0` (total / vulnerable). Numerator and denominator are swapped.
- **Root Cause**: `compute_risk_score()` in `modules/risk/src/score.rs` divides `total_deps / vulnerable_deps` instead of `vulnerable_deps / total_deps`. The result is persisted to `assessments.risk_score` at ingestion time and never recomputed, so existing records contain inflated values.
