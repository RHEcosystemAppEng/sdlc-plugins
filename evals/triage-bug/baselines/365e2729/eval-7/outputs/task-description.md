# Jira API Metadata (jira.create_issue parameters — not executed)

```
jira.create_issue(
  cloudId: "mock-cloud-id-for-eval",
  projectKey: "ACME",
  issueTypeName: "Task",
  summary: "Fix swapped operands in compute_risk_score and migrate persisted risk scores (ACME-520)",
  description: <task description body below>,
  additional_fields: {
    "labels": ["ai-generated-jira"]
  }
)
```

Follow-up operations (simulated):

- Step 5b: `jira.create_issue_link(link_type="Blocks", inward_issue_key=<created-task-key>, outward_issue_key="ACME-520")` — Task blocks Bug.
- Step 5c: re-fetch `<created-task-key>`, compute digest with `python3 scripts/sha256-digest.py`, post standalone comment `[sdlc-workflow] Description digest: <tagged-digest>` (no footnote).

---

## Repository
acme-backend

## Target Branch
main

## Description
Fixes ACME-520. `compute_risk_score()` divides total dependencies by vulnerable
dependencies instead of vulnerable by total, so every risk score is the reciprocal of
the correct value (100 total / 5 vulnerable produces `20.0` instead of `0.05`). The
score is persisted to `assessments.risk_score` at assessment creation time and is served
verbatim by `GET /api/v2/assessments/{id}`, so fixing the function alone only corrects
future assessments. This task fixes the computation and adds a data migration that
corrects all existing persisted risk scores.

## Files to Modify
- `modules/risk/src/score.rs` — swap division operands in `compute_risk_score` to `vulnerable_deps / total_deps` and guard `total_deps == 0`
- `modules/risk/tests/score_test.rs` — add reproducer test for `total != vulnerable` and edge-case tests

## Files to Create
- `migration/2026-11-26-000004_fix_inverted_risk_scores/up.sql` — data migration correcting existing `assessments.risk_score` values
- `migration/2026-11-26-000004_fix_inverted_risk_scores/down.sql` — reverse of the data correction

## Implementation Notes
Fixes ACME-520.

**Code fix** — `modules/risk/src/score.rs::compute_risk_score(total_deps: u32, vulnerable_deps: u32) -> f64`
currently returns `total_deps as f64 / vulnerable_deps as f64`. Change it to return
`vulnerable_deps as f64 / total_deps as f64`. When `total_deps == 0`, return `0.0`
instead of producing `NaN`. Keep the function signature unchanged — its sole caller,
`modules/risk/src/assessment.rs::create_assessment`, passes `(total_deps, vulnerable_deps)`
in the correct order and needs no change.

**Reproducer test** — add to `modules/risk/tests/score_test.rs`, following the existing
`test_risk_score_all_vulnerable` pattern (plain `#[test]` with `assert_eq!`):
- Input (from Steps to Reproduce): `compute_risk_score(100, 5)` — 100 total, 5 vulnerable.
- Before fix (Actual Result): returns `20.0`.
- After fix (Expected Result): must return `0.05`. Because `5.0 / 100.0` is an f64,
  prefer an epsilon comparison (e.g., `assert!((score - 0.05).abs() < f64::EPSILON)`) or
  `assert_eq!` if the value is exactly representable in the comparison used.
- Note: the existing test `compute_risk_score(10, 10) == 1.0` does not detect the bug
  because operand order does not matter for equal inputs — keep it, but do not rely on it.

**Data migration (persistence impact)** — the buggy value is written once at ingestion
time by `create_assessment` via
`diesel::insert_into(assessments::table).values((assessments::risk_score.eq(score), ...))`
into table `assessments`, column `risk_score` (`DOUBLE PRECISION`). It is never
recomputed: `modules/risk/src/endpoints.rs::get_assessment` reads the stored column
directly. Existing rows therefore hold the inverted value `total / vulnerable`.

Follow the existing Diesel migration convention in `migration/`
(`YYYY-MM-DD-NNNNNN_description/{up.sql,down.sql}`; latest is
`2024-03-10-000003_add_severity_column`), so the new migration is sequence `000004`.
Use `migration/2024-03-10-000003_add_severity_column/` as the structural reference.

Because the stored value is exactly the reciprocal of the correct value, the correction
can be computed from the persisted column alone (the `assessments` table does not store
the dependency counts):

- `up.sql`:
  - rows where `risk_score` is finite and non-zero → `risk_score = 1.0 / risk_score`
  - rows where `risk_score = 'Infinity'` (created with 0 vulnerable deps; correct value is 0) → `risk_score = 0.0`
  - rows where `risk_score = 'NaN'` (created with 0 total and 0 vulnerable deps) → `risk_score = 0.0`, matching the new `total_deps == 0` behavior
  - Perform all updates in a single `UPDATE assessments SET risk_score = CASE ... END`
    statement so each row is transformed exactly once (running the reciprocal twice
    would revert the fix).
- `down.sql`: apply the inverse — finite non-zero values → `1.0 / risk_score`; `0.0` →
  `'Infinity'`. Document that `NaN` rows collapsed to `0.0` cannot be restored exactly.

Only rows created before the code fix is deployed carry inverted values; deploy the
migration together with the code fix (same release) so no correctly computed rows get
inverted. If the code fix and migration cannot ship atomically, restrict the update
with `created_at < <deploy timestamp>`.

## Reuse Candidates
- `modules/risk/tests/score_test.rs::test_risk_score_all_vulnerable` — existing test pattern for `compute_risk_score`; mirror its structure for the reproducer
- `migration/2024-03-10-000003_add_severity_column/` — existing Diesel migration to follow for directory layout and `up.sql`/`down.sql` structure
- `migration/2024-02-20-000002_create_assessments/up.sql` — defines the `assessments` table and `risk_score` column targeted by the migration

## Acceptance Criteria
- [ ] Reproducer test `compute_risk_score(100, 5)` asserts `0.05` — fails before the fix (returns `20.0`) and passes after
- [ ] `compute_risk_score` returns `vulnerable_deps / total_deps` for all inputs
- [ ] `compute_risk_score` returns `0.0` when `total_deps == 0` (no `NaN`)
- [ ] New assessments created via `create_assessment` persist the correct `risk_score` (e.g., 100 total / 5 vulnerable → `0.05`)
- [ ] Existing records in `assessments.risk_score` with incorrect persisted values are corrected by the data migration (e.g., `20.0` → `0.05`, `Infinity` → `0.0`)
- [ ] Migration follows the Diesel `migration/YYYY-MM-DD-NNNNNN_description/` convention and includes `up.sql` and `down.sql`
- [ ] No regression in existing tests (including `test_risk_score_all_vulnerable`)

## Test Requirements
- [ ] Reproducer: in `modules/risk/tests/score_test.rs`, assert `compute_risk_score(100, 5)` equals `0.05` (Steps to Reproduce: 100 total, 5 vulnerable; Actual `20.0`, Expected `0.05`)
- [ ] Asymmetric-case test: e.g., `compute_risk_score(10, 1)` equals `0.1`, confirming operand order
- [ ] Edge case: `compute_risk_score(100, 0)` equals `0.0`
- [ ] Edge case: `compute_risk_score(0, 0)` equals `0.0` (not `NaN`)
- [ ] Migration test: seed `assessments` rows with `risk_score` values `20.0`, `1.0`, `'Infinity'`, `'NaN'`; after running `up.sql` they equal `0.05`, `1.0`, `0.0`, `0.0`

## Verification Commands
- `cargo test -p risk` (or `cargo test` in `modules/risk`) — all tests pass, including the new reproducer
- `diesel migration run` followed by `diesel migration redo` — migration applies and reverts cleanly
- `curl http://localhost:8080/api/v2/assessments/{id}` for an assessment of an SBOM with 100 deps / 5 vulnerable — `risk_score` is `0.05`

## Bug Context

- **Bug**: [ACME-520](https://mock-jira.example.com/browse/ACME-520)
- **Steps to Reproduce**: Ingest an SBOM with 100 total dependencies (5 vulnerable), create a risk assessment, retrieve it via `GET /api/v2/assessments/{id}`, and inspect `risk_score`.
- **Expected Result**: `risk_score` is `5 / 100 = 0.05` (vulnerable / total).
- **Actual Result**: `risk_score` is `100 / 5 = 20.0` (total / vulnerable) — numerator and denominator swapped.
- **Root Cause**: `modules/risk/src/score.rs::compute_risk_score` divides `total_deps` by `vulnerable_deps` (operands swapped). The result is persisted at creation time to `assessments.risk_score` by `create_assessment` and never recomputed, so existing records are stale and require a data migration.
