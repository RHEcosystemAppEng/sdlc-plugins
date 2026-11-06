# Steps 2-3 — Reproduction/Trace and Codebase Investigation (ACME-520)

## Step 2 — Reproduce / Trace

### Runnable reproduction

The Steps to Reproduce involve ingesting an SBOM, creating an assessment, and calling
`GET /api/v2/assessments/{id}` against a running service with a database. No running
environment is available (and the skill is read-only), so direct reproduction was
not attempted. Outcome: **environment-dependent — traced via code instead**.

### Code-path trace

Entry point: `GET /api/v2/assessments/{id}` (Step 3 of reproduction), but the value is
produced earlier, at assessment creation (Step 2 of reproduction).

1. **Assessment creation** — `modules/risk/src/assessment.rs::create_assessment(conn, sbom_id, total_deps, vulnerable_deps)`
   calls `compute_risk_score(total_deps, vulnerable_deps)`.
2. **Score computation** — `modules/risk/src/score.rs::compute_risk_score(total_deps: u32, vulnerable_deps: u32) -> f64`
   returns `total_deps as f64 / vulnerable_deps as f64`.
   With the reproduction inputs (`total_deps = 100`, `vulnerable_deps = 5`) this yields
   `100 / 5 = 20.0`. **This is the divergence point** — the expected value is
   `5 / 100 = 0.05`.
3. **Persistence** — `create_assessment` writes the score with
   `diesel::insert_into(assessments::table).values((..., assessments::risk_score.eq(score), ...))`.
4. **Retrieval** — `modules/risk/src/endpoints.rs::get_assessment` loads the row with
   `assessments::table.find(id).first::<Assessment>(...)` and serializes it directly;
   `risk_score` is returned as stored (`20.0`), never recomputed.

The trace exactly reproduces the reported Actual Result (`20.0`).

## Step 3 — Codebase Investigation

### Target repository

- Component `risk-engine` and the `compute_risk_score()` symbol named in the bug map to
  **acme-backend** (Repository Registry: Serena instance `serena_backend`, path
  `/home/dev/repos/acme-backend`).
- Code Intelligence section states no Serena MCP servers are configured, so the
  Read/Grep/Glob fallback is used (in this eval, the repository context mock).

### Affected files and symbols

| File | Symbol | Role |
|---|---|---|
| `modules/risk/src/score.rs` | `compute_risk_score` | **Defect** — division operands swapped |
| `modules/risk/src/assessment.rs` | `create_assessment` | Only caller found; persists the score into `assessments.risk_score` |
| `modules/risk/src/endpoints.rs` | `get_assessment` | Reads persisted `risk_score` and returns it unchanged |
| `migration/2024-02-20-000002_create_assessments/` | — | Defines the `assessments` table |

### Existing tests and patterns

- `modules/risk/tests/score_test.rs::test_risk_score_all_vulnerable` — asserts
  `compute_risk_score(10, 10) == 1.0`. This passes even with the bug because the
  operands are equal; **no test covers `total != vulnerable`**, which is why the bug
  went undetected. New reproducer test belongs in this file, following the same
  `#[test]` + `assert_eq!` style.

### Edge cases noted

- Current code: `vulnerable_deps = 0` produces `total / 0.0 = +Infinity` (f64 division,
  no panic). Such rows may exist in the DB as `Infinity`.
- After the fix: `total_deps = 0` would produce `0 / 0 = NaN` (or `x / 0 = Infinity`).
  The fix should define behavior for `total_deps == 0` (e.g., return `0.0`).

### Reuse candidates

- `modules/risk/src/score.rs::compute_risk_score` — fix in place; no new helper needed.
- `modules/risk/tests/score_test.rs` — existing test module / assertion style.
- `migration/` Diesel migration directories — pattern for the data migration.

### CONVENTIONS.md

The repository has no `CONVENTIONS.md` at its root. No additional conventions applied;
existing code patterns (Diesel, `#[test]` unit tests, Diesel migration layout) are used
as the reference instead.

## Persistence-impact analysis

### Trace from buggy function to persistence boundary

```
compute_risk_score(total_deps, vulnerable_deps)          [modules/risk/src/score.rs]
  -> let score = compute_risk_score(...)                  [modules/risk/src/assessment.rs::create_assessment]
  -> diesel::insert_into(assessments::table)
       .values(assessments::risk_score.eq(score))          -- PERSISTENCE BOUNDARY FOUND
```

Read path (confirms no recomputation):

```
GET /api/v2/assessments/{id}
  -> endpoints.rs::get_assessment
  -> assessments::table.find(id).first::<Assessment>()    -- returns stored risk_score as-is
```

### Findings (carried forward to Step 5)

| Item | Value |
|---|---|
| Persistence boundary found? | **Yes** |
| Table | `assessments` |
| Column | `risk_score` (`DOUBLE PRECISION`) |
| Write location | `modules/risk/src/assessment.rs::create_assessment` (`diesel::insert_into(assessments::table)`) |
| Write timing | **Ingestion time** — written once when the assessment is created; never updated or recomputed on read |
| Read location | `modules/risk/src/endpoints.rs::get_assessment` (reads stored value directly) |
| Consequence | Fixing `compute_risk_score()` only corrects **future** assessments. Every existing `assessments` row created before the fix holds an inflated (inverted) score and will never self-correct. **A data migration is required.** |

### Migration convention discovered

- Directory: `migration/`
- Existing entries:
  - `2024-01-15-000001_create_sboms/{up.sql,down.sql}`
  - `2024-02-20-000002_create_assessments/{up.sql,down.sql}`
  - `2024-03-10-000003_add_severity_column/{up.sql,down.sql}`
- Convention: Diesel, `YYYY-MM-DD-NNNNNN_description/` containing `up.sql` and `down.sql`,
  with a monotonically increasing six-digit sequence. Next migration should use sequence
  `000004`, e.g. `migration/<YYYY-MM-DD>-000004_fix_assessment_risk_score/`.

### Migration data strategy

The `assessments` table stores only `sbom_id`, `risk_score`, and `created_at` — the
original `total_deps` / `vulnerable_deps` inputs are not stored on the row. Two options:

1. **Recompute from source data** (preferred if dependency/vulnerability counts per
   SBOM are derivable from the `sboms` and related tables via `sbom_id`): set
   `risk_score = vulnerable_count / total_count`.
2. **Mathematical inversion** (always available): since the buggy value is
   `total / vulnerable` and the correct value is `vulnerable / total`, the correct
   score is exactly the reciprocal of the stored score:
   - `risk_score > 0` and finite -> `1.0 / risk_score`
   - `risk_score = 'Infinity'` (vulnerable = 0) -> `0.0`
   - `risk_score = 'NaN'` (total = 0 and vulnerable = 0) -> `0.0` (matches the fix's
     zero-total behavior)
   The reciprocal is self-inverse, so `down.sql` can apply the same transformation.
