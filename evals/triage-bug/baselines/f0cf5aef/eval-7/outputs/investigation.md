# Steps 2-3 -- Codebase Investigation: ACME-520

## Target Repository

- **Repository**: acme-backend
- **Role**: Rust backend service
- **Serena Instance**: serena_backend
- **Path**: /home/dev/repos/acme-backend

The **Component** field (`risk-engine`) and code paths referenced in Steps to Reproduce (risk assessment computation, `GET /api/v2/assessments/{id}`) point to the `acme-backend` repository.

## Step 2 -- Reproduce/Trace

### Code-path tracing

The Steps to Reproduce describe an API-driven workflow that cannot be directly reproduced without a running service. Tracing through the code paths instead:

1. **Entry point**: Creating a risk assessment triggers `create_assessment()` in `modules/risk/src/assessment.rs`, which calls `compute_risk_score(total_deps, vulnerable_deps)`.
2. **Buggy function**: `compute_risk_score()` in `modules/risk/src/score.rs` computes `total_deps as f64 / vulnerable_deps as f64` -- the operands are reversed.
3. **Expected behavior**: For an SBOM with 100 total and 5 vulnerable dependencies, the score should be `5 / 100 = 0.05`.
4. **Actual behavior**: The function computes `100 / 5 = 20.0` -- numerator and denominator are swapped, producing a grossly inflated score.
5. **Read path**: `GET /api/v2/assessments/{id}` in `modules/risk/src/endpoints.rs` reads the persisted `risk_score` directly from the database. It does NOT recompute the score.

The trace confirms the bug: the division operands in `compute_risk_score()` are reversed, and the incorrect value is stored permanently in the database.

## Step 3 -- Codebase Investigation

### Affected files and symbols

| File | Symbol | Role |
|------|--------|------|
| `modules/risk/src/score.rs` | `compute_risk_score()` | Buggy function -- division operands reversed |
| `modules/risk/src/assessment.rs` | `create_assessment()` | Caller that persists the incorrect score to the database |
| `modules/risk/src/endpoints.rs` | `get_assessment()` | Read endpoint -- returns persisted score without recomputation |

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

This test passes even with the bug because `10 / 10 = 1.0` regardless of operand order. No test exercises the case where `total_deps != vulnerable_deps`, which is why the bug went undetected.

### Existing migration pattern

Migration files are located in `migration/` and follow the Diesel convention:

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

Naming convention: `YYYY-MM-DD-NNNNNN_description/up.sql` (and `down.sql`).

### CONVENTIONS.md

No `CONVENTIONS.md` file found at the repository root.

## Persistence-Impact Analysis

### Trace: output to persistence boundary

1. `compute_risk_score(total_deps, vulnerable_deps)` returns `f64` (the incorrect score).
2. `create_assessment()` in `modules/risk/src/assessment.rs` calls `compute_risk_score()` and assigns the return value to `score`.
3. `create_assessment()` executes `diesel::insert_into(assessments::table).values((..., assessments::risk_score.eq(score), ...))` -- **persistence boundary found**.

### Persistence boundary details

- **Table**: `assessments`
- **Column**: `risk_score` (DOUBLE PRECISION)
- **Write operation location**: `modules/risk/src/assessment.rs`, function `create_assessment()`
- **Write timing**: Ingestion time -- the score is computed and persisted once when the assessment is first created. It is NOT recomputed on read.

### Impact

Fixing `compute_risk_score()` alone will only correct **future** assessments. All **existing** assessments in the `assessments` table have incorrect (inflated) `risk_score` values that will never self-correct because the read endpoint (`get_assessment()`) returns the persisted value directly.

**A data migration is required** to recompute and correct the `risk_score` column for all existing records in the `assessments` table.

### Reuse candidates

- `modules/risk/src/score.rs::compute_risk_score` -- the function to fix (swap operands)
- `modules/risk/tests/score_test.rs` -- existing test file where the reproducer test should be added
- `migration/` directory -- location for the new data migration file following Diesel conventions
