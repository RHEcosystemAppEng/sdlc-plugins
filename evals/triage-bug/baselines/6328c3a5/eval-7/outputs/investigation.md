# Steps 2-3 -- Codebase Investigation: ACME-520

## Step 2 -- Reproduce/Trace

### Reproduction approach

The Steps to Reproduce reference API calls (`GET /api/v2/assessments/{id}`) and an SBOM ingestion pipeline. Direct reproduction is not possible without a running environment. Code-path tracing is used instead.

### Code-path trace

**Entry point**: SBOM ingestion triggers risk assessment creation.

1. An SBOM with 100 total dependencies (5 vulnerable) is ingested.
2. `create_assessment()` in `modules/risk/src/assessment.rs` is called, which invokes `compute_risk_score(total_deps, vulnerable_deps)`.
3. `compute_risk_score()` in `modules/risk/src/score.rs` computes `total_deps as f64 / vulnerable_deps as f64` -- the operands are swapped.
4. For the test case (total=100, vulnerable=5): `100 / 5 = 20.0` instead of `5 / 100 = 0.05`.
5. The incorrect score (20.0) is persisted to the `assessments` table via `diesel::insert_into`.
6. `GET /api/v2/assessments/{id}` in `modules/risk/src/endpoints.rs` reads the persisted value directly from the database -- it does NOT recompute the score.

**Trace outcome**: Bug confirmed via code-path analysis. The numerator and denominator are swapped in the division expression.

## Step 3 -- Codebase Investigation

### Target repository

- **Repository**: acme-backend (Rust backend service)
- **Serena instance**: serena_backend (not available -- no Serena MCP configured)
- **Path**: /home/dev/repos/acme-backend
- **Fallback**: Read/Grep/Glob tools used for investigation

### Affected files and symbols

| File | Symbol | Role |
|------|--------|------|
| `modules/risk/src/score.rs` | `compute_risk_score()` | Buggy function -- division operands swapped |
| `modules/risk/src/assessment.rs` | `create_assessment()` | Caller that persists the result to database |
| `modules/risk/src/endpoints.rs` | `get_assessment()` | API endpoint that reads persisted value |

### Database schema

**Table**: `assessments`

| Column | Type | Description |
|--------|------|-------------|
| id | BIGSERIAL | Primary key |
| sbom_id | BIGINT | Foreign key to sboms table |
| risk_score | DOUBLE PRECISION | Computed risk score (persisted at creation) |
| created_at | TIMESTAMPTZ | Creation timestamp |

### Existing test analysis

**File**: `modules/risk/tests/score_test.rs`

```rust
#[test]
fn test_risk_score_all_vulnerable() {
    let score = compute_risk_score(10, 10);
    assert_eq!(score, 1.0);
}
```

This test passes even with the bug because `10 / 10 = 1.0` regardless of operand order. No test exercises the asymmetric case where `total != vulnerable`, which is why the bug was not caught.

### CONVENTIONS.md lookup

The repository does not have a CONVENTIONS.md at its root. No repository-specific conventions apply.

### Migration conventions

**Directory**: `migration/`

Existing migrations follow the Diesel convention: `YYYY-MM-DD-NNNNNN_description/up.sql` with corresponding `down.sql`.

```
migration/
  2024-01-15-000001_create_sboms/
  2024-02-20-000002_create_assessments/
  2024-03-10-000003_add_severity_column/
```

Next migration should use sequential numbering after `000003` with a descriptive name.

## Persistence-Impact Analysis

### Trace: buggy output to persistence boundary

```
compute_risk_score(total_deps, vulnerable_deps)     [modules/risk/src/score.rs]
  -> return value assigned to `score`
    -> create_assessment()                            [modules/risk/src/assessment.rs]
      -> diesel::insert_into(assessments::table)
           .values(assessments::risk_score.eq(score))  <-- PERSISTENCE BOUNDARY
```

### Persistence boundary found

- **Table**: `assessments`
- **Column**: `risk_score`
- **Write operation location**: `modules/risk/src/assessment.rs`, function `create_assessment()`
- **Write timing**: Ingestion time (once, when assessment is first created)
- **Recomputed on read?**: No -- `get_assessment()` reads persisted value directly from the database

### Impact

The incorrect risk score is written to the `assessments.risk_score` column at ingestion time and is never recomputed. Fixing `compute_risk_score()` alone will only correct **future** assessments. All **existing** assessments retain the inflated, incorrect risk score.

**A data migration is required** to recompute and correct `risk_score` for all existing records in the `assessments` table.
