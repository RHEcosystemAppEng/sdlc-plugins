# Steps 2-3 -- Codebase Investigation: ACME-520

## Step 2 -- Reproduce/Trace

### Code-path tracing

The Steps to Reproduce describe an API-driven workflow (SBOM ingestion, assessment creation, assessment retrieval) that cannot be directly reproduced in a read-only triage context. Code-path tracing was performed instead.

**Entry point**: The reproduction begins with creating a risk assessment for an ingested SBOM. The assessment creation calls `compute_risk_score()` and persists the result.

**Trace through the code path**:

1. **`compute_risk_score(total_deps, vulnerable_deps)` in `modules/risk/src/score.rs`**:
   - Current (buggy) implementation: `total_deps as f64 / vulnerable_deps as f64`
   - With inputs total_deps=100, vulnerable_deps=5: computes `100.0 / 5.0 = 20.0`
   - Expected computation: `vulnerable_deps as f64 / total_deps as f64` = `5.0 / 100.0 = 0.05`
   - **Confirmed**: The numerator and denominator are swapped, producing inflated scores.

2. **`create_assessment()` in `modules/risk/src/assessment.rs`**:
   - Calls `compute_risk_score(total_deps, vulnerable_deps)` and receives the buggy result (20.0).
   - Persists the result via `diesel::insert_into(assessments::table)` with `assessments::risk_score.eq(score)`.
   - The incorrect score is written to the database at this point.

3. **`GET /api/v2/assessments/{id}` in `modules/risk/src/endpoints.rs`**:
   - Reads the persisted `risk_score` directly from the `assessments` table.
   - Does NOT recompute the score -- returns whatever was stored at creation time.
   - This means the API returns the buggy value (20.0) for all existing assessments.

**Trace finding**: The bug is confirmed. The division operands in `compute_risk_score()` are reversed, and the incorrect value is persisted to the database and served unchanged to API consumers.

## Step 3 -- Codebase Investigation

### Target repository

- **Repository**: acme-backend
- **Role**: Rust backend service
- **Serena Instance**: serena_backend
- **Path**: /home/dev/repos/acme-backend

The bug's Component field (`risk-engine`) and the code paths referenced in Steps to Reproduce point to the `acme-backend` repository.

### Affected files and symbols

| File | Symbol | Role |
|------|--------|------|
| `modules/risk/src/score.rs` | `compute_risk_score()` | Buggy function -- division operands swapped |
| `modules/risk/src/assessment.rs` | `create_assessment()` | Caller that persists the buggy result to DB |
| `modules/risk/src/endpoints.rs` | `get_assessment()` | API endpoint that reads persisted (buggy) risk_score |

### Database schema

**Table**: `assessments`

| Column | Type | Description |
|--------|------|-------------|
| id | BIGSERIAL | Primary key |
| sbom_id | BIGINT | Foreign key to sboms table |
| risk_score | DOUBLE PRECISION | Computed risk score (persisted at creation) |
| created_at | TIMESTAMPTZ | Creation timestamp |

### Existing test files and patterns

**File**: `modules/risk/tests/score_test.rs`

Existing test:
```rust
#[test]
fn test_risk_score_all_vulnerable() {
    let score = compute_risk_score(10, 10);
    assert_eq!(score, 1.0);
}
```

This test passes even with the bug because `10 / 10 = 1.0` regardless of operand order. No test exercises the case where `total_deps != vulnerable_deps`, which is the condition that exposes the bug.

### Existing migration structure

```
migration/
  2024-01-15-000001_create_sboms/
    up.sql
    down.sql
  2024-02-20-000002_create_assessments/
    up.sql
    down.sql
  2024-03-10-000003_add_severity_column/
    up.sql
    down.sql
```

Migration files follow the Diesel naming convention: `YYYY-MM-DD-NNNNNN_description/up.sql`.

### CONVENTIONS.md lookup

No `CONVENTIONS.md` file found at the repository root. No additional conventions to apply.

### Persistence-impact analysis

**Trace**: `compute_risk_score()` -> `create_assessment()` -> `diesel::insert_into(assessments::table).values(assessments::risk_score.eq(score))`

**Persistence boundary found**:
- **Table**: `assessments`
- **Column**: `risk_score` (DOUBLE PRECISION)
- **Write operation location**: `modules/risk/src/assessment.rs`, `create_assessment()` function
- **Write timing**: Ingestion time -- the risk score is computed and written once when the assessment is first created. It is NOT recomputed on read.

**Impact**: Fixing `compute_risk_score()` alone will only correct future assessments. All existing assessments in the `assessments` table retain the incorrect (inflated) `risk_score` values. A **data migration is required** to recompute and update the `risk_score` column for all existing records.

The correct recomputation requires access to the original `total_deps` and `vulnerable_deps` values. Since the `assessments` table stores `sbom_id`, the migration must join against the `sboms` table (or its related vulnerability data) to retrieve the original dependency counts and recompute `vulnerable_deps / total_deps` for each existing assessment.
