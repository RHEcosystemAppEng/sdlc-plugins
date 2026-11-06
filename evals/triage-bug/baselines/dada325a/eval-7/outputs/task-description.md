# Jira API Metadata (jira.create_issue)

```json
{
  "cloudId": "mock-cloud-id-for-eval",
  "projectKey": "ACME",
  "issueTypeName": "Task",
  "summary": "Fix inverted risk score in compute_risk_score and correct persisted assessments.risk_score values",
  "additional_fields": {
    "labels": ["ai-generated-jira"]
  }
}
```

Follow-up operations after creation:

- Step 5b: `jira.create_issue_link(link_type="Blocks", inward_issue_key=<created-task-key>, outward_issue_key="ACME-520")` — the Task blocks the Bug.
- Step 5c: re-fetch `<created-task-key>`, compute digest with `python3 scripts/sha256-digest.py /tmp/desc-<created-task-key>.txt`, post standalone comment `[sdlc-workflow] Description digest: <tagged-digest>` (no footnote).

---

## Repository
acme-backend

## Target Branch
main

## Description
Fixes ACME-520. `compute_risk_score()` divides with its operands swapped, returning
`total_deps / vulnerable_deps` instead of `vulnerable_deps / total_deps`. For an SBOM
with 100 dependencies of which 5 are vulnerable, the risk score is `20.0` instead of
`0.05`. Because the score is persisted to `assessments.risk_score` once at assessment
creation and is never recomputed on read, every existing assessment in the database
also carries the inflated value. This task fixes the calculation, adds a reproducer
test, and adds a Diesel data migration that corrects already-persisted scores.

## Files to Modify
- `modules/risk/src/score.rs` — swap the division operands in `compute_risk_score` and handle `total_deps == 0`
- `modules/risk/tests/score_test.rs` — add reproducer test and asymmetric/edge-case tests

## Files to Create
- `migration/<YYYY-MM-DD>-000004_fix_assessment_risk_score/up.sql` — data migration that corrects existing `assessments.risk_score` values
- `migration/<YYYY-MM-DD>-000004_fix_assessment_risk_score/down.sql` — reverts the correction

## Implementation Notes
Fixes ACME-520.

**Code fix — `modules/risk/src/score.rs::compute_risk_score`**
- Current: `total_deps as f64 / vulnerable_deps as f64`.
- Correct: `vulnerable_deps as f64 / total_deps as f64`.
- Guard `total_deps == 0` and return `0.0` (no dependencies means no risk), so the
  function never yields `NaN`/`Infinity`. Keep the signature
  `pub fn compute_risk_score(total_deps: u32, vulnerable_deps: u32) -> f64` unchanged so
  the sole caller, `modules/risk/src/assessment.rs::create_assessment`, needs no change.

**Reproducer test — `modules/risk/tests/score_test.rs`**
- Scenario from the bug: SBOM with 100 total dependencies, 5 vulnerable.
- Before the fix, `compute_risk_score(100, 5)` returns `20.0` (Actual Result) — the test
  fails against current code.
- After the fix it must return `0.05` (Expected Result).
- Follow the existing `#[test]` + `assert_eq!` style of `test_risk_score_all_vulnerable`;
  for non-integral floats prefer an epsilon comparison
  (e.g., `assert!((score - 0.05).abs() < f64::EPSILON)`).
- Note that `test_risk_score_all_vulnerable` (`compute_risk_score(10, 10) == 1.0`) passes
  regardless of operand order — that is why the bug went undetected. Keep it, but rely on
  asymmetric inputs for real coverage.

**Data migration (persistence impact)**
- Persistence boundary: `modules/risk/src/assessment.rs::create_assessment` writes the
  score via `diesel::insert_into(assessments::table).values(assessments::risk_score.eq(score))`.
  Table `assessments`, column `risk_score` (`DOUBLE PRECISION`), written once at
  ingestion time. `modules/risk/src/endpoints.rs::get_assessment` reads it back unchanged,
  so existing rows will never self-correct.
- Follow the existing Diesel migration convention in `migration/`
  (`2024-01-15-000001_create_sboms`, `2024-02-20-000002_create_assessments`,
  `2024-03-10-000003_add_severity_column`): directory `YYYY-MM-DD-NNNNNN_description/`
  with `up.sql` and `down.sql`. Use the next sequence number, `000004`, and the date
  the migration is authored.
- Correction logic. The `assessments` row does not store the original
  `total_deps`/`vulnerable_deps`. Preferred: if per-SBOM dependency and vulnerability
  counts can be derived from the `sboms` table (and related tables) via
  `assessments.sbom_id`, recompute `risk_score = vulnerable / total` from that source
  data. Otherwise, use the exact mathematical inverse of the bug (stored value is
  `total / vulnerable`, correct value is `vulnerable / total`):
  ```sql
  UPDATE assessments
  SET risk_score = CASE
      WHEN risk_score = 'Infinity'::float8 THEN 0.0   -- vulnerable_deps was 0
      WHEN risk_score = 'NaN'::float8      THEN 0.0   -- total_deps and vulnerable_deps were 0
      WHEN risk_score > 0                  THEN 1.0 / risk_score
      ELSE risk_score
  END;
  ```
  `down.sql` can apply the reciprocal again for finite positive values (the transform is
  self-inverse); the `Infinity`/`NaN` -> `0.0` cases are lossy and should be documented
  as such in `down.sql`.
- Ordering matters: the migration must correct only rows written by the buggy code.
  Ship the migration in the same release as the code fix so Diesel runs it before the
  fixed code writes new rows; do not run the reciprocal transform on rows already written
  by the fixed function.

## Reuse Candidates
- `modules/risk/src/score.rs::compute_risk_score` — the function to fix in place; no new helper needed
- `modules/risk/tests/score_test.rs::test_risk_score_all_vulnerable` — existing test pattern to follow for the reproducer
- `migration/2024-03-10-000003_add_severity_column/` — most recent Diesel migration; template for directory naming and `up.sql`/`down.sql` layout

## Acceptance Criteria
- [ ] A reproducer test asserts `compute_risk_score(100, 5) == 0.05`; it fails against the current code (returns `20.0`) and passes after the fix
- [ ] `compute_risk_score` returns `vulnerable_deps / total_deps` for all inputs where `total_deps > 0`
- [ ] `compute_risk_score` returns `0.0` when `total_deps == 0` (no `NaN`/`Infinity`)
- [ ] New assessments created via `create_assessment` persist the correct `risk_score`, and `GET /api/v2/assessments/{id}` returns it
- [ ] Existing `assessments` records with incorrect persisted `risk_score` values are corrected by the new data migration (e.g., a stored `20.0` becomes `0.05`; stored `Infinity` becomes `0.0`)
- [ ] The migration follows the Diesel `migration/YYYY-MM-DD-NNNNNN_description/{up.sql,down.sql}` convention
- [ ] No regression in existing tests (including `test_risk_score_all_vulnerable`)

## Test Requirements
- [ ] Reproducer test in `modules/risk/tests/score_test.rs`: call `compute_risk_score(100, 5)` (100 total, 5 vulnerable, per ACME-520 Steps to Reproduce) and assert the result is `0.05` (Expected Result), not `20.0` (Actual Result)
- [ ] Asymmetric case in the other direction, e.g. `compute_risk_score(10, 3)` ≈ `0.3`, to ensure operand order is locked in
- [ ] Edge cases: `compute_risk_score(50, 0) == 0.0` and `compute_risk_score(0, 0) == 0.0`
- [ ] Migration verification: seed `assessments` rows with `risk_score` values `20.0`, `'Infinity'`, and `1.0`; after running `up.sql`, assert they become `0.05`, `0.0`, and `1.0` respectively

## Verification Commands
- `cargo test -p risk` (or `cargo test --test score_test`) — all score tests pass, including the new reproducer
- `diesel migration run` followed by `diesel migration redo` — migration applies and reverts cleanly
- `curl -s http://localhost:8080/api/v2/assessments/{id} | jq .risk_score` — for an assessment of an SBOM with 100 deps / 5 vulnerable, returns `0.05`

## Bug Context

- **Bug**: [ACME-520](https://mock-jira.example.com/browse/ACME-520)
- **Steps to Reproduce**: Ingest an SBOM with 100 total dependencies (5 vulnerable), create a risk assessment for it, fetch it via `GET /api/v2/assessments/{id}`, and inspect `risk_score`.
- **Expected Result**: `risk_score` is `5 / 100 = 0.05` (vulnerable / total).
- **Actual Result**: `risk_score` is `100 / 5 = 20.0` (total / vulnerable) — numerator and denominator are swapped.
- **Root Cause**: `modules/risk/src/score.rs::compute_risk_score` computes `total_deps / vulnerable_deps` instead of `vulnerable_deps / total_deps`. The value is persisted once to `assessments.risk_score` by `create_assessment` at ingestion time and returned as-is by `get_assessment`, so existing records are stale and require a data migration in addition to the code fix.
