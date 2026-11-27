# Steps 2–3 — Reproduce/Trace and Codebase Investigation (ACME-520)

## Step 2 — Reproduce/Trace

### Runnable reproduction

The Steps to Reproduce require a running acme-backend service with a database (SBOM
ingestion + assessment creation + `GET /api/v2/assessments/{id}`). No such environment
is available in this triage session, so direct reproduction was **not attempted**
(outcome: environment-dependent). Code-path tracing was used instead.

### Code-path trace

Entry point: `GET /api/v2/assessments/{id}` (Step 3 of the reproduction).

1. `modules/risk/src/endpoints.rs::get_assessment` — loads the row from
   `assessments::table.find(id)` and serializes it as JSON. It does **not** compute the
   score; it returns the persisted `risk_score` column verbatim.
2. The value in that column was written by
   `modules/risk/src/assessment.rs::create_assessment` (Step 2 of the reproduction),
   which calls `compute_risk_score(total_deps, vulnerable_deps)` and inserts the result.
3. `modules/risk/src/score.rs::compute_risk_score` returns
   `total_deps as f64 / vulnerable_deps as f64`.

Divergence point: `compute_risk_score` — for `total_deps = 100`, `vulnerable_deps = 5` it
returns `100 / 5 = 20.0` instead of the expected `5 / 100 = 0.05`. This matches the
reported Actual Result exactly.

## Step 3 — Codebase Investigation

### Target repository

- Component `risk-engine` and the referenced symbol `compute_risk_score()` / endpoint
  `/api/v2/assessments/{id}` map to **acme-backend** (only registered repository).
- Serena instance in the registry: `serena_backend`; however Code Intelligence states no
  Serena MCP servers are configured, so the Read/Grep/Glob fallback was used (simulated
  via `repo-context-persistence-mock.md`). Path: `/home/dev/repos/acme-backend`.

### Affected files and symbols

| File | Symbol | Role |
|---|---|---|
| `modules/risk/src/score.rs` | `compute_risk_score(total_deps: u32, vulnerable_deps: u32) -> f64` | **Defect** — operands swapped |
| `modules/risk/src/assessment.rs` | `create_assessment(conn, sbom_id, total_deps, vulnerable_deps)` | Sole caller found; persists the score |
| `modules/risk/src/endpoints.rs` | `get_assessment(path, db)` | Read path; returns persisted value, no recompute |

### Impact analysis (callers of `compute_risk_score`)

- `create_assessment` in `modules/risk/src/assessment.rs` (`use crate::score::compute_risk_score;`).
- No other callers identified in the provided context.

### Existing tests and patterns

- `modules/risk/tests/score_test.rs::test_risk_score_all_vulnerable` —
  `assert_eq!(compute_risk_score(10, 10), 1.0)`. This test passes with the bug because
  `10/10 == 1.0` regardless of operand order; there is **no test covering
  `total != vulnerable`**, which is why the defect went undetected.
- The reproducer test should be added to this same file following the same plain
  `#[test]` + `assert_eq!` pattern (use an approximate float comparison or exact values
  that are representable, e.g. `compute_risk_score(100, 5)` → `0.05`).

### Edge cases noted

- Current code: `vulnerable_deps == 0` yields `inf` (f64 division by zero).
- After fix: `total_deps == 0` would yield `NaN` (`0/0`). The fix should define behavior
  for `total_deps == 0` (e.g., return `0.0`) so no NaN is persisted.

### CONVENTIONS.md

No `CONVENTIONS.md` exists at the acme-backend root. Conventions inferred from existing
code: Diesel ORM, Rust unit tests in `modules/risk/tests/`, Diesel migrations in
`migration/`.

## Persistence-impact analysis

### Trace from buggy function to persistence boundary

```
compute_risk_score()                      (modules/risk/src/score.rs)
  → let score = compute_risk_score(...)   (modules/risk/src/assessment.rs::create_assessment)
  → diesel::insert_into(assessments::table)
        .values(assessments::risk_score.eq(score), ...)
  — PERSISTENCE BOUNDARY FOUND at `assessments` table, `risk_score` column
```

Read side: `modules/risk/src/endpoints.rs::get_assessment` reads `risk_score` directly
from `assessments` — no recomputation on read.

### Recorded findings (carried forward to Step 5)

| Item | Value |
|---|---|
| Table | `assessments` |
| Column | `risk_score` (`DOUBLE PRECISION`) |
| Write operation | `modules/risk/src/assessment.rs::create_assessment` — `diesel::insert_into(assessments::table)` |
| Write timing | **Ingestion time** — written once when the assessment is created; never recomputed or updated on access |
| Consequence | Every existing assessment row holds an inflated (inverted) score. Fixing the code only corrects new assessments; existing rows are stale and **not self-correcting** |
| Data migration needed | **Yes** |

### Migration conventions discovered

Directory `migration/` with Diesel-style migrations:

```
migration/
├── 2024-01-15-000001_create_sboms/{up.sql,down.sql}
├── 2024-02-20-000002_create_assessments/{up.sql,down.sql}
└── 2024-03-10-000003_add_severity_column/{up.sql,down.sql}
```

Naming convention: `YYYY-MM-DD-NNNNNN_description/up.sql` + `down.sql`. Next sequence
number: `000004`.

### Data-correction approach

Because the persisted value is exactly `total / vulnerable`, and the correct value is
`vulnerable / total`, the correct value is the reciprocal of the stored value:
`correct = 1.0 / risk_score` (for `risk_score > 0` and finite). Rows where the bug
produced `inf` (vulnerable = 0) should become `0.0` (0 vulnerable deps → zero risk).
Recomputing from source data (dependency counts derived from the `sboms` side) is
preferable if those counts are available in the database; the `assessments` table itself
does not store `total_deps` / `vulnerable_deps`, so the reciprocal transformation is
the reliable approach given only the schema shown. The implementer should confirm
whether source counts are queryable and prefer recomputation if so.
