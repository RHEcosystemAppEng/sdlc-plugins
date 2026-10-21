# Steps 2-3 -- Codebase Investigation: ACME-520

## Step 2 -- Reproduce/Trace

### Code-path tracing

The Steps to Reproduce describe an API-driven workflow that cannot be directly
executed in this context. Tracing through the code paths instead.

**Entry point**: The reproduction path starts with ingesting an SBOM, creating a
risk assessment, and retrieving it via `GET /api/v2/assessments/{id}`.

**Trace through code**:

1. **Assessment creation** -- `create_assessment()` in `modules/risk/src/assessment.rs`
   is called with `total_deps=100` and `vulnerable_deps=5`.
2. **Score computation** -- `create_assessment()` calls `compute_risk_score(total_deps, vulnerable_deps)`
   in `modules/risk/src/score.rs`.
3. **Bug location** -- `compute_risk_score()` computes `total_deps as f64 / vulnerable_deps as f64`,
   which yields `100.0 / 5.0 = 20.0`. The correct formula is `vulnerable_deps as f64 / total_deps as f64`,
   which would yield `5.0 / 100.0 = 0.05`.
4. **Persistence** -- The incorrect score (`20.0`) is persisted via
   `diesel::insert_into(assessments::table)` with `assessments::risk_score.eq(score)`.
5. **Retrieval** -- `GET /api/v2/assessments/{id}` in `modules/risk/src/endpoints.rs`
   reads the persisted `risk_score` directly from the database without recomputing it.

**Trace finding**: The bug is confirmed. The numerator and denominator in
`compute_risk_score()` are swapped, producing reciprocal values. For the example
inputs (100 total, 5 vulnerable), the score is 20.0 instead of 0.05 -- a factor
of 400x inflation.

## Step 3 -- Codebase Investigation

### Target repository

- **Repository**: acme-backend (Rust backend service)
- **Component**: risk-engine (matches the Bug's Component field)
- **Serena Instance**: serena_backend
- **Path**: /home/dev/repos/acme-backend

### Affected files and symbols

| File | Symbol | Role |
|------|--------|------|
| `modules/risk/src/score.rs` | `compute_risk_score()` | Buggy function -- division operands swapped |
| `modules/risk/src/assessment.rs` | `create_assessment()` | Caller that persists the incorrect score |
| `modules/risk/src/endpoints.rs` | `get_assessment()` | Read endpoint returning persisted value |
| `modules/risk/tests/score_test.rs` | `test_risk_score_all_vulnerable()` | Existing test -- insufficient coverage |

### Existing test analysis

The existing test `test_risk_score_all_vulnerable()` in `modules/risk/tests/score_test.rs`
passes even with the bug because it uses `total=10, vulnerable=10` -- the result is
`1.0` regardless of operand order. No test exercises the asymmetric case where
`total != vulnerable`, which is why the bug was not caught.

### CONVENTIONS.md lookup

No `CONVENTIONS.md` file found at the repository root. No repository-specific
conventions to incorporate.

### Persistence-Impact Analysis

#### Trace: output to persistence boundary

```
compute_risk_score(total_deps, vulnerable_deps)     -- modules/risk/src/score.rs
  -> returns f64 (the incorrect score)
    -> let score = compute_risk_score(...)           -- modules/risk/src/assessment.rs::create_assessment()
      -> diesel::insert_into(assessments::table)
           .values(assessments::risk_score.eq(score))  -- PERSISTENCE BOUNDARY
```

#### Persistence boundary: FOUND

- **Table**: `assessments`
- **Column**: `risk_score` (type: `DOUBLE PRECISION`)
- **Write operation location**: `modules/risk/src/assessment.rs`, function `create_assessment()`
- **Write timing**: Ingestion time (assessment creation) -- the score is computed
  and persisted once when the assessment is first created. It is NOT recomputed on
  read.

#### Consequence

Fixing `compute_risk_score()` alone will only correct **future** assessments.
All **existing** assessments in the `assessments` table retain the incorrect
(inflated) `risk_score` values. A **data migration** is required to recompute
and correct the `risk_score` column for all existing rows.

#### Existing migration patterns

The repository uses Diesel migrations in the `migration/` directory following the
convention `YYYY-MM-DD-NNNNNN_description/up.sql`:

```
migration/
  2024-01-15-000001_create_sboms/up.sql
  2024-02-20-000002_create_assessments/up.sql
  2024-03-10-000003_add_severity_column/up.sql
```

The correction migration should follow this pattern, e.g.:
`migration/YYYY-MM-DD-NNNNNN_fix_risk_score_values/up.sql`

#### Migration logic

The migration must update every row in the `assessments` table, recomputing
`risk_score` from the source data. Since the original formula was inverted
(`total / vulnerable` instead of `vulnerable / total`), the correction is:

```sql
UPDATE assessments
SET risk_score = 1.0 / risk_score
WHERE risk_score != 0;
```

Alternatively, if joining with the source SBOM data to recompute from scratch:

```sql
UPDATE assessments a
SET risk_score = s.vulnerable_deps::double precision / s.total_deps::double precision
FROM sboms s
WHERE a.sbom_id = s.id
  AND s.total_deps > 0;
```

The join-based approach is more robust as it handles edge cases and does not
rely on the invertibility of the original incorrect values.
