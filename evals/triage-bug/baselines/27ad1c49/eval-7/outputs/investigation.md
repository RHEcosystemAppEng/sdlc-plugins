# Steps 2-3 -- Codebase Investigation

## Step 2 -- Reproduce/Trace

### Code-path tracing

The Steps to Reproduce describe a flow that exercises the risk scoring pipeline
end-to-end. Since direct execution is not available, the code paths were traced
through the codebase.

**Entry point**: SBOM ingestion followed by risk assessment creation.

**Trace**:

1. **`compute_risk_score(total_deps, vulnerable_deps)`** in `modules/risk/src/score.rs`
   - Receives `total_deps = 100`, `vulnerable_deps = 5`
   - Computes `total_deps as f64 / vulnerable_deps as f64` = `100.0 / 5.0` = `20.0`
   - **Expected**: `vulnerable_deps as f64 / total_deps as f64` = `5.0 / 100.0` = `0.05`
   - **Divergence found here**: the numerator and denominator are swapped

2. **`create_assessment(conn, sbom_id, total_deps, vulnerable_deps)`** in `modules/risk/src/assessment.rs`
   - Calls `compute_risk_score(total_deps, vulnerable_deps)` and receives the incorrect value `20.0`
   - Persists it via `diesel::insert_into(assessments::table)` into the `risk_score` column

3. **`GET /api/v2/assessments/{id}`** in `modules/risk/src/endpoints.rs`
   - Reads the persisted `risk_score` directly from the database
   - Does NOT recompute the score -- returns the stale/incorrect value

**Trace outcome**: Bug confirmed through code-path analysis. The division operands
are reversed in `compute_risk_score()`, producing a reciprocal of the intended score.

## Step 3 -- Codebase Investigation

### Target repository

- **Repository**: acme-backend
- **Role**: Rust backend service
- **Path**: /home/dev/repos/acme-backend

### Affected files and symbols

| File | Symbol | Role |
|------|--------|------|
| `modules/risk/src/score.rs` | `compute_risk_score()` | Buggy function -- swapped division operands |
| `modules/risk/src/assessment.rs` | `create_assessment()` | Caller that persists the incorrect score |
| `modules/risk/src/endpoints.rs` | `get_assessment()` | Read endpoint -- returns persisted value without recomputing |

### Existing test analysis

**File**: `modules/risk/tests/score_test.rs`

The existing test `test_risk_score_all_vulnerable()` uses `compute_risk_score(10, 10)`,
which produces `1.0` regardless of operand order (`10/10 = 1.0` either way). This
test is insufficient to detect the bug -- it does not exercise the case where
`total_deps != vulnerable_deps`.

### CONVENTIONS.md

No `CONVENTIONS.md` found at the repository root.

### Persistence-impact analysis

**Trace of buggy output to persistence boundary**:

```
compute_risk_score(total_deps, vulnerable_deps)   -- modules/risk/src/score.rs
  |
  v  (return value: f64)
create_assessment(conn, sbom_id, total_deps, vulnerable_deps)   -- modules/risk/src/assessment.rs
  |
  v  (uses score in insert)
diesel::insert_into(assessments::table)
  .values(assessments::risk_score.eq(score))   -- PERSISTENCE BOUNDARY
```

**Persistence boundary found**:

- **Table**: `assessments`
- **Column**: `risk_score` (type: `DOUBLE PRECISION`)
- **Write operation location**: `modules/risk/src/assessment.rs`, `create_assessment()` function
- **Write timing**: Ingestion time -- the risk score is computed and written once when the assessment is first created. It is NOT recomputed on read.

**Conclusion**: A data migration IS needed. Fixing `compute_risk_score()` alone
will only correct future assessments. All existing assessments in the `assessments`
table have incorrect `risk_score` values (the reciprocal of the correct value).
The migration must recompute and update these values.

### Database schema

**Table: assessments**

| Column | Type | Description |
|--------|------|-------------|
| id | BIGSERIAL | Primary key |
| sbom_id | BIGINT | Foreign key to sboms table |
| risk_score | DOUBLE PRECISION | Computed risk score (persisted at creation) |
| created_at | TIMESTAMPTZ | Creation timestamp |

### Migration convention

Existing migrations follow the Diesel convention in the `migration/` directory:

```
migration/
  YYYY-MM-DD-NNNNNN_description/
    up.sql
    down.sql
```

Existing migrations:
- `2024-01-15-000001_create_sboms/`
- `2024-02-20-000002_create_assessments/`
- `2024-03-10-000003_add_severity_column/`

The next migration should follow this pattern, e.g.:
`migration/2024-04-01-000004_fix_risk_score_values/up.sql`
