# Steps 2–3 — Reproduce/Trace and Codebase Investigation (ACME-520)

## Step 2 — Reproduce/Trace

### Runnable reproduction

The Steps to Reproduce require a running acme-backend service with a database
(ingest an SBOM, create an assessment, call `GET /api/v2/assessments/{id}`). No
such environment is available to this triage session, so direct reproduction was
not attempted. Outcome: **environment-dependent** — switched to code-path tracing.

### Code-path trace

Entry point: `GET /api/v2/assessments/{id}` (Step 3 of Steps to Reproduce).

1. `modules/risk/src/endpoints.rs::get_assessment` — loads the row with
   `assessments::table.find(id).first::<Assessment>(...)` and serializes it as-is.
   It does **not** compute the score; it returns the persisted `risk_score` column.
2. The `risk_score` column is written by
   `modules/risk/src/assessment.rs::create_assessment`, which calls
   `compute_risk_score(total_deps, vulnerable_deps)` and inserts the result.
3. `modules/risk/src/score.rs::compute_risk_score` returns
   `total_deps as f64 / vulnerable_deps as f64`.

Divergence point: `compute_risk_score` — with inputs `(100, 5)` it returns
`100 / 5 = 20.0` instead of `5 / 100 = 0.05`. This exactly matches the reported
Actual Result vs Expected Result.

## Step 3 — Codebase Investigation

### Target repository

- Component `risk-engine` and the paths in the description point to the risk module.
- Repository Registry: `acme-backend` (Path `/home/dev/repos/acme-backend`, Serena
  instance `serena_backend`).
- Code Intelligence section states no Serena MCP servers are configured, so the
  investigation uses the Read/Grep/Glob fallback (simulated via
  `repo-context-persistence-mock.md`).

### Affected files and symbols

| File | Symbol | Role |
|---|---|---|
| `modules/risk/src/score.rs` | `compute_risk_score(total_deps: u32, vulnerable_deps: u32) -> f64` | **Defect location** — operands of the division are swapped |
| `modules/risk/src/assessment.rs` | `create_assessment(conn, sbom_id, total_deps, vulnerable_deps)` | Sole caller found; persists the computed score via Diesel `insert_into(assessments::table)` |
| `modules/risk/src/endpoints.rs` | `get_assessment(path, db)` | Read path for `GET /api/v2/assessments/{id}`; returns persisted value, no recomputation |
| `modules/risk/tests/score_test.rs` | `test_risk_score_all_vulnerable` | Existing unit test; uses `(10, 10)` so it passes regardless of operand order — gap in coverage |

### Impact analysis (callers / references)

- `compute_risk_score` → referenced by `create_assessment` (via `use crate::score::compute_risk_score`).
- `create_assessment` → writes to `assessments` table.
- `assessments.risk_score` → read by `get_assessment` (API `GET /api/v2/assessments/{id}`).
- No other callers of `compute_risk_score` were identified in the repository context.

### Existing test patterns

- `modules/risk/tests/score_test.rs` uses plain `#[test]` functions calling
  `compute_risk_score(...)` directly with `assert_eq!` on the returned `f64`. The
  reproducer test should follow this file and pattern.
- No test exercises `total_deps != vulnerable_deps`, which is why the bug was not caught.

### Reuse candidates

- `modules/risk/src/score.rs::compute_risk_score` — fix in place; no new helper needed.
- `modules/risk/tests/score_test.rs` — add reproducer test alongside the existing test.
- `migration/2024-02-20-000002_create_assessments/` — defines the `assessments`
  table; reference for table/column names in the data migration.
- `migration/2024-03-10-000003_add_severity_column/` — most recent migration;
  reference for Diesel `up.sql`/`down.sql` layout.

### CONVENTIONS.md lookup

`/home/dev/repos/acme-backend/CONVENTIONS.md` — **not present**. No repository
conventions to apply beyond the observed patterns (Diesel migrations, `#[test]`
unit tests in `modules/<module>/tests/`).

### Edge case observed

`compute_risk_score` performs unchecked floating-point division. Currently
`vulnerable_deps == 0` yields `+inf`; after the fix, `total_deps == 0` yields `NaN`
(0/0). This should be handled as part of the fix (e.g., return `0.0` when
`total_deps == 0`), and is relevant to the data migration (existing rows with
`vulnerable_deps == 0` currently hold `Infinity`).

## Persistence-Impact Analysis

### Trace from buggy function to persistence boundary

```
compute_risk_score(total_deps, vulnerable_deps)          // modules/risk/src/score.rs
  -> let score = compute_risk_score(...)                 // modules/risk/src/assessment.rs::create_assessment
  -> diesel::insert_into(assessments::table)
       .values(assessments::risk_score.eq(score), ...)   // PERSISTENCE BOUNDARY
```

Read path: `GET /api/v2/assessments/{id}` → `endpoints.rs::get_assessment` →
`assessments::table.find(id).first::<Assessment>()` → returns stored `risk_score`
without recomputation.

### Result: persistence boundary FOUND

| Item | Value |
|---|---|
| Table | `assessments` |
| Column | `risk_score` (`DOUBLE PRECISION`) |
| Write operation | `modules/risk/src/assessment.rs::create_assessment` — `diesel::insert_into(assessments::table).values((..., assessments::risk_score.eq(score), ...))` |
| Write timing | **Ingestion time** — written once when the assessment is created; never recomputed on read or updated afterwards |
| Consequence | Fixing `compute_risk_score()` corrects only future assessments. Every existing row in `assessments` holds the inverted value (`total / vulnerable`) and will remain stale indefinitely. **A data migration is required.** |

### Migration convention discovered

- Directory: `migration/` (Diesel)
- Naming: `YYYY-MM-DD-NNNNNN_description/` with `up.sql` and `down.sql`
- Existing: `2024-01-15-000001_create_sboms`, `2024-02-20-000002_create_assessments`,
  `2024-03-10-000003_add_severity_column`
- Next migration: `migration/<YYYY-MM-DD>-000004_fix_inverted_risk_scores/{up.sql,down.sql}`

### Migration correction strategy

The `assessments` table stores only `risk_score` — not the dependency counts — so the
correct value cannot be recomputed from columns on the same row. Two options:

1. **Preferred if source counts are available**: recompute
   `vulnerable_deps / total_deps` from the SBOM's dependency/vulnerability data
   joined via `assessments.sbom_id → sboms.id` (implementer must confirm the source
   tables that hold these counts).
2. **Algebraic inversion** (always possible, since the stored value is exactly
   `total / vulnerable`): correct value = `1.0 / risk_score`, with special cases:
   - `risk_score = 'Infinity'` (vulnerable = 0) → correct value `0.0`
   - `risk_score = 'NaN'` (total = 0 and vulnerable = 0) → correct value `0.0`
   - `risk_score = 1.0` (total = vulnerable) → unchanged
