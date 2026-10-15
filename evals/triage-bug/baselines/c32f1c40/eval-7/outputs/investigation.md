# Steps 2-3 -- Codebase Investigation: ACME-520

## Step 2 -- Reproduce/Trace

### Code-path tracing

The bug cannot be directly reproduced in this environment (no running service),
so we trace the code path described in the Steps to Reproduce.

**Entry point**: The Steps to Reproduce describe ingesting an SBOM and creating
a risk assessment. The code path flows through these symbols:

1. **SBOM ingestion** with 100 total dependencies, 5 vulnerable.
2. **`create_assessment()`** in `modules/risk/src/assessment.rs` is called with
   `total_deps = 100` and `vulnerable_deps = 5`.
3. **`compute_risk_score(total_deps=100, vulnerable_deps=5)`** in
   `modules/risk/src/score.rs` is called by `create_assessment()`.
4. The buggy function computes `total_deps / vulnerable_deps = 100 / 5 = 20.0`
   instead of the correct `vulnerable_deps / total_deps = 5 / 100 = 0.05`.
5. The inflated score `20.0` is written to the `assessments` table via Diesel
   `insert_into`.
6. **`GET /api/v2/assessments/{id}`** in `modules/risk/src/endpoints.rs` reads
   the persisted `risk_score` directly from the database -- it does NOT
   recompute. The caller sees `20.0`.

**Trace outcome**: The bug is confirmed by code-path analysis. The division
operands in `compute_risk_score()` are reversed.

## Step 3 -- Codebase Investigation

### Target repository

- **Repository**: acme-backend
- **Component**: risk-engine
- **Path**: /home/dev/repos/acme-backend
- **Serena Instance**: serena_backend (Code Intelligence not available per CLAUDE.md)

Since no Serena instance is operationally available, investigation used Read/Grep/Glob
fallback on the repository context.

### Affected files and symbols

| File | Symbol | Role |
|------|--------|------|
| `modules/risk/src/score.rs` | `compute_risk_score()` | Buggy function -- division operands reversed |
| `modules/risk/src/assessment.rs` | `create_assessment()` | Caller that persists the buggy result |
| `modules/risk/src/endpoints.rs` | `get_assessment()` | Read endpoint -- returns persisted value, no recomputation |

### Database schema

- **Table**: `assessments`
- **Column**: `risk_score` (DOUBLE PRECISION)
- **Other columns**: `id` (BIGSERIAL PK), `sbom_id` (BIGINT FK), `created_at` (TIMESTAMPTZ)

### Existing test analysis

- **File**: `modules/risk/tests/score_test.rs`
- **Test**: `test_risk_score_all_vulnerable` -- tests `compute_risk_score(10, 10)`
  which equals `1.0` regardless of operand order.
- **Gap**: No test exercises the case where `total_deps != vulnerable_deps`.
  This is exactly the scenario described in the bug report (100 total, 5 vulnerable).

### CONVENTIONS.md

No CONVENTIONS.md found at the repository root.

### Existing migration pattern

- **Directory**: `migration/`
- **Naming convention**: Diesel convention `YYYY-MM-DD-NNNNNN_description/up.sql`
- **Latest migration**: `2024-03-10-000003_add_severity_column/up.sql`

---

## Persistence-Impact Analysis

### Trace: compute_risk_score() output to persistence boundary

```
compute_risk_score(total_deps, vulnerable_deps)
  -> returns f64 score
    -> create_assessment() binds score to assessments::risk_score
      -> diesel::insert_into(assessments::table).values(risk_score.eq(score))
        -> PERSISTENCE BOUNDARY: assessments table, risk_score column
```

### Persistence boundary details

| Property | Value |
|----------|-------|
| Table name | `assessments` |
| Column | `risk_score` (DOUBLE PRECISION) |
| Write operation location | `modules/risk/src/assessment.rs`, `create_assessment()` |
| Write timing | **Ingestion time** -- written once when the assessment is first created |
| Recomputed on read? | **No** -- `get_assessment()` reads directly from DB |

### Impact

Because `risk_score` is written at ingestion time and never recomputed on read,
**all existing assessments in the database contain incorrect (inflated) risk scores**.
Fixing `compute_risk_score()` alone will only correct **future** assessments.
Existing assessments retain the wrong score until a data migration corrects them.

### Migration requirement

A data migration is required to:

1. Recompute all existing `risk_score` values in the `assessments` table.
2. The correct formula is `vulnerable_deps / total_deps` (instead of the
   current `total_deps / vulnerable_deps`).
3. Since the `assessments` table stores `risk_score` but not the original
   `total_deps` and `vulnerable_deps` values separately, the migration must
   join with the source data (the `sboms` table or related vulnerability data)
   to recompute the correct scores. Alternatively, if the original ratio can be
   inverted (`1.0 / old_score` where `old_score != 0`), that provides a
   mathematical shortcut -- but this must be validated against edge cases
   (e.g., `risk_score = 0` when `total_deps = 0`).
