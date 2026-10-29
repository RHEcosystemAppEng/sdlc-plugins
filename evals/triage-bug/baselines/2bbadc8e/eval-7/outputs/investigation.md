# Steps 2-3 -- Codebase Investigation: ACME-520

## Step 2 -- Reproduce/Trace

### Code-path tracing

The Steps to Reproduce describe an API-level scenario (SBOM ingestion followed by assessment retrieval) that cannot be directly executed in this environment. Code-path tracing was performed instead.

**Entry point**: SBOM ingestion triggering risk assessment creation, followed by retrieval via `GET /api/v2/assessments/{id}`.

**Trace path**:

1. An SBOM with 100 total dependencies (5 vulnerable) is ingested.
2. `create_assessment()` in `modules/risk/src/assessment.rs` is called with `total_deps=100, vulnerable_deps=5`.
3. `create_assessment()` calls `compute_risk_score(100, 5)` in `modules/risk/src/score.rs`.
4. `compute_risk_score()` computes `total_deps as f64 / vulnerable_deps as f64` = `100.0 / 5.0` = `20.0`.
5. The correct computation should be `vulnerable_deps as f64 / total_deps as f64` = `5.0 / 100.0` = `0.05`.
6. The result `20.0` is persisted to the `assessments` table via `diesel::insert_into(assessments::table)`.
7. `GET /api/v2/assessments/{id}` in `modules/risk/src/endpoints.rs` reads the persisted `risk_score` directly from the database and returns it as JSON.

**Divergence point**: The division operands in `compute_risk_score()` are swapped -- numerator and denominator are reversed, producing `total / vulnerable` instead of `vulnerable / total`.

**Reproduction outcome**: Confirmed via code-path tracing. The bug is deterministic and affects all assessments where `total_deps != vulnerable_deps`.

## Step 3 -- Codebase Investigation

### Target repository

- **Repository**: acme-backend
- **Role**: Rust backend service
- **Serena Instance**: serena_backend (per Repository Registry, but Code Intelligence notes indicate no Serena MCP servers are configured)
- **Path**: /home/dev/repos/acme-backend

Investigation performed using Read/Grep/Glob fallback (no Serena available).

### Affected files and symbols

| File | Symbol | Role |
|------|--------|------|
| `modules/risk/src/score.rs` | `compute_risk_score()` | Buggy function -- division operands swapped |
| `modules/risk/src/assessment.rs` | `create_assessment()` | Caller that persists the buggy result to database |
| `modules/risk/src/endpoints.rs` | `get_assessment()` | Query endpoint that reads persisted value (does NOT recompute) |

### Existing test files

| File | Test | Observation |
|------|------|-------------|
| `modules/risk/tests/score_test.rs` | `test_risk_score_all_vulnerable` | Uses `compute_risk_score(10, 10)` -- passes with the bug because `10/10 = 1.0` regardless of operand order. No test exercises `total != vulnerable`. |

### CONVENTIONS.md lookup

No `CONVENTIONS.md` file found at the repository root (`/home/dev/repos/acme-backend`).

### Database schema

**Table**: `assessments`

| Column | Type | Description |
|--------|------|-------------|
| id | BIGSERIAL | Primary key |
| sbom_id | BIGINT | Foreign key to sboms table |
| risk_score | DOUBLE PRECISION | Computed risk score (persisted at creation) |
| created_at | TIMESTAMPTZ | Creation timestamp |

### Existing migrations

```
migration/
+-- 2024-01-15-000001_create_sboms/
|   +-- up.sql
|   +-- down.sql
+-- 2024-02-20-000002_create_assessments/
|   +-- up.sql
|   +-- down.sql
+-- 2024-03-10-000003_add_severity_column/
    +-- up.sql
    +-- down.sql
```

Migration naming convention: `YYYY-MM-DD-NNNNNN_description/up.sql` (Diesel convention).

## Persistence-Impact Analysis

### Trace: compute_risk_score() output to persistence boundary

```
compute_risk_score(total_deps, vulnerable_deps)     -- modules/risk/src/score.rs
  -> returns f64 (the buggy score)
    -> assigned to `score` in create_assessment()   -- modules/risk/src/assessment.rs
      -> diesel::insert_into(assessments::table)
           .values(assessments::risk_score.eq(score))  -- PERSISTENCE BOUNDARY
```

### Persistence boundary found

- **Table**: `assessments`
- **Column**: `risk_score` (DOUBLE PRECISION)
- **Write operation**: `diesel::insert_into(assessments::table)` in `create_assessment()` at `modules/risk/src/assessment.rs`
- **Write timing**: Ingestion time (when the assessment is first created). The `risk_score` is computed once during `create_assessment()` and written to the database. It is NOT recomputed on read.

### Impact on existing data

All existing assessments in the `assessments` table have incorrect `risk_score` values where `total_deps != vulnerable_deps`. The stored values are inflated because the operands are swapped (`total / vulnerable` instead of `vulnerable / total`).

Fixing `compute_risk_score()` alone will only correct **future** assessments. **Existing assessments retain the wrong score** because `GET /api/v2/assessments/{id}` reads the persisted value directly from the database without recomputing.

### Data migration required

A data migration is needed to correct existing `risk_score` values in the `assessments` table. The migration must recompute `risk_score` using the correct formula (`vulnerable_deps / total_deps`) from the source SBOM data linked via `sbom_id`.
