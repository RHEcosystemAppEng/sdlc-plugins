# Codebase Investigation -- Steps 2-3

## Step 2 -- Reproduce/Trace

### Code-path tracing

The Steps to Reproduce describe an API-driven workflow that cannot be directly
executed in this context. The code path was traced instead.

**Entry point**: An SBOM is ingested, then a risk assessment is created, and finally
the assessment is retrieved via `GET /api/v2/assessments/{id}`.

**Trace**:

1. `compute_risk_score(total_deps, vulnerable_deps)` in `modules/risk/src/score.rs`
   performs the computation `total_deps as f64 / vulnerable_deps as f64`.
2. `create_assessment()` in `modules/risk/src/assessment.rs` calls
   `compute_risk_score(total_deps, vulnerable_deps)` and receives the result in
   the local variable `score`.
3. `create_assessment()` then executes `diesel::insert_into(assessments::table)`
   with `.values(...)` including `assessments::risk_score.eq(score)`, persisting
   the computed (incorrect) score to the `assessments` table.
4. `get_assessment()` in `modules/risk/src/endpoints.rs` reads from
   `assessments::table` using `.find(id).first::<Assessment>(...)` and returns the
   persisted `risk_score` value directly -- it does NOT recompute the score.

**Divergence point**: The division in `compute_risk_score()` has the operands
swapped. For the example in the bug report (100 total deps, 5 vulnerable):
- Expected: `vulnerable_deps / total_deps = 5 / 100 = 0.05`
- Actual: `total_deps / vulnerable_deps = 100 / 5 = 20.0`

**Reproduction outcome**: Confirmed via code-path tracing. The operand swap is
clearly visible in the source code.

## Step 3 -- Codebase Investigation

### Target repository

- **Repository**: acme-backend
- **Role**: Rust backend service
- **Path**: /home/dev/repos/acme-backend
- **Serena Instance**: serena_backend (but Code Intelligence section notes no
  Serena MCP servers are configured)

### Affected files and symbols

| File | Symbol | Role |
|------|--------|------|
| `modules/risk/src/score.rs` | `compute_risk_score()` | Buggy function -- operands swapped |
| `modules/risk/src/assessment.rs` | `create_assessment()` | Caller that persists the result to DB |
| `modules/risk/src/endpoints.rs` | `get_assessment()` | Read endpoint -- returns persisted score |

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

The existing test `test_risk_score_all_vulnerable` passes even with the bug because
it uses `total_deps = 10, vulnerable_deps = 10`, where `10 / 10 = 1.0` regardless
of operand order. No test exercises the case where `total_deps != vulnerable_deps`,
which is why the bug was not caught.

### CONVENTIONS.md lookup

No CONVENTIONS.md file found at the repository root.

### Existing migration pattern

Migration files follow the Diesel convention: `YYYY-MM-DD-NNNNNN_description/up.sql`

Existing migrations:
```
migration/
  2024-01-15-000001_create_sboms/up.sql
  2024-02-20-000002_create_assessments/up.sql
  2024-03-10-000003_add_severity_column/up.sql
```

### Persistence-impact analysis

#### Trace output to persistence boundary

**Trace**: `compute_risk_score()` -> `create_assessment()` -> `diesel::insert_into(assessments::table).values(assessments::risk_score.eq(score))`

**Persistence boundary found**:
- **Table**: `assessments`
- **Column**: `risk_score`
- **Write operation location**: `modules/risk/src/assessment.rs`, function `create_assessment()`
- **Write timing**: The `risk_score` value is written at **ingestion time** (when the
  assessment is first created via `create_assessment()`). It is NOT recomputed on read.
  The `get_assessment()` endpoint in `modules/risk/src/endpoints.rs` reads the persisted
  value directly from the database.

#### Impact

Fixing `compute_risk_score()` alone will only correct **future** assessments. All
**existing** assessments in the `assessments` table have incorrect `risk_score` values
(inflated by the swapped operands). A **data migration** is needed to recompute and
update the `risk_score` column for all existing records.

The migration must:
1. Join `assessments` with the source data (the `sboms` table or the original
   `total_deps` / `vulnerable_deps` values) to recompute the correct score.
2. Update the `risk_score` column with the corrected value for each existing row.
