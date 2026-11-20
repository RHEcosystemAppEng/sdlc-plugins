# Jira API Metadata (jira.create_issue parameters)

```
jira.create_issue(
  cloudId: "mock-cloud-id-for-eval",
  projectKey: "ACME",
  issueTypeName: "Task",
  summary: "Fix swapped operands in compute_risk_score and migrate persisted assessment risk scores",
  description: <task description body below, markdown>,
  additional_fields: {
    "labels": ["ai-generated-jira"]
  }
)
```

| Parameter | Value |
|---|---|
| Project key | `ACME` |
| Issue type | `Task` |
| Summary | Fix swapped operands in compute_risk_score and migrate persisted assessment risk scores |
| Labels | `ai-generated-jira` |

Follow-up operations after creation:

- **Step 5b link:** `jira.create_issue_link(link_type="Blocks", inward_issue_key=<created-task-key>, outward_issue_key="ACME-520")`. The Task blocks the Bug.
- **Step 5c digest:** re-fetch the created task with `jira.get_issue(<created-task-key>)`, write the description to `/tmp/desc-<task-key>.txt`, and run `python3 scripts/sha256-digest.py /tmp/desc-<task-key>.txt`. Then post the standalone comment `[sdlc-workflow] Description digest: <tagged-digest>`, with no footnote.

---

## Repository
acme-backend

## Target Branch
main

## Description
Fixes ACME-520. `compute_risk_score()` in the risk engine has its division operands swapped. It computes `total_deps / vulnerable_deps` instead of `vulnerable_deps / total_deps`, so every risk assessment gets an inflated score (e.g. `20.0` instead of `0.05` for 5 vulnerable out of 100 dependencies). The score is persisted to `assessments.risk_score` once, when the assessment is created, and `GET /api/v2/assessments/{id}` returns the stored value without recomputing it. This task therefore covers both the code fix and a data migration that corrects every existing assessment row holding an incorrect score.

## Files to Modify
- `modules/risk/src/score.rs` — fix `compute_risk_score` to return `vulnerable_deps / total_deps`, returning `0.0` when `total_deps == 0`
- `modules/risk/tests/score_test.rs` — add the reproducer test and edge-case tests; the existing `test_risk_score_all_vulnerable` only covers `total == vulnerable`

## Files to Create
- `migration/2026-11-20-000004_fix_assessment_risk_scores/up.sql` — Diesel data migration that corrects existing inflated `assessments.risk_score` values
- `migration/2026-11-20-000004_fix_assessment_risk_scores/down.sql` — reverse migration (see Implementation Notes)

## Implementation Notes
Fixes ACME-520.

**Code fix: `modules/risk/src/score.rs::compute_risk_score`**
- The current line `total_deps as f64 / vulnerable_deps as f64` has the operands reversed. Change it to `vulnerable_deps as f64 / total_deps as f64`.
- Add a guard: if `total_deps == 0`, return `0.0`. This avoids `NaN` from `0.0 / 0.0`. The correct score is always in `[0.0, 1.0]`.
- Keep the signature `pub fn compute_risk_score(total_deps: u32, vulnerable_deps: u32) -> f64` unchanged. Its only caller, `modules/risk/src/assessment.rs::create_assessment`, already passes the arguments in `(total_deps, vulnerable_deps)` order, so no caller changes are needed.

**Reproducer test: `modules/risk/tests/score_test.rs`**
- Follow the existing pattern in `test_risk_score_all_vulnerable`: a plain `#[test]` function that calls `compute_risk_score` directly and checks the result with `assert_eq!`.
- Trigger scenario from the bug: `compute_risk_score(100, 5)`.
  - Before the fix it returns `20.0` (the Actual Result: total / vulnerable).
  - After the fix it must return `0.05` (the Expected Result: vulnerable / total).
- Use exact equality or a small epsilon for floats. `5.0 / 100.0` is exactly representable enough that `assert_eq!(score, 0.05)` holds in practice; `(score - 0.05).abs() < f64::EPSILON` is the safer form.
- Edge cases: `compute_risk_score(100, 0) == 0.0` (the buggy code returns `inf`) and `compute_risk_score(0, 0) == 0.0` (no NaN).

**Persistence impact and data migration**
- Persistence boundary: `modules/risk/src/assessment.rs::create_assessment` calls `diesel::insert_into(assessments::table).values((assessments::sbom_id.eq(sbom_id), assessments::risk_score.eq(score), assessments::created_at.eq(now)))`.
  - The value is written once at ingestion time, when the assessment is created.
  - `modules/risk/src/endpoints.rs::get_assessment` reads it back with `assessments::table.find(id).first::<Assessment>()` and never recomputes it.
  - Existing rows are therefore stale and will not self-correct.
- Table and column: `assessments.risk_score` (`DOUBLE PRECISION`).
- Follow the existing Diesel migration convention in `migration/` (`YYYY-MM-DD-NNNNNN_description/up.sql` + `down.sql`). Existing examples are `migration/2024-02-20-000002_create_assessments/` and `migration/2024-03-10-000003_add_severity_column/`. The next sequence number is `000004`; adjust the date prefix to the actual implementation date.
- Migration logic for `up.sql`:
  - **Preferred:** if the SBOM's dependency and vulnerability counts can be derived in SQL from source tables joined on `assessments.sbom_id` (e.g. the `sboms` table and related dependency/vulnerability tables), recompute `risk_score = vulnerable_count::float8 / NULLIF(total_count, 0)`, coalescing to `0.0`. This matches the fixed `compute_risk_score` exactly. Confirm which tables hold these counts before choosing this path.
  - **Fallback (algebraic):** the `assessments` table does not store the input counts. Every buggy value equals `total / vulnerable`, so the correct value is its reciprocal:
    ```sql
    UPDATE assessments
    SET risk_score = CASE
        WHEN risk_score = 'Infinity'::float8 OR risk_score = 'NaN'::float8 THEN 0.0
        ELSE 1.0 / risk_score
    END
    WHERE risk_score > 1.0 OR risk_score = 'NaN'::float8;
    ```
    - Correct scores are always `<= 1.0`, while buggy ones are always `>= 1.0`, `Infinity` or `NaN`. The `WHERE` clause therefore skips rows that are already correct.
    - Rows with exactly `1.0` (total == vulnerable) are identical under both formulas and need no change.
    - In Postgres, `'NaN'::float8 > 1.0` is true, but the explicit check keeps the intent clear.
- Ordering and idempotency: the reciprocal update is not idempotent on rows below 1.0, so ship the migration in the same deployment as the code fix. Diesel's `__diesel_schema_migrations` tracking ensures it runs exactly once.
- `down.sql`: the reciprocal is reversible except for rows mapped from `Infinity`/`NaN` to `0.0`. Either apply the inverse (`1.0 / risk_score` for `0 < risk_score < 1.0`) with a comment noting that the zero-mapped rows cannot be restored, or make `down.sql` a documented no-op. Choose whichever matches how existing data migrations handle irreversible changes.

**Conventions:** acme-backend has no CONVENTIONS.md. Follow the patterns in the referenced files.

## Reuse Candidates
- `modules/risk/src/score.rs::compute_risk_score` — the function being fixed; the migration's recompute formula must match its corrected semantics (`vulnerable / total`, `0.0` when total is 0)
- `modules/risk/tests/score_test.rs::test_risk_score_all_vulnerable` — existing test pattern to copy for the reproducer and edge-case tests
- `migration/2024-03-10-000003_add_severity_column/` — most recent Diesel migration; follow its directory layout and `up.sql`/`down.sql` structure

## Acceptance Criteria
- [ ] A reproducer test asserts `compute_risk_score(100, 5) == 0.05`; it fails against the current code (returns `20.0`) and passes after the fix
- [ ] `compute_risk_score` returns `vulnerable_deps / total_deps` and returns `0.0` (not `NaN` or `Infinity`) when `total_deps == 0` or `vulnerable_deps == 0`
- [ ] New assessments created through `create_assessment` persist the correct `risk_score` (e.g. `0.05` for 5 of 100 vulnerable), and `GET /api/v2/assessments/{id}` returns it
- [ ] A Diesel data migration in `migration/` corrects existing `assessments` records with incorrect persisted `risk_score` values (e.g. a stored `20.0` becomes `0.05`; `Infinity` becomes `0.0`), and leaves already-correct values (`<= 1.0`) untouched
- [ ] After migration, every `assessments.risk_score` value is in `[0.0, 1.0]`
- [ ] No regressions: all existing tests pass, including `test_risk_score_all_vulnerable`

## Test Requirements
- [ ] Reproducer test in `modules/risk/tests/score_test.rs` (e.g. `test_risk_score_partial_vulnerable`): call `compute_risk_score(100, 5)` and assert the result equals `0.05`. Before the fix this returns `20.0` (total / vulnerable, the bug's Actual Result); after the fix it returns `0.05` (vulnerable / total, the bug's Expected Result).
- [ ] Edge-case test: `compute_risk_score(100, 0)` returns `0.0` (the buggy code returns `inf`)
- [ ] Edge-case test: `compute_risk_score(0, 0)` returns `0.0` (no `NaN`)
- [ ] Migration test (integration, against a test database): seed `assessments` rows with `risk_score` values `20.0`, `Infinity` and `1.0`, run the migration, and assert they become `0.05`, `0.0` and `1.0` respectively
- [ ] Existing `test_risk_score_all_vulnerable` still passes

## Verification Commands
- `cargo test -p risk score` — all score tests pass, including the new reproducer
- `diesel migration run` then `psql -c "SELECT count(*) FROM assessments WHERE risk_score > 1.0 OR risk_score = 'NaN'::float8;"` — returns `0`

## Bug Context

- **Bug**: [ACME-520](https://mock-jira.example.com/browse/ACME-520)
- **Steps to Reproduce**: Ingest an SBOM with 100 total dependencies (5 vulnerable), create a risk assessment for it, retrieve it via `GET /api/v2/assessments/{id}`, and inspect `risk_score`.
- **Expected Result**: `risk_score` is `5 / 100 = 0.05` (vulnerable / total).
- **Actual Result**: `risk_score` is `100 / 5 = 20.0` (total / vulnerable); numerator and denominator are swapped.
- **Root Cause**: `modules/risk/src/score.rs::compute_risk_score` divides `total_deps / vulnerable_deps` instead of `vulnerable_deps / total_deps`. The result is persisted at creation time to `assessments.risk_score` by `modules/risk/src/assessment.rs::create_assessment` and served unchanged by `get_assessment`, so existing records stay wrong until a data migration corrects them.
