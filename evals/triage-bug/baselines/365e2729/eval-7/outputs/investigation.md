# Steps 2–3 — Reproduce/Trace and Codebase Investigation: ACME-520

## Step 2 — Reproduce/Trace

### Runnable reproduction

The Steps to Reproduce reference an API call (`GET /api/v2/assessments/{id}`), but they
require a running acme-backend service with an ingested SBOM and database. No such
environment is available in this session (and external tool usage is disallowed for
this eval), so outcome is: **environment-dependent — not directly reproduced**.
Falling back to code-path tracing.

### Code-path trace

Entry point: SBOM risk assessment creation (Step 2 of reproduction) followed by
retrieval via `GET /api/v2/assessments/{id}` (Steps 3–4).

1. **Assessment creation** — `modules/risk/src/assessment.rs::create_assessment(conn, sbom_id, total_deps, vulnerable_deps)`
   calls `compute_risk_score(total_deps, vulnerable_deps)`.
2. **Score computation** — `modules/risk/src/score.rs::compute_risk_score(total_deps: u32, vulnerable_deps: u32) -> f64`
   returns `total_deps as f64 / vulnerable_deps as f64`.
   With the reproduction inputs (100 total, 5 vulnerable) this yields `100 / 5 = 20.0`.
   **Divergence point**: expected `vulnerable_deps / total_deps = 5 / 100 = 0.05`.
3. **Persistence** — `create_assessment` inserts the score via
   `diesel::insert_into(assessments::table).values((..., assessments::risk_score.eq(score), ...))`.
4. **Retrieval** — `modules/risk/src/endpoints.rs::get_assessment` loads the row with
   `assessments::table.find(id).first::<Assessment>(...)` and serializes it directly as
   JSON. The `risk_score` returned is the persisted value; it is **not** recomputed.

The trace fully explains the Actual Result (`20.0`) reported in the bug.

## Step 3 — Codebase Investigation

### Target repository

- Component `risk-engine` and the symbol `compute_risk_score()` named in the description
  both point to the risk module of **acme-backend**.
- Registry: `acme-backend`, Serena instance `serena_backend`, path `/home/dev/repos/acme-backend`.
- Code Intelligence section states no Serena MCP servers are configured, so the
  Read/Grep/Glob fallback applies (findings sourced from repo-context-persistence-mock.md).

### Affected files and symbols

| File | Symbol | Role |
|---|---|---|
| `modules/risk/src/score.rs` | `compute_risk_score` | **Defect** — division operands reversed |
| `modules/risk/src/assessment.rs` | `create_assessment` | Sole caller found; persists result to DB |
| `modules/risk/src/endpoints.rs` | `get_assessment` | Read path; returns persisted `risk_score` verbatim |
| `modules/risk/tests/score_test.rs` | `test_risk_score_all_vulnerable` | Existing unit test; does not catch the bug |

### Impact analysis (callers / references)

- `compute_risk_score` → referenced by `create_assessment` (via `use crate::score::compute_risk_score;`).
- No other callers identified in the provided repository context.
- `get_assessment` does not reference `compute_risk_score` — it is a pure read of the
  stored column.

### Existing tests and patterns

- `modules/risk/tests/score_test.rs` contains `test_risk_score_all_vulnerable`, asserting
  `compute_risk_score(10, 10) == 1.0`. This passes with or without the bug because
  `10/10 == 10/10`. **No test exercises `total != vulnerable`**, which is why the bug
  shipped. The reproducer should be added to this file following the same plain
  `#[test]` + `assert_eq!` pattern.

### Edge cases noted

- `total_deps == 0`: after the fix, `0 / 0` → `NaN` in f64. Today, `vulnerable_deps == 0`
  produces `+Infinity` (`n / 0.0`). The fix should define behavior for `total_deps == 0`
  (e.g., return `0.0`), and the migration must handle rows currently holding `Infinity`
  or `NaN`.

### CONVENTIONS.md

The repository has no `CONVENTIONS.md` at its root — no additional conventions to apply.

### Existing migration pattern

Directory `migration/` (Diesel convention `YYYY-MM-DD-NNNNNN_description/{up.sql,down.sql}`):

```
migration/2024-01-15-000001_create_sboms/
migration/2024-02-20-000002_create_assessments/
migration/2024-03-10-000003_add_severity_column/
```

Next migration would be sequence `000004`, e.g.
`migration/2026-11-26-000004_fix_inverted_risk_scores/up.sql` and `down.sql`.

## Persistence-Impact Analysis

### Trace from buggy function to persistence boundary

`compute_risk_score()` (`modules/risk/src/score.rs`)
→ return value bound to `score` in `create_assessment()` (`modules/risk/src/assessment.rs`)
→ `diesel::insert_into(assessments::table).values((assessments::risk_score.eq(score), ...)).get_result(conn)`
— **persistence boundary found** at `assessments` table, `risk_score` column.

### Findings carried forward to Step 5

| Item | Value |
|---|---|
| Persistence boundary | **YES** |
| Table | `assessments` |
| Column | `risk_score` (`DOUBLE PRECISION`) |
| Write operation | `modules/risk/src/assessment.rs::create_assessment` — `diesel::insert_into(assessments::table)` |
| Write timing | **Ingestion time** — written once when the assessment is created; never updated or recomputed |
| Read path | `modules/risk/src/endpoints.rs::get_assessment` returns the stored value directly |

### Consequence

Fixing `compute_risk_score()` corrects only assessments created after the fix is
deployed. Every assessment already in the `assessments` table retains its inflated
(inverted) `risk_score`, and the value is never self-correcting because the read path
does not recompute. **A data migration is required** to correct existing records.

### Migration feasibility

The stored value is exactly `total / vulnerable`, so the correct value
`vulnerable / total` is its reciprocal. The `assessments` table does not store
`total_deps`/`vulnerable_deps`, but the reciprocal transformation recovers the correct
score from the persisted column alone:

- finite, non-zero `risk_score` → `1.0 / risk_score`
- `risk_score = 'Infinity'` (created with 0 vulnerable deps) → `0.0`
- `risk_score = 'NaN'` (created with 0 total and 0 vulnerable deps) → `0.0` (consistent with the new `total_deps == 0` handling)

If source dependency/vulnerability counts are available per SBOM, recomputing from
source is an acceptable alternative; the reciprocal approach is preferred because it
needs no joins and is exact.
