# Jira API Metadata (jira.create_issue parameters)

```
jira.create_issue(
  cloudId: "mock-cloud-id-for-eval",
  projectKey: "ACME",
  issueTypeName: "Task",
  summary: "Fix swapped operands in compute_risk_score and migrate persisted assessment risk scores (fixes ACME-520)",
  description: <task description body below>,
  additional_fields: {
    "labels": ["ai-generated-jira"],
    "components": [{"name": "risk-engine"}]
  }
)
```

| Parameter | Value |
|---|---|
| Project key | `ACME` |
| Issue type | `Task` |
| Labels | `ai-generated-jira` |
| Component | `risk-engine` |

Follow-up operations (simulated):

- **Step 5b link**: `jira.create_issue_link(link_type="Blocks", inward_issue_key=<created-task-key>, outward_issue_key="ACME-520")`. The Task blocks the Bug.
- **Step 5c digest**: re-fetch the created task, write its description to `/tmp/desc-<task-key>.txt`, run `python3 scripts/sha256-digest.py`, and post the standalone comment `[sdlc-workflow] Description digest: <tagged-digest>` (no footnote).

---

## Repository
acme-backend

## Target Branch
main

## Description
Fixes ACME-520. `compute_risk_score()` divides total dependencies by vulnerable dependencies
instead of vulnerable by total, so every risk score is the reciprocal of the correct value. For
example, an SBOM with 100 dependencies, 5 of them vulnerable, scores `20.0` instead of `0.05`.
The score is persisted to `assessments.risk_score` when an assessment is created and is never
recomputed. This task therefore fixes the calculation for future assessments **and** adds a data
migration that corrects scores already stored in the database.

## Files to Modify
- `modules/risk/src/score.rs`: swap the operands in `compute_risk_score` to `vulnerable_deps / total_deps` and guard `total_deps == 0`
- `modules/risk/tests/score_test.rs`: add the reproducer test and edge-case tests for `compute_risk_score`

## Files to Create
- `migration/<YYYY-MM-DD>-000004_fix_assessment_risk_score/up.sql`: data migration that corrects existing `assessments.risk_score` values written with the swapped formula
- `migration/<YYYY-MM-DD>-000004_fix_assessment_risk_score/down.sql`: reverses the correction (reciprocal again) where it can be reversed

## API Changes
- `GET /api/v2/assessments/{id}` — MODIFY: no schema change. The `risk_score` value becomes correct (`vulnerable / total`, range 0.0–1.0) for new assessments and, after the migration, for existing ones.

## Implementation Notes
Fixes ACME-520.

**Code fix: `modules/risk/src/score.rs::compute_risk_score`**
- Current (buggy): `total_deps as f64 / vulnerable_deps as f64`
- Correct: `vulnerable_deps as f64 / total_deps as f64`
- Add a guard. If `total_deps == 0`, return `0.0` instead of producing `NaN` or `inf`. Keep the
  signature `pub fn compute_risk_score(total_deps: u32, vulnerable_deps: u32) -> f64` unchanged
  so the only caller, `modules/risk/src/assessment.rs::create_assessment`, needs no change.

**Reproducer test guidance (from Steps to Reproduce and Expected vs Actual Result)**
- Trigger input: `total_deps = 100`, `vulnerable_deps = 5`, matching the bug's SBOM with 100 deps and 5 vulnerable.
- Before the fix (Actual Result): `compute_risk_score(100, 5)` returns `20.0`.
- After the fix (Expected Result): `compute_risk_score(100, 5)` returns `0.05`.
- Follow the existing pattern in `modules/risk/tests/score_test.rs`
  (`test_risk_score_all_vulnerable`: a plain `#[test]` calling `compute_risk_score` and asserting
  the result). Compare floats with a tolerance (for example `(score - 0.05).abs() < f64::EPSILON * 10.0`)
  rather than exact `assert_eq!`.
- Note that `test_risk_score_all_vulnerable` (10, 10 -> 1.0) cannot detect the bug because the
  inputs are symmetric. The new test must use `total != vulnerable`.

**Persistence impact and data migration**
- Persistence boundary: `modules/risk/src/assessment.rs::create_assessment` writes the score
  through `diesel::insert_into(assessments::table).values((... assessments::risk_score.eq(score) ...))`.
- Table/column: `assessments.risk_score` (`DOUBLE PRECISION`). It is written once at creation
  time (ingestion) and never recomputed. `modules/risk/src/endpoints.rs::get_assessment` returns
  the stored value directly.
- Existing migration convention (Diesel): `migration/YYYY-MM-DD-NNNNNN_description/{up.sql,down.sql}`.
  Existing entries go up to `2024-03-10-000003_add_severity_column`, so the new directory is
  `migration/<current-date>-000004_fix_assessment_risk_score/`. Use `diesel migration generate fix_assessment_risk_score`
  if the project uses the Diesel CLI, then renumber or rename to match the sequence.
- Migration logic: the `assessments` table does not store `total_deps` or `vulnerable_deps`. The
  bug is a pure operand swap, so the stored value is exactly the reciprocal of the correct one
  (`stored = total / vulnerable`, so `correct = 1 / stored`). Suggested `up.sql`:
  ```sql
  UPDATE assessments
  SET risk_score = CASE
      WHEN risk_score = 'Infinity'::float8 OR risk_score = 'NaN'::float8 THEN 0.0
      WHEN risk_score > 0 THEN 1.0 / risk_score
      ELSE risk_score
  END;
  ```
  `Infinity` means vulnerable = 0 (correct score 0.0). `NaN` means total = 0 and vulnerable = 0,
  and the new guard returns 0.0 for that case.
- If the SBOM dependency and vulnerability data reachable via `assessments.sbom_id` can reliably
  reproduce the counts used at creation, recomputing `vulnerable / total` from that source data
  is an acceptable, more robust alternative. Document the chosen approach in the migration.
- `down.sql`: apply the reciprocal again for finite values `> 0`. Add a comment that rows mapped
  from `Infinity`/`NaN` to `0.0` cannot be restored exactly.
- The migration must run only once. Diesel's migration tracking table enforces this. Do not make
  the logic re-runnable, because applying the reciprocal twice would bring back the wrong values.
- Deploy the code fix and the migration together in the same release. Otherwise, assessments
  created after the migration but before the code fix would be stored wrong again.

No `CONVENTIONS.md` exists in acme-backend. Follow the existing Diesel and test patterns above.

## Reuse Candidates
- `modules/risk/src/score.rs::compute_risk_score`: fix in place. It is the single source of the score calculation.
- `modules/risk/tests/score_test.rs::test_risk_score_all_vulnerable`: test structure to copy for the reproducer.
- `migration/2024-03-10-000003_add_severity_column/` (and the other entries under `migration/`): Diesel migration layout (`up.sql`/`down.sql`) to follow.

## Acceptance Criteria
- [ ] Reproducer test: `compute_risk_score(100, 5)` returns `0.05`. It fails before the fix (returns `20.0`) and passes after.
- [ ] `compute_risk_score` computes `vulnerable_deps / total_deps` and returns `0.0` when `total_deps == 0` (no `NaN` or `inf`).
- [ ] New assessments created through `create_assessment` persist the correct `risk_score`, and `GET /api/v2/assessments/{id}` returns it.
- [ ] Existing records in `assessments` with wrong persisted `risk_score` values are corrected by the data migration (for example, a stored `20.0` becomes `0.05`, and stored `Infinity`/`NaN` become `0.0`).
- [ ] The migration follows the Diesel convention `migration/YYYY-MM-DD-NNNNNN_description/{up.sql,down.sql}` and applies cleanly with `diesel migration run`.
- [ ] No regression in existing tests, including `test_risk_score_all_vulnerable`.

## Test Requirements
- [ ] Reproducer test in `modules/risk/tests/score_test.rs`: call `compute_risk_score(100, 5)` and assert the result is `0.05` (within a float tolerance). Before the fix this returns `20.0` (total / vulnerable), so the test fails. After the fix it passes.
- [ ] Edge case: `compute_risk_score(10, 0)` returns `0.0` (no vulnerable deps).
- [ ] Edge case: `compute_risk_score(0, 0)` returns `0.0` (empty SBOM, no division by zero).
- [ ] Keep `test_risk_score_all_vulnerable` (`10, 10` -> `1.0`) passing.
- [ ] Migration test (integration test or manual verification against a test database): seed `assessments` rows with `risk_score` values `20.0`, `'Infinity'`, and `'NaN'`, run the migration, and assert the values become `0.05`, `0.0`, and `0.0`.

## Verification Commands
- `cargo test -p risk` (or `cargo test --test score_test`): all score tests pass, including the new reproducer.
- `diesel migration run`: the new migration applies without error.
- `diesel migration redo`: down/up round-trip succeeds.
- `curl http://localhost:8080/api/v2/assessments/{id}` for an assessment created from an SBOM with 100 deps / 5 vulnerable: `risk_score` is `0.05`.

## Bug Context

- **Bug**: [ACME-520](https://mock-jira.example.com/browse/ACME-520)
- **Steps to Reproduce**: Ingest an SBOM with 100 total dependencies (5 vulnerable), create a risk assessment for it, retrieve it via `GET /api/v2/assessments/{id}`, and inspect `risk_score`.
- **Expected Result**: `risk_score` is `5 / 100 = 0.05` (vulnerable / total).
- **Actual Result**: `risk_score` is `100 / 5 = 20.0` (total / vulnerable). The numerator and denominator are swapped.
- **Root Cause**: `modules/risk/src/score.rs::compute_risk_score` has its division operands swapped (`total_deps / vulnerable_deps`). The result is persisted at creation time to `assessments.risk_score` by `create_assessment` and served unchanged by `get_assessment`, so existing assessments hold wrong scores and need a data migration in addition to the code fix.
