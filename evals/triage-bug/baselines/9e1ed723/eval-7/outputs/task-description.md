# Jira API Metadata (simulated `jira.create_issue`)

```
jira.create_issue(
  cloudId: "mock-cloud-id-for-eval",
  projectKey: "ACME",
  issueTypeName: "Task",
  summary: "Fix swapped operands in compute_risk_score and migrate persisted risk scores (fixes ACME-520)",
  description: <task description body below>,
  additional_fields: {
    "labels": ["ai-generated-jira"]
  }
)
```

| Parameter | Value |
|---|---|
| Project key | `ACME` |
| Issue type | `Task` |
| Labels | `ai-generated-jira` |
| Summary | Fix swapped operands in compute_risk_score and migrate persisted risk scores (fixes ACME-520) |

Follow-up operations (simulated):
- **Step 5b link:** `jira.create_issue_link(link_type="Blocks", inward_issue_key=<created-task-key>, outward_issue_key="ACME-520")`. The Task blocks the Bug.
- **Step 5c digest:** re-fetch `<created-task-key>`, write its description to `/tmp/desc-<task-key>.txt`, run `python3 scripts/sha256-digest.py /tmp/desc-<task-key>.txt`, then post the standalone comment `[sdlc-workflow] Description digest: <tagged-digest>`, without the footnote.

---

## Repository
acme-backend

## Target Branch
main

## Description
Fixes ACME-520. `compute_risk_score()` divides total dependencies by vulnerable dependencies instead of the reverse. Every risk assessment therefore gets the reciprocal of its correct score: an SBOM with 100 dependencies, 5 of them vulnerable, gets 20.0 instead of 0.05. The score is persisted to `assessments.risk_score` when the assessment is created and is never recomputed. The fix has two parts:
1. Correct the formula, and guard the zero-denominator case, so new assessments are scored correctly.
2. Add a data migration that corrects the inverted `risk_score` values already stored in the `assessments` table.

## Files to Modify
- `modules/risk/src/score.rs`: swap the division operands in `compute_risk_score` to `vulnerable_deps / total_deps`, and return `0.0` when `total_deps == 0`
- `modules/risk/tests/score_test.rs`: add the reproducer test and edge-case tests for `compute_risk_score`

## Files to Create
- `migration/<YYYY-MM-DD>-000004_fix_inverted_risk_scores/up.sql`: data migration that corrects existing inverted `assessments.risk_score` values
- `migration/<YYYY-MM-DD>-000004_fix_inverted_risk_scores/down.sql`: reverse migration that restores the previous (inverted) values

(Use the date the migration is authored. This follows the Diesel convention `YYYY-MM-DD-NNNNNN_description/` used by `2024-01-15-000001_create_sboms`, `2024-02-20-000002_create_assessments` and `2024-03-10-000003_add_severity_column`.)

## Implementation Notes
Fixes ACME-520.

**Reproducer test (write first).** In `modules/risk/tests/score_test.rs`, follow the pattern of `test_risk_score_all_vulnerable`: a plain `#[test]` that calls `compute_risk_score` directly.
- Trigger scenario from the Steps to Reproduce: `total_deps = 100`, `vulnerable_deps = 5`.
- Before the fix, the function returns `20.0` (Actual Result: total / vulnerable). The test must fail against the current code.
- After the fix, the function must return `0.05` (Expected Result: vulnerable / total). Compare `f64` values with a tolerance, e.g. `assert!((score - 0.05).abs() < f64::EPSILON)`, rather than exact `assert_eq!`.
- The existing `test_risk_score_all_vulnerable` (`(10, 10)` returning `1.0`) cannot catch this bug because it gives the same result in either operand order. Keep it, since it still holds after the fix.

**Code fix.** In `modules/risk/src/score.rs::compute_risk_score(total_deps: u32, vulnerable_deps: u32) -> f64`:
- Change `total_deps as f64 / vulnerable_deps as f64` to `vulnerable_deps as f64 / total_deps as f64`.
- Return `0.0` when `total_deps == 0`, to avoid `NaN` from `0 / 0`.
- Keep the signature unchanged. The only caller, `modules/risk/src/assessment.rs::create_assessment`, passes `(total_deps, vulnerable_deps)` in the correct parameter order and does not need to change.

**Persistence impact / data migration.** The score is written at ingestion time by `modules/risk/src/assessment.rs::create_assessment` through `diesel::insert_into(assessments::table).values(assessments::risk_score.eq(score))`. It is read back unchanged by `modules/risk/src/endpoints.rs::get_assessment` (`GET /api/v2/assessments/{id}`). Existing rows will not correct themselves, so a data migration is required.
- Table/column: `assessments.risk_score` (`DOUBLE PRECISION`).
- The table does not store the original `total_deps` / `vulnerable_deps` inputs. Because the defect is a pure operand swap, every stored value is the exact reciprocal of the correct one, so recompute it as follows:
  - Finite, positive values: `risk_score = 1.0 / risk_score`. Values of `1.0` map to themselves.
  - `'Infinity'` (from `vulnerable_deps == 0`) and `'NaN'` (from `0 / 0`): `risk_score = 0.0`.
- Suggested `up.sql`:
  ```sql
  UPDATE assessments SET risk_score = 0.0
   WHERE risk_score = 'Infinity'::float8 OR risk_score = 'NaN'::float8;
  UPDATE assessments SET risk_score = 1.0 / risk_score
   WHERE risk_score > 0 AND risk_score <> 'Infinity'::float8 AND risk_score <> 'NaN'::float8;
  ```
  Note the ordering: both statements must target disjoint rows. Infinity/NaN rows set to `0.0` are excluded from the second statement by `risk_score > 0`. In PostgreSQL, `'NaN'` compares greater than every other value, which is why it is excluded explicitly.
- Suggested `down.sql`: apply the reciprocal again (`1.0 / risk_score`) to positive finite values. Restoring `0.0` rows to `Infinity` cannot be done exactly, because rows that were legitimately `0` cannot be told apart. Document this as a lossy rollback in a comment in `down.sql`.
- Make sure the migration runs once, after the code fix is deployed, as part of the standard Diesel migration run, so that no newly created correct rows are inverted. If deployment ordering cannot be guaranteed, restrict the `UPDATE` with `created_at < <fix-deploy-cutoff>`, or ship the migration and the code fix in the same release so they apply atomically.

**Conventions.** acme-backend has no `CONVENTIONS.md`. Follow the existing Diesel migration layout under `migration/` and the test style in `modules/risk/tests/score_test.rs`.

## Reuse Candidates
- `modules/risk/src/score.rs::compute_risk_score`: fix in place. No new scoring helper is needed.
- `modules/risk/tests/score_test.rs::test_risk_score_all_vulnerable`: template for the new unit tests.
- `migration/2024-03-10-000003_add_severity_column/`: the most recent migration. Use its `up.sql`/`down.sql` layout as the pattern for the new data migration.

## Acceptance Criteria
- [ ] A reproducer test asserting `compute_risk_score(100, 5)` returns `0.05` exists in `modules/risk/tests/score_test.rs`. It fails before the fix, returning `20.0`, and passes after the fix.
- [ ] `compute_risk_score` computes `vulnerable_deps / total_deps`
- [ ] `compute_risk_score` returns `0.0` when `total_deps == 0` (no `NaN`) and `0.0` when `vulnerable_deps == 0` (no `Infinity`)
- [ ] New assessments created via `create_assessment` persist the correct `risk_score`, and `GET /api/v2/assessments/{id}` returns it, e.g. `0.05` for 100 total / 5 vulnerable
- [ ] Existing records in `assessments` with incorrect, inverted `risk_score` values are corrected by the data migration: finite positive values become their reciprocal, and `Infinity`/`NaN` values become `0.0`
- [ ] The migration follows the Diesel `migration/YYYY-MM-DD-NNNNNN_description/{up,down}.sql` convention and applies cleanly
- [ ] No regression in existing tests, including `test_risk_score_all_vulnerable`

## Test Requirements
- [ ] Reproducer: `compute_risk_score(100, 5)` asserts a result of `0.05` within an `f64` tolerance. This test must fail against the current code (which returns `20.0`) and pass after the fix.
- [ ] Edge case: `compute_risk_score(100, 0)` returns `0.0`
- [ ] Edge case: `compute_risk_score(0, 0)` returns `0.0`
- [ ] Existing: `compute_risk_score(10, 10)` still returns `1.0`
- [ ] Migration test: seed `assessments` rows with `risk_score` values `20.0`, `1.0`, `'Infinity'` and `'NaN'`, run the migration, and assert the results are `0.05`, `1.0`, `0.0` and `0.0`

## Verification Commands
- `cargo test -p risk score_test`: all score tests pass, including the reproducer
- `diesel migration run` followed by `diesel migration redo`: the migration applies and reverts without errors
- `curl -s http://localhost:8080/api/v2/assessments/{id} | jq .risk_score`: returns `0.05` for an assessment of an SBOM with 100 dependencies, 5 of them vulnerable

## Bug Context

- **Bug**: [ACME-520](https://mock-jira.example.com/browse/ACME-520)
- **Steps to Reproduce**: Ingest an SBOM with 100 total dependencies, 5 of which are vulnerable. Create a risk assessment for it, retrieve it via `GET /api/v2/assessments/{id}`, and inspect `risk_score`.
- **Expected Result**: `risk_score` is `5 / 100 = 0.05` (vulnerable / total).
- **Actual Result**: `risk_score` is `100 / 5 = 20.0` (total / vulnerable). The numerator and denominator are swapped.
- **Root Cause**: `modules/risk/src/score.rs::compute_risk_score` has its division operands swapped (`total_deps / vulnerable_deps`) and no zero-denominator guard. `create_assessment` persists the result to `assessments.risk_score` at ingestion time, and `get_assessment` serves it without recomputing. Existing rows therefore need a data migration in addition to the code fix.
