# Codebase Investigation: ACME-520

## Step 2: Locate the Buggy Code

### Primary bug location: `modules/risk/src/score.rs`

The `compute_risk_score()` function has swapped numerator and denominator:

```rust
pub fn compute_risk_score(total_deps: u32, vulnerable_deps: u32) -> f64 {
    // BUG: numerator and denominator are swapped
    total_deps as f64 / vulnerable_deps as f64
}
```

The correct computation should be `vulnerable_deps as f64 / total_deps as f64`, but the code performs `total_deps as f64 / vulnerable_deps as f64`. This produces inflated scores (values > 1.0) whenever total_deps > vulnerable_deps.

## Step 3: Trace the Persistence Chain

### Caller: `modules/risk/src/assessment.rs` -- `create_assessment()`

`create_assessment()` calls `compute_risk_score(total_deps, vulnerable_deps)` and immediately persists the result to the database:

```rust
let score = compute_risk_score(total_deps, vulnerable_deps);

diesel::insert_into(assessments::table)
    .values((
        assessments::sbom_id.eq(sbom_id),
        assessments::risk_score.eq(score),    // <-- persisted here
        assessments::created_at.eq(now),
    ))
    .get_result(conn)
```

**Persistence boundary identified**: The output of `compute_risk_score()` is written to the `assessments` table, `risk_score` column, via `diesel::insert_into(assessments::table)`. This write happens at ingestion time (assessment creation). The risk_score is NOT recomputed on subsequent reads.

### Read path: `modules/risk/src/endpoints.rs` -- `get_assessment()`

The `GET /api/v2/assessments/{id}` endpoint reads the persisted `risk_score` directly from the database:

```rust
let assessment = assessments::table
    .find(path.into_inner())
    .first::<Assessment>(&mut db.get()?)?;
```

It does NOT call `compute_risk_score()` -- it simply returns the value stored in the `assessments.risk_score` column.

### Database schema: `assessments` table

| Column | Type | Description |
|--------|------|-------------|
| id | BIGSERIAL | Primary key |
| sbom_id | BIGINT | Foreign key to sboms table |
| risk_score | DOUBLE PRECISION | Computed risk score (persisted at creation) |
| created_at | TIMESTAMPTZ | Creation timestamp |

## Persistence-Impact Analysis

### Key Finding

The risk_score is **written once at ingestion time** (when `create_assessment()` is called) and is **never recomputed on read**. This means:

1. **All existing assessments** in the database have incorrect `risk_score` values stored in the `assessments.risk_score` column.
2. **Fixing `compute_risk_score()` alone** will only correct future assessments. Existing assessments will retain the wrong (inflated) scores.
3. **A data migration is required** to recompute and update the `risk_score` for all existing rows in the `assessments` table.

### Trace summary

```
compute_risk_score(total_deps, vulnerable_deps)     [modules/risk/src/score.rs]
    -- returns total_deps / vulnerable_deps (WRONG)
    -- should return vulnerable_deps / total_deps
        |
        v
create_assessment(conn, sbom_id, total_deps, vulnerable_deps)  [modules/risk/src/assessment.rs]
    -- calls compute_risk_score()
    -- persists result via diesel::insert_into(assessments::table)
    -- writes to assessments.risk_score column
        |
        v
assessments table, risk_score column (DOUBLE PRECISION)   [database]
    -- stores the wrong value permanently
        |
        v
get_assessment()  [modules/risk/src/endpoints.rs]
    -- reads persisted risk_score directly from database
    -- does NOT recompute -- returns the wrong stored value
```

### Existing migration convention

Migrations follow the Diesel convention: `migration/YYYY-MM-DD-NNNNNN_description/up.sql`

Existing migrations:
- `migration/2024-01-15-000001_create_sboms/up.sql`
- `migration/2024-02-20-000002_create_assessments/up.sql`
- `migration/2024-03-10-000003_add_severity_column/up.sql`

### Existing test gap

The existing test `test_risk_score_all_vulnerable` in `modules/risk/tests/score_test.rs` uses `compute_risk_score(10, 10)` which returns 1.0 regardless of operand order (10/10 = 1.0 either way). No test exercises the case where `total_deps != vulnerable_deps`, so the bug was never caught by the test suite.
