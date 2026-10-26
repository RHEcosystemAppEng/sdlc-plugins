<!-- SYNTHETIC TEST DATA — mock repository context with a persistence chain for triage-bug persistence-impact eval testing -->

# Mock Repository Context: acme-backend (persistence scenario)

This file simulates the relevant code paths that the triage-bug skill would
discover during Step 3 (Codebase Investigation) for bug ACME-520.

## File: modules/risk/src/score.rs

### compute_risk_score (the buggy function)

```rust
/// Computes a risk score for an SBOM based on its vulnerability profile.
pub fn compute_risk_score(total_deps: u32, vulnerable_deps: u32) -> f64 {
    // BUG: numerator and denominator are swapped
    total_deps as f64 / vulnerable_deps as f64
}
```

**Root cause**: The division operands are reversed. Should be
`vulnerable_deps / total_deps`, not `total_deps / vulnerable_deps`.

## File: modules/risk/src/assessment.rs

### create_assessment (caller that persists the result)

```rust
use crate::score::compute_risk_score;
use diesel::prelude::*;

/// Creates a risk assessment for an SBOM and persists it to the database.
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

**Persistence boundary**: The risk score computed by `compute_risk_score()` is
written to the `assessments` table, `risk_score` column, at ingestion time
(when the assessment is first created). It is NOT recomputed on read.

## File: modules/risk/src/endpoints.rs

### GET /api/v2/assessments/{id} (query endpoint)

```rust
/// Retrieves a risk assessment by ID.
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

**Note**: This endpoint reads the persisted `risk_score` directly from the
database — it does NOT recompute the score. Fixing `compute_risk_score()` alone
will only correct future assessments; existing assessments retain the wrong score.

## Database schema

### Table: assessments

| Column | Type | Description |
|--------|------|-------------|
| id | BIGSERIAL | Primary key |
| sbom_id | BIGINT | Foreign key to sboms table |
| risk_score | DOUBLE PRECISION | Computed risk score (persisted at creation) |
| created_at | TIMESTAMPTZ | Creation timestamp |

## Existing migrations

### Directory: migration/

```
migration/
├── 2024-01-15-000001_create_sboms/
│   ├── up.sql
│   └── down.sql
├── 2024-02-20-000002_create_assessments/
│   ├── up.sql
│   └── down.sql
└── 2024-03-10-000003_add_severity_column/
    ├── up.sql
    └── down.sql
```

Migration files follow the Diesel convention: `YYYY-MM-DD-NNNNNN_description/up.sql`.

## Test files

### Existing test: modules/risk/tests/score_test.rs

```rust
#[test]
fn test_risk_score_all_vulnerable() {
    let score = compute_risk_score(10, 10);
    assert_eq!(score, 1.0);
}
```

**Note**: This test passes even with the bug because `10 / 10 = 1.0` regardless
of operand order. No test exercises the case where `total != vulnerable`.

## CONVENTIONS.md

The repository does not have a CONVENTIONS.md at its root.
