# Codebase Investigation: ACME-520

## Call Chain Analysis

### 1. Buggy Function: `compute_risk_score()` in `modules/risk/src/score.rs`

```rust
pub fn compute_risk_score(total_deps: u32, vulnerable_deps: u32) -> f64 {
    // BUG: numerator and denominator are swapped
    total_deps as f64 / vulnerable_deps as f64
}
```

**Finding**: The function divides `total_deps / vulnerable_deps` instead of
`vulnerable_deps / total_deps`. For an SBOM with 100 total deps and 5 vulnerable,
this produces `100 / 5 = 20.0` instead of the correct `5 / 100 = 0.05`.

### 2. Caller: `create_assessment()` in `modules/risk/src/assessment.rs`

```rust
pub fn create_assessment(
    conn: &mut PgConnection,
    sbom_id: i64,
    total_deps: u32,
    vulnerable_deps: u32,
) -> Result<Assessment, Error> {
    let score = compute_risk_score(total_deps, vulnerable_deps);

    diesel::insert_into(assessments::table)
        .values((
            assessments::sbom_id.eq(sbom_id),
            assessments::risk_score.eq(score),    // <-- persisted here
            assessments::created_at.eq(now),
        ))
        .get_result(conn)
}
```

**Finding**: `create_assessment()` calls `compute_risk_score()` and immediately
persists the result to the `assessments` table in the `risk_score` column via
`diesel::insert_into`. The incorrect score is written to the database at ingestion
time (assessment creation).

### 3. Read Path: `get_assessment()` in `modules/risk/src/endpoints.rs`

```rust
pub async fn get_assessment(
    path: web::Path<i64>,
    db: web::Data<DbPool>,
) -> Result<HttpResponse, Error> {
    let assessment = assessments::table
        .find(path.into_inner())
        .first::<Assessment>(&mut db.get()?)?;

    Ok(HttpResponse::Ok().json(assessment))
}
```

**Finding**: The `GET /api/v2/assessments/{id}` endpoint reads the persisted
`risk_score` directly from the database. It does NOT recompute the score. This
means fixing `compute_risk_score()` alone will only correct **future** assessments;
all **existing** assessments retain incorrect scores.

## Persistence-Impact Analysis

### Persistence Boundary Identified

- **Table**: `assessments`
- **Column**: `risk_score` (type: DOUBLE PRECISION)
- **Written at**: Ingestion time (assessment creation via `create_assessment()`)
- **Recomputed on read**: NO -- `get_assessment()` reads persisted value directly
- **Impact**: All existing assessments in the database have incorrect (inflated)
  risk scores that will persist even after the code fix is deployed

### Conclusion: Data Migration Required

Fixing `compute_risk_score()` alone is **insufficient**. A data migration is
required to correct the `risk_score` values for all existing assessments in the
database. The migration must recompute `risk_score` using the correct formula
(`vulnerable_deps / total_deps`) for every row in the `assessments` table.

## Existing Test Analysis

### Test: `test_risk_score_all_vulnerable` in `modules/risk/tests/score_test.rs`

```rust
#[test]
fn test_risk_score_all_vulnerable() {
    let score = compute_risk_score(10, 10);
    assert_eq!(score, 1.0);
}
```

**Finding**: This test passes even with the bug because `10 / 10 = 1.0` regardless
of operand order. No test exercises the case where `total_deps != vulnerable_deps`,
which is the case that reveals the swapped operands.

## Existing Migration Pattern

Migration files follow the Diesel convention: `YYYY-MM-DD-NNNNNN_description/up.sql`.

Existing migrations:
```
migration/
  2024-01-15-000001_create_sboms/up.sql
  2024-02-20-000002_create_assessments/up.sql
  2024-03-10-000003_add_severity_column/up.sql
```

A new migration must be added following this pattern to correct existing data.
