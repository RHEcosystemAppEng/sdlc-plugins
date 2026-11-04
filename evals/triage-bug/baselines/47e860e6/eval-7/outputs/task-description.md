# Jira API Metadata (jira.create_issue parameters)

```
jira.create_issue(
  cloudId: "mock-cloud-id-for-eval",
  project_key: "ACME",
  issue_type: "Task",
  summary: "Fix inverted risk score in compute_risk_score and correct persisted assessment scores (ACME-520)",
  description: <task description body below>,
  additional_fields: {
    "labels": ["ai-generated-jira"]
  }
)
```

- **Project key**: ACME
- **Issue type**: Task
- **Labels**: `ai-generated-jira`

---

## Repository
acme-backend

## Target Branch
main

## Description
Fixes ACME-520. `compute_risk_score()` divides total dependencies by vulnerable dependencies when it should divide vulnerable by total. As a result, every risk assessment gets an inverted, inflated score: 5 vulnerable out of 100 produces `20.0` instead of `0.05`. The score is persisted to `assessments.risk_score` when the assessment is created and is never recomputed on read. Two changes are needed: correct the formula so new assessments are right, and add a data migration that repairs the inflated scores already stored for existing assessments.

## Files to Modify
- `modules/risk/src/score.rs` — swap the division operands in `compute_risk_score` to `vulnerable_deps / total_deps` and return `0.0` when `total_deps == 0`
- `modules/risk/tests/score_test.rs` — add the reproducer test and edge-case tests for `compute_risk_score`

## Files to Create
- `migration/2026-11-04-000004_fix_assessment_risk_scores/up.sql` — data migration that corrects existing inflated values in `assessments.risk_score`. Follows the Diesel `YYYY-MM-DD-NNNNNN_description` convention; the latest existing migration is `2024-03-10-000003_add_severity_column`. Use the actual creation date as the prefix.
- `migration/2026-11-04-000004_fix_assessment_risk_scores/down.sql` — required by Diesel. A documented no-op, since the correction cannot be safely reversed once new, correctly scored rows exist.

## Implementation Notes
Fixes ACME-520.

**Code fix (`modules/risk/src/score.rs::compute_risk_score`)**
- The current body is `total_deps as f64 / vulnerable_deps as f64`. Change it to `vulnerable_deps as f64 / total_deps as f64`.
- Add a guard: when `total_deps == 0`, return `0.0`. Without it the result is `NaN`/`Infinity`, which is invalid in a `DOUBLE PRECISION` column and in JSON. After the fix the result is always in `[0.0, 1.0]`, given `vulnerable_deps <= total_deps`.
- Keep the signature `pub fn compute_risk_score(total_deps: u32, vulnerable_deps: u32) -> f64` unchanged. The only caller is `modules/risk/src/assessment.rs::create_assessment`, and it needs no changes.

**Persistence impact and data migration**
- Persistence boundary: `modules/risk/src/assessment.rs::create_assessment` writes the score with `diesel::insert_into(assessments::table).values((... assessments::risk_score.eq(score) ...))`. This happens at ingestion time (once, on creation).
- `modules/risk/src/endpoints.rs::get_assessment` (`GET /api/v2/assessments/{id}`) returns the stored `risk_score` without recomputing it. Existing rows therefore stay wrong until they are migrated.
- Table/column to correct: `assessments.risk_score` (`DOUBLE PRECISION`). The table does not store `total_deps` or `vulnerable_deps`. However, the bug is a pure operand swap: stored = `total / vulnerable` and correct = `vulnerable / total`, so correct = `1 / stored`.
- Buggy values are always `>= 1` and correct values are always `<= 1`. Restrict the update to `risk_score > 1` so the migration is idempotent and cannot touch rows written by the fixed code.
- Suggested `up.sql`:
  ```sql
  -- ACME-520: risk_score was persisted as total_deps / vulnerable_deps (inverted).
  -- Correct value is the reciprocal. 1.0 / 'Infinity' = 0 handles vulnerable_deps = 0.
  UPDATE assessments
     SET risk_score = 1.0 / risk_score
   WHERE risk_score > 1
     AND risk_score <> 'NaN'::float8;

  -- Rows where total_deps = vulnerable_deps = 0 were stored as NaN; align with the new zero-total guard.
  UPDATE assessments
     SET risk_score = 0.0
   WHERE risk_score = 'NaN'::float8;
  ```
- Suggested `down.sql`: a comment-only no-op explaining that the data correction is intentionally irreversible.
- Follow the existing Diesel migration layout in `migration/` (for example, `migration/2024-03-10-000003_add_severity_column/up.sql` and `down.sql`). Use `migration/2024-02-20-000002_create_assessments/up.sql` as the reference for the `assessments` column definitions.
- Alternative: if the reviewer prefers to recompute from source data (SBOM dependency and vulnerability records reached via `assessments.sbom_id`), that is acceptable. The reciprocal approach is exact for this defect and avoids depending on source data that may have changed since the assessment was created.

**Reproducer test guidance (`modules/risk/tests/score_test.rs`)**
- Trigger: `compute_risk_score(100, 5)`, which mirrors the bug's Steps to Reproduce (an SBOM with 100 total dependencies, 5 of them vulnerable).
- Before the fix: returns `20.0` (Actual Result).
- After the fix: must return `0.05` (Expected Result). Use a float tolerance, for example `assert!((score - 0.05).abs() < f64::EPSILON)`, or `assert_eq!` if exact.
- Follow the existing pattern in `test_risk_score_all_vulnerable`: a `#[test]` function that calls `compute_risk_score` directly and asserts the result. That test uses `(10, 10)`, which cannot detect the operand swap. That gap is the reason this bug went unnoticed.

No CONVENTIONS.md exists in acme-backend. Follow the patterns observed above.

## Reuse Candidates
- `modules/risk/src/score.rs::compute_risk_score` — fix in place. It is the single source of truth for the score formula.
- `modules/risk/tests/score_test.rs::test_risk_score_all_vulnerable` — existing test pattern to copy for the new tests.
- `migration/2024-03-10-000003_add_severity_column/` — most recent Diesel migration. Use it as the naming and structure template for the new migration directory.
- `migration/2024-02-20-000002_create_assessments/up.sql` — schema reference for the `assessments` table and its `risk_score` column.

## Acceptance Criteria
- [ ] A reproducer test asserts that `compute_risk_score(100, 5)` returns `0.05`. It fails before the fix (returns `20.0`) and passes after.
- [ ] `compute_risk_score` returns `vulnerable_deps / total_deps` for all inputs where `total_deps > 0`
- [ ] `compute_risk_score` returns `0.0` when `total_deps == 0`, with no `NaN` or `Infinity`
- [ ] New assessments created through `create_assessment` persist the corrected score, and `GET /api/v2/assessments/{id}` returns it (for example, `0.05` for 5 of 100)
- [ ] A Diesel data migration corrects existing `assessments` rows with incorrectly persisted `risk_score` values: buggy finite values become their reciprocal, `Infinity` becomes `0.0`, and rows already in `[0, 1]` are untouched
- [ ] The migration is idempotent: running the correction twice does not change already-corrected rows
- [ ] No regression in existing tests, and `test_risk_score_all_vulnerable` still passes

## Test Requirements
- [ ] Reproducer test in `modules/risk/tests/score_test.rs`: `compute_risk_score(100, 5)` must equal `0.05`. Before the fix it returns `20.0`, which is the bug's Actual Result, so the test must fail on the unfixed code.
- [ ] Edge-case test: `compute_risk_score(100, 0)` returns `0.0` (no vulnerable dependencies)
- [ ] Edge-case test: `compute_risk_score(0, 0)` returns `0.0` (zero-total guard)
- [ ] Asymmetric case: `compute_risk_score(4, 1)` returns `0.25`, which guards against an operand regression
- [ ] Migration test (integration or manual against a test database): seed `assessments` rows with `risk_score` values `20.0`, `'Infinity'`, `1.0`, and `0.05`, then run the migration. Assert the results `0.05`, `0.0`, `1.0`, and `0.05` respectively.

## Verification Commands
- `cargo test -p risk score` — all `compute_risk_score` tests pass, including the reproducer (adjust the package name to the actual crate name)
- `diesel migration run` — the new `2026-11-04-000004_fix_assessment_risk_scores` migration applies without error
- `psql -c "SELECT count(*) FROM assessments WHERE risk_score > 1 OR risk_score = 'NaN'::float8;"` — returns `0` after the migration

## Bug Context

- **Bug**: [ACME-520](https://mock-jira.example.com/browse/ACME-520)
- **Steps to Reproduce**: Ingest an SBOM with 100 total dependencies, 5 of them vulnerable. Create a risk assessment for it, call `GET /api/v2/assessments/{id}`, and inspect `risk_score`.
- **Expected Result**: `risk_score` is `5 / 100 = 0.05` (vulnerable / total).
- **Actual Result**: `risk_score` is `100 / 5 = 20.0` (total / vulnerable), because the numerator and denominator are swapped.
- **Root Cause**: `modules/risk/src/score.rs::compute_risk_score` computes `total_deps / vulnerable_deps` instead of `vulnerable_deps / total_deps`. The incorrect value is persisted to `assessments.risk_score` by `create_assessment` when the assessment is created, and the read endpoint never recomputes it. Existing records therefore need a data migration in addition to the code fix.

---

# Follow-up Jira operations (Steps 5b, 5c, 7) — not executed in eval

**Step 5b — Link Task to Bug**
```
jira.create_issue_link(
  link_type: "Blocks",
  inward_issue_key: "<created-task-key>",   # Task = blocker
  outward_issue_key: "ACME-520"             # Bug = blocked
)
```

**Step 5c — Digest comment**
1. `jira.get_issue("<created-task-key>")`, then write the `description` field to `/tmp/desc-<created-task-key>.txt`
2. `python3 scripts/sha256-digest.py /tmp/desc-<created-task-key>.txt`, which outputs `sha256-md:...` or `sha256-adf:...`
3. Post a standalone ADF comment: `[sdlc-workflow] Description digest: <tagged-digest>`. Do not add the footnote.

**Step 6 — Decomposition Guard**: not triggered. There is a single root cause; the migration fixes the data that same defect already wrote.

**Step 7 — Report**
> Created <created-task-key>, which blocks ACME-520. Root cause: the division operands in `compute_risk_score` are swapped, and the inflated scores were already persisted to `assessments.risk_score`. The fix corrects the formula and adds a Diesel data migration that repairs existing rows. Reproducer: assert that `compute_risk_score(100, 5) == 0.05`.
>
> Run `/implement-task <created-task-key>` to implement the fix.
