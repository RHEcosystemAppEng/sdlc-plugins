# Jira API Metadata (simulated `jira.create_issue`)

```
jira.create_issue(
  cloudId: "mock-cloud-id-for-eval",
  projectKey: "ACME",
  issueTypeName: "Task",
  summary: "Fix swapped operands in compute_risk_score and correct persisted assessment risk scores (ACME-520)",
  description: <task description body below, markdown>,
  additional_fields: {
    "labels": ["ai-generated-jira"]
  }
)
```

Follow-up operations:
- Step 5b: `jira.create_issue_link(link_type="Blocks", inward_issue_key=<created-task-key>, outward_issue_key="ACME-520")` — Task blocks Bug.
- Step 5c: re-fetch the created task, compute `python3 scripts/sha256-digest.py /tmp/desc-<task-key>.txt`, post standalone comment `[sdlc-workflow] Description digest: <tagged-digest>` (no footnote).

---

## Repository
acme-backend

## Target Branch
main

## Description
Fixes ACME-520. `compute_risk_score()` divides total dependencies by vulnerable
dependencies instead of vulnerable by total, inverting every risk score (100 total /
5 vulnerable yields `20.0` instead of `0.05`). The score is persisted to
`assessments.risk_score` when an assessment is created and is served verbatim by
`GET /api/v2/assessments/{id}`, so in addition to fixing the function, a data migration
is required to correct the scores already stored for existing assessments.

## Files to Modify
- `modules/risk/src/score.rs` — swap the division operands in `compute_risk_score` and guard against `total_deps == 0`
- `modules/risk/tests/score_test.rs` — add the reproducer test and additional coverage for `total != vulnerable` and zero-input cases

## Files to Create
- `migration/YYYY-MM-DD-000004_fix_assessment_risk_scores/up.sql` — data migration correcting existing `assessments.risk_score` values (use the date the migration is authored; `000004` follows the existing sequence `000001`–`000003`)
- `migration/YYYY-MM-DD-000004_fix_assessment_risk_scores/down.sql` — reverse of the correction

## Implementation Notes
Fixes ACME-520.

**Code fix** — `modules/risk/src/score.rs::compute_risk_score(total_deps: u32, vulnerable_deps: u32) -> f64`
currently returns `total_deps as f64 / vulnerable_deps as f64`. Change it to
`vulnerable_deps as f64 / total_deps as f64`. Add a guard so that `total_deps == 0`
returns `0.0` rather than `NaN` (`0.0 / 0.0`), which would otherwise be persisted. Keep
the function signature unchanged — the only caller is
`modules/risk/src/assessment.rs::create_assessment`, which passes
`(total_deps, vulnerable_deps)` in the correct order and needs no change.

**Reproducer test** — add to `modules/risk/tests/score_test.rs`, following the existing
`test_risk_score_all_vulnerable` pattern (`#[test]` + direct call + assertion):
- Input (from Steps to Reproduce): `compute_risk_score(100, 5)` — 100 total, 5 vulnerable.
- Before the fix it returns `20.0` (Actual Result); after the fix it must return `0.05`
  (Expected Result). Use an epsilon comparison for floats, e.g.
  `assert!((score - 0.05).abs() < f64::EPSILON * 10.0)`.
- Note the existing `test_risk_score_all_vulnerable` (`10, 10 → 1.0`) is insensitive to
  operand order — that is why the bug went undetected; keep it, but do not rely on it.

**Persistence impact / data migration** — the buggy value is persisted at ingestion time:
`compute_risk_score()` → `create_assessment()` →
`diesel::insert_into(assessments::table).values(assessments::risk_score.eq(score), ...)`.
`modules/risk/src/endpoints.rs::get_assessment` reads `risk_score` straight from the
table with no recomputation, so existing rows stay wrong until corrected.

Create a Diesel migration following the existing convention in `migration/`
(`YYYY-MM-DD-NNNNNN_description/` with `up.sql` and `down.sql`, cf.
`migration/2024-03-10-000003_add_severity_column/`):
- Table/column: `assessments.risk_score` (`DOUBLE PRECISION`).
- Correct value: `vulnerable_deps / total_deps`. Since the stored value is exactly
  `total_deps / vulnerable_deps`, the correct value is its reciprocal. Preferred: if
  dependency counts for each assessment's SBOM are queryable from source tables (via
  `assessments.sbom_id` → `sboms`), recompute the score from those counts. Otherwise
  apply the reciprocal transformation:
  ```sql
  -- up.sql
  UPDATE assessments SET risk_score = 0.0
    WHERE risk_score = 'Infinity'::double precision;   -- bug produced inf when vulnerable_deps = 0
  UPDATE assessments SET risk_score = 1.0 / risk_score
    WHERE risk_score > 0 AND risk_score <> 'Infinity'::double precision;
  ```
  Rows with `NaN` (0 total, 0 vulnerable) should be set to `0.0`.
- `down.sql`: apply the reciprocal again for `risk_score > 0` (the transformation is
  its own inverse); rows mapped from `inf` to `0.0` cannot be distinguished from genuine
  zeros — document this as a lossy edge in a SQL comment.
- The reciprocal migration is not idempotent; it relies on Diesel running each migration
  exactly once. Deploy the code fix and the migration together so no new rows are written
  with the old formula after the migration runs (or, if they could be, scope the
  `UPDATE` to `created_at` before the deployment cutover).

No `CONVENTIONS.md` exists in acme-backend; follow the patterns above (Diesel ORM,
Diesel SQL migrations, tests under `modules/risk/tests/`).

## Reuse Candidates
- `modules/risk/src/score.rs::compute_risk_score` — the function being fixed; keep its signature so `create_assessment` remains unchanged
- `modules/risk/tests/score_test.rs::test_risk_score_all_vulnerable` — existing test pattern to follow for the reproducer
- `migration/2024-03-10-000003_add_severity_column/` — most recent migration; template for directory naming and `up.sql`/`down.sql` layout
- `migration/2024-02-20-000002_create_assessments/up.sql` — defines the `assessments` table schema targeted by the data migration

## Acceptance Criteria
- [ ] A reproducer test asserting `compute_risk_score(100, 5)` returns `0.05` exists in `modules/risk/tests/score_test.rs`; it fails against the current code (returns `20.0`) and passes after the fix
- [ ] `compute_risk_score` returns `vulnerable_deps / total_deps` for all inputs where `total_deps > 0`
- [ ] `compute_risk_score` returns `0.0` (not `NaN` or `inf`) when `total_deps == 0` or `vulnerable_deps == 0`
- [ ] Newly created assessments persist the correct `risk_score` and `GET /api/v2/assessments/{id}` returns it (e.g. `0.05` for 100 total / 5 vulnerable)
- [ ] A Diesel data migration under `migration/` following the `YYYY-MM-DD-NNNNNN_description/{up.sql,down.sql}` convention corrects existing `assessments` records whose persisted `risk_score` was computed with the inverted formula (including `inf` values → `0.0`)
- [ ] No regression in existing tests (including `test_risk_score_all_vulnerable`)

## Test Requirements
- [ ] Reproducer: `compute_risk_score(100, 5)` ≈ `0.05` (epsilon float comparison). Derived from ACME-520 Steps to Reproduce (100 total, 5 vulnerable); must assert the Expected Result `0.05`, not the Actual Result `20.0`
- [ ] Asymmetric-input cases that are sensitive to operand order, e.g. `compute_risk_score(10, 2)` ≈ `0.2`, `compute_risk_score(4, 1)` ≈ `0.25`
- [ ] Edge cases: `compute_risk_score(100, 0)` == `0.0`; `compute_risk_score(0, 0)` == `0.0` (no NaN)
- [ ] Migration check: seed an `assessments` row with the old inverted value (e.g. `20.0`), run the migration, assert the row's `risk_score` becomes `0.05`; seed a row with `Infinity`, assert it becomes `0.0`; verify `diesel migration redo` runs cleanly

## Verification Commands
- `cargo test -p risk` (or `cargo test --test score_test`) — all tests pass, including the new reproducer
- `diesel migration run` — new `000004` migration applies without error
- `diesel migration redo` — migration reverts and reapplies cleanly
- `curl -s http://localhost:8080/api/v2/assessments/{id} | jq .risk_score` — for an SBOM with 100 total / 5 vulnerable deps, returns `0.05`

## Bug Context

- **Bug**: [ACME-520](https://mock-jira.example.com/browse/ACME-520)
- **Steps to Reproduce**: Ingest an SBOM with 100 total dependencies (5 vulnerable), create a risk assessment for it, retrieve it via `GET /api/v2/assessments/{id}`, and inspect `risk_score`.
- **Expected Result**: `risk_score` is `5 / 100 = 0.05` (vulnerable / total).
- **Actual Result**: `risk_score` is `100 / 5 = 20.0` (total / vulnerable) — numerator and denominator are swapped.
- **Root Cause**: `modules/risk/src/score.rs::compute_risk_score` computes `total_deps / vulnerable_deps` instead of `vulnerable_deps / total_deps`. The result is persisted at assessment creation time to `assessments.risk_score` by `create_assessment` and served without recomputation, so existing rows hold inverted scores and require a data migration in addition to the code fix.
