# Codebase Investigation — ACME-520

## Target Repository

- **Repository**: acme-backend
- **Role**: Rust backend service
- **Serena Instance**: serena_backend (not available — Code Intelligence section notes no Serena MCP servers are configured)
- **Path**: /home/dev/repos/acme-backend
- **Fallback**: Read/Grep/Glob tools used for investigation

## Step 2 — Code-Path Tracing

The Steps to Reproduce describe an API-level flow: ingest SBOM, create assessment,
retrieve via GET endpoint. This is a code-path trace (not a runnable reproduction)
since no CLI commands are provided.

### Entry point trace

1. **SBOM ingestion** creates the raw data (100 total deps, 5 vulnerable).
2. **Assessment creation** calls `compute_risk_score()` and persists the result.
3. **GET /api/v2/assessments/{id}** retrieves the persisted value directly.

The bug manifests at step 2: the score is computed incorrectly and then persisted.
The GET endpoint at step 3 merely reads the already-incorrect persisted value.

## Step 3 — Codebase Investigation Findings

### Affected Files and Symbols

| File | Symbol | Role |
|------|--------|------|
| `modules/risk/src/score.rs` | `compute_risk_score()` | Buggy function — swapped division operands |
| `modules/risk/src/assessment.rs` | `create_assessment()` | Caller that persists the incorrect result |
| `modules/risk/src/endpoints.rs` | `get_assessment()` | Query endpoint — reads persisted value, does NOT recompute |

### Buggy Function Analysis

In `modules/risk/src/score.rs`, the function `compute_risk_score()`:

```rust
pub fn compute_risk_score(total_deps: u32, vulnerable_deps: u32) -> f64 {
    total_deps as f64 / vulnerable_deps as f64
}
```

The division is `total_deps / vulnerable_deps` but should be `vulnerable_deps / total_deps`.
With inputs (100, 5), this produces 20.0 instead of 0.05.

### Caller Chain

`compute_risk_score(total_deps, vulnerable_deps)` is called by `create_assessment()`
in `modules/risk/src/assessment.rs`:

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

### Query Endpoint

The GET endpoint in `modules/risk/src/endpoints.rs` reads `risk_score` directly
from the database:

```rust
let assessment = assessments::table
    .find(path.into_inner())
    .first::<Assessment>(&mut db.get()?)?;
Ok(HttpResponse::Ok().json(assessment))
```

It does NOT recompute the score. Fixing `compute_risk_score()` alone will only
correct future assessments; existing assessments retain the wrong score.

### Persistence-Impact Analysis

**Persistence boundary found.**

1. **Trace**: `compute_risk_score()` return value flows to `create_assessment()`,
   which calls `diesel::insert_into(assessments::table)` with
   `assessments::risk_score.eq(score)`.

2. **Persistence boundary**:
   - **Table**: `assessments`
   - **Column**: `risk_score` (type: DOUBLE PRECISION)
   - **Write operation**: `diesel::insert_into(assessments::table)` in
     `modules/risk/src/assessment.rs::create_assessment()`
   - **Write timing**: Ingestion time (assessment creation). The risk_score is
     computed once when the assessment is first created and is NOT recomputed on
     read.

3. **Conclusion**: Since `risk_score` is written at ingestion time and is NOT
   recomputed on read, all existing assessments contain incorrect (inflated)
   risk_score values. A **data migration is required** to recompute and correct
   existing risk_score values in the `assessments` table.

### Database Schema

| Column | Type | Description |
|--------|------|-------------|
| id | BIGSERIAL | Primary key |
| sbom_id | BIGINT | Foreign key to sboms table |
| risk_score | DOUBLE PRECISION | Computed risk score (persisted at creation) |
| created_at | TIMESTAMPTZ | Creation timestamp |

### Existing Migration Convention

Migration directory: `migration/`

Existing migrations follow the Diesel naming convention:
`YYYY-MM-DD-NNNNNN_description/up.sql`

```
migration/
  2024-01-15-000001_create_sboms/up.sql
  2024-02-20-000002_create_assessments/up.sql
  2024-03-10-000003_add_severity_column/up.sql
```

### Existing Tests

File: `modules/risk/tests/score_test.rs`

```rust
#[test]
fn test_risk_score_all_vulnerable() {
    let score = compute_risk_score(10, 10);
    assert_eq!(score, 1.0);
}
```

This test passes even with the bug because `10 / 10 = 1.0` regardless of operand
order. No test exercises the case where `total != vulnerable` — this is the gap
that allowed the bug to ship.

### CONVENTIONS.md

No CONVENTIONS.md found at the repository root.

### Reuse Candidates

- `modules/risk/tests/score_test.rs` — existing test file and assertion pattern
  for `compute_risk_score()`. The reproducer test should be added here, following
  the existing test structure.
