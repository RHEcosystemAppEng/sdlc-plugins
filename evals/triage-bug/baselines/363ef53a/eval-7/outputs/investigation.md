# Steps 2-3: Codebase Investigation and Persistence-Impact Analysis

## Repository
acme-backend (Rust backend service)

## Bug Location

### Primary Defect: `modules/risk/src/score.rs` -- `compute_risk_score()`

```rust
pub fn compute_risk_score(total_deps: u32, vulnerable_deps: u32) -> f64 {
    // BUG: numerator and denominator are swapped
    total_deps as f64 / vulnerable_deps as f64
}
```

The function divides `total_deps / vulnerable_deps` instead of `vulnerable_deps / total_deps`. This produces inflated scores (e.g., 20.0 instead of 0.05 for 5 vulnerable out of 100 total).

## Call Chain Analysis

1. **`compute_risk_score()`** in `modules/risk/src/score.rs` -- computes the incorrect score.
2. **`create_assessment()`** in `modules/risk/src/assessment.rs` -- calls `compute_risk_score()` and writes the result to the database via `diesel::insert_into(assessments::table)`.
3. **`get_assessment()`** in `modules/risk/src/endpoints.rs` -- reads the persisted `risk_score` directly from the database; does NOT recompute the score.

## Persistence-Impact Analysis

### Persistence Boundary Identified

The persistence boundary is in `create_assessment()` (`modules/risk/src/assessment.rs`). The buggy risk score is written to the `assessments` table (`risk_score` column of type `DOUBLE PRECISION`) at ingestion time -- when the assessment is first created. The value is never recomputed on subsequent reads.

### Impact on Existing Data

- **All existing assessment records contain incorrect `risk_score` values.** The scores are inverted (total/vulnerable instead of vulnerable/total).
- The `GET /api/v2/assessments/{id}` endpoint simply reads the persisted value from the database -- it does not recompute. Therefore, fixing `compute_risk_score()` alone will only correct **future** assessments.
- **A data migration is required** to correct the `risk_score` column for all existing rows in the `assessments` table.

### Migration Strategy

The existing migration directory follows the Diesel convention: `YYYY-MM-DD-NNNNNN_description/up.sql`. Existing migrations:

- `migration/2024-01-15-000001_create_sboms/`
- `migration/2024-02-20-000002_create_assessments/`
- `migration/2024-03-10-000003_add_severity_column/`

A new migration is needed (e.g., `migration/YYYY-MM-DD-NNNNNN_fix_risk_scores/up.sql`) to correct existing values. The migration logic: for each row in `assessments`, the corrected score is `1.0 / risk_score` (since `total/vulnerable` is the reciprocal of `vulnerable/total`), but only where `risk_score != 0`.

## Existing Test Coverage Gap

The only existing test in `modules/risk/tests/score_test.rs` uses `total_deps = 10, vulnerable_deps = 10`, which produces `1.0` regardless of operand order. No test exercises the case where `total != vulnerable`, so the bug was never caught by tests.
