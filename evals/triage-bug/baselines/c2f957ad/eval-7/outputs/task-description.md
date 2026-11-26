# Jira API Metadata (jira.create_issue parameters)

```
jira.create_issue(
  cloudId:        "mock-cloud-id-for-eval",
  projectKey:     "ACME",
  issueTypeName:  "Task",
  summary:        "Fix swapped operands in compute_risk_score and migrate persisted risk scores (ACME-520)",
  description:    <task description body below, markdown>,
  additional_fields: {
    "labels": ["ai-generated-jira"]
  }
)
```

Follow-up operations (simulated):

- Step 5b: `jira.create_issue_link(link_type="Blocks", inward_issue_key=<created-task-key>, outward_issue_key="ACME-520")` — the Task blocks the Bug.
- Step 5c: re-fetch the created task, run `python3 scripts/sha256-digest.py` on its description, and post the standalone comment `[sdlc-workflow] Description digest: <tagged-digest>` (no footnote).

---

## Repository
acme-backend

## Target Branch
main

## Description
Fixes ACME-520. `compute_risk_score()` divides total dependencies by vulnerable
dependencies instead of vulnerable by total, so every risk assessment gets an
inverted, inflated `risk_score` (e.g. `20.0` instead of `0.05` for 5 vulnerable out
of 100). The score is written to `assessments.risk_score` once, when the assessment
is created, and `GET /api/v2/assessments/{id}` returns that stored value without
recomputing it. This task fixes the calculation for new assessments and adds a data
migration that corrects the scores already stored in the database.

## Files to Modify
- `modules/risk/src/score.rs` — swap the division operands in `compute_risk_score` and guard against a zero `total_deps`
- `modules/risk/tests/score_test.rs` — add the reproducer test and edge-case tests

## Files to Create
- `migration/<YYYY-MM-DD>-000004_fix_inverted_risk_scores/up.sql` — data migration that corrects existing `assessments.risk_score` values
- `migration/<YYYY-MM-DD>-000004_fix_inverted_risk_scores/down.sql` — reverts the correction (re-inverts values)

## Implementation Notes
Fixes ACME-520.

**Code fix — `modules/risk/src/score.rs::compute_risk_score`**
- Current body: `total_deps as f64 / vulnerable_deps as f64` (operands swapped).
- Change it to `vulnerable_deps as f64 / total_deps as f64`.
- Add a guard: when `total_deps == 0`, return `0.0`. Without it the fixed formula gives `NaN` for `(0, 0)`. Today, `vulnerable_deps == 0` produces `+inf`.
- Keep the signature `pub fn compute_risk_score(total_deps: u32, vulnerable_deps: u32) -> f64` unchanged. The only caller is `modules/risk/src/assessment.rs::create_assessment`, which needs no changes because it already passes `(total_deps, vulnerable_deps)` in the right order.

**Reproducer test — `modules/risk/tests/score_test.rs`**
- Follow the existing `test_risk_score_all_vulnerable` pattern: a plain `#[test]` function that calls `compute_risk_score(...)` directly and checks the result with `assert_eq!`. Use a tolerance check (`(score - 0.05).abs() < f64::EPSILON`) if exact float comparison is fragile.
- Trigger scenario, from the Steps to Reproduce: 100 total dependencies, 5 vulnerable, so `compute_risk_score(100, 5)`.
- Buggy output (Actual Result): `20.0`. The test fails against the current code.
- Correct output (Expected Result): `0.05`. The test passes after the fix.
- The existing test uses `(10, 10)`, which returns `1.0` whichever way round the division is. That is why the bug went unnoticed. The new test must use `total != vulnerable`.

**Data migration — persistence impact**
- Persistence boundary: `modules/risk/src/assessment.rs::create_assessment` writes the score with `diesel::insert_into(assessments::table).values((assessments::risk_score.eq(score), ...))`. This happens once, at assessment creation. `modules/risk/src/endpoints.rs::get_assessment` reads `risk_score` straight from the table and never recomputes it.
- Table/column to correct: `assessments.risk_score` (`DOUBLE PRECISION`).
- Follow the existing Diesel migration convention in `migration/`: a `YYYY-MM-DD-NNNNNN_description/` directory containing `up.sql` and `down.sql`. Existing migrations are `2024-01-15-000001_create_sboms`, `2024-02-20-000002_create_assessments` and `2024-03-10-000003_add_severity_column`, so the new one is sequence `000004`, dated with the implementation date. Use `migration/2024-03-10-000003_add_severity_column/` as the layout reference and `migration/2024-02-20-000002_create_assessments/up.sql` for the table definition.
- Correction logic:
  - Preferred: if the SBOM's dependency and vulnerability counts can be read from source tables (via `assessments.sbom_id` -> `sboms.id`), recompute `risk_score = vulnerable / total` from that data, with `0.0` when total is 0.
  - Fallback: every stored value is exactly `total / vulnerable`, so the correct value is its reciprocal. `up.sql` along these lines:
    ```sql
    UPDATE assessments
    SET risk_score = CASE
        WHEN risk_score = 'Infinity'::float8 OR risk_score = 'NaN'::float8 THEN 0.0
        WHEN risk_score <> 0 THEN 1.0 / risk_score
        ELSE risk_score
    END;
    ```
  - `down.sql` applies the reciprocal again (`1.0 / risk_score` where `risk_score <> 0`). Rows that were `Infinity`/`NaN` and became `0.0` cannot be restored exactly, so note this in a comment in `down.sql`.
- Deploy the migration together with the code fix, so that no assessments are created with the old formula after the migration has run (which would leave a mix of corrected and uncorrected rows).

## Reuse Candidates
- `modules/risk/src/score.rs::compute_risk_score` — fix it in place rather than adding a new function
- `modules/risk/tests/score_test.rs::test_risk_score_all_vulnerable` — test structure and assertion pattern for the reproducer
- `migration/2024-03-10-000003_add_severity_column/` — Diesel `up.sql`/`down.sql` layout for the new data migration
- `migration/2024-02-20-000002_create_assessments/up.sql` — definition of the `assessments` table and its `risk_score` column

## Acceptance Criteria
- [ ] A reproducer test asserts `compute_risk_score(100, 5) == 0.05`. It fails before the fix (returns `20.0`) and passes after it.
- [ ] `compute_risk_score` returns `vulnerable_deps / total_deps`
- [ ] `compute_risk_score` returns `0.0` (not `NaN` or `inf`) when `total_deps == 0`
- [ ] New assessments created through `create_assessment` store the correct `risk_score`, and `GET /api/v2/assessments/{id}` returns it (e.g. `0.05` for 5/100)
- [ ] A Diesel data migration under `migration/` (named `YYYY-MM-DD-000004_fix_inverted_risk_scores`) corrects existing `assessments.risk_score` rows that hold the wrong value (e.g. a stored `20.0` becomes `0.05`, a stored `Infinity` becomes `0.0`)
- [ ] The migration includes a `down.sql`
- [ ] All existing tests still pass

## Test Requirements
- [ ] Reproducer test in `modules/risk/tests/score_test.rs`: call `compute_risk_score(100, 5)` and assert the result is `0.05`, not `20.0`. This is the scenario from ACME-520's Steps to Reproduce (100 dependencies, 5 vulnerable).
- [ ] Edge-case test: `compute_risk_score(0, 0)` returns `0.0`
- [ ] Edge-case test: `compute_risk_score(100, 0)` returns `0.0`
- [ ] Keep `test_risk_score_all_vulnerable` (`(10, 10)` gives `1.0`) passing
- [ ] Migration check: seed `assessments` rows with `risk_score` values `20.0`, `1.0` and `'Infinity'`, run the migration, and assert they become `0.05`, `1.0` and `0.0`

## Verification Commands
- `cargo test -p risk score_test` — the reproducer and edge-case tests pass
- `diesel migration run && diesel migration redo` — the migration applies and reverts cleanly
- `curl -s http://localhost:8080/api/v2/assessments/<id> | jq .risk_score` — returns `0.05` for an assessment on an SBOM with 5 of 100 dependencies vulnerable

## Bug Context

- **Bug**: [ACME-520](https://mock-jira.example.com/browse/ACME-520)
- **Steps to Reproduce**: Ingest an SBOM with 100 dependencies, 5 of them vulnerable. Create a risk assessment for it, call `GET /api/v2/assessments/{id}` and check `risk_score`.
- **Expected Result**: `risk_score` is `5 / 100 = 0.05` (vulnerable / total).
- **Actual Result**: `risk_score` is `100 / 5 = 20.0` (total / vulnerable), because the numerator and denominator are swapped.
- **Root Cause**: `modules/risk/src/score.rs::compute_risk_score` swaps the division operands. `create_assessment` stores the result in `assessments.risk_score` at creation time, and it is never recomputed, so existing rows stay wrong until a data migration corrects them.
