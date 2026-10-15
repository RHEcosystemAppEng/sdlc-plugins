# Steps 2-3 -- Codebase Investigation: ACME-520

## Step 2 -- Reproduce/Trace

### Reproduction method: Code-path tracing

The Steps to Reproduce describe an end-to-end flow (SBOM ingestion, assessment
creation, API retrieval) that cannot be directly executed in this context. Code-path
tracing is used instead.

### Trace findings

**Entry point**: The bug originates in `compute_risk_score()` in
`modules/risk/src/score.rs`.

**Buggy code**:

```rust
pub fn compute_risk_score(total_deps: u32, vulnerable_deps: u32) -> f64 {
    // BUG: numerator and denominator are swapped
    total_deps as f64 / vulnerable_deps as f64
}
```

**Divergence from expected behavior**: The function divides `total_deps / vulnerable_deps`
instead of `vulnerable_deps / total_deps`. For the scenario in the bug report
(total=100, vulnerable=5):

- Expected: `5 / 100 = 0.05`
- Actual: `100 / 5 = 20.0`

**Call chain**: `compute_risk_score()` is called by `create_assessment()` in
`modules/risk/src/assessment.rs`, which passes the return value directly into a
Diesel `insert_into` call, persisting the incorrect score to the `assessments` table.

**Query path**: `GET /api/v2/assessments/{id}` in `modules/risk/src/endpoints.rs`
reads the persisted `risk_score` directly from the database. It does NOT recompute
the score. This means existing assessments will continue to return the wrong score
even after the code is fixed.

### Reproduction outcome

**Confirmed via code-path analysis.** The operands are clearly reversed in the
division. The existing test (`test_risk_score_all_vulnerable`) does not catch the
bug because it uses `total_deps=10, vulnerable_deps=10`, where `10/10 = 1.0`
regardless of operand order.

---

## Step 3 -- Codebase Investigation

### Target repository

- **Repository**: acme-backend
- **Role**: Rust backend service
- **Serena Instance**: serena_backend (but Code Intelligence not available per CLAUDE.md)
- **Path**: /home/dev/repos/acme-backend

### Affected files and symbols

| File | Symbol | Role |
|------|--------|------|
| `modules/risk/src/score.rs` | `compute_risk_score()` | Buggy function -- operands reversed |
| `modules/risk/src/assessment.rs` | `create_assessment()` | Caller that persists the result to DB |
| `modules/risk/src/endpoints.rs` | `get_assessment()` | Read endpoint (reads persisted value, no recompute) |
| `modules/risk/tests/score_test.rs` | `test_risk_score_all_vulnerable()` | Existing test (does not catch the bug) |

### Database schema

**Table**: `assessments`

| Column | Type | Description |
|--------|------|-------------|
| id | BIGSERIAL | Primary key |
| sbom_id | BIGINT | Foreign key to sboms table |
| risk_score | DOUBLE PRECISION | Computed risk score (persisted at creation) |
| created_at | TIMESTAMPTZ | Creation timestamp |

### Existing migration structure

```
migration/
  2024-01-15-000001_create_sboms/
    up.sql, down.sql
  2024-02-20-000002_create_assessments/
    up.sql, down.sql
  2024-03-10-000003_add_severity_column/
    up.sql, down.sql
```

Migration files follow the Diesel convention: `YYYY-MM-DD-NNNNNN_description/up.sql`.

### Existing test patterns

The existing test in `modules/risk/tests/score_test.rs` uses direct assertion:

```rust
#[test]
fn test_risk_score_all_vulnerable() {
    let score = compute_risk_score(10, 10);
    assert_eq!(score, 1.0);
}
```

This test does not exercise the case where `total_deps != vulnerable_deps`, which
is why the bug was not caught.

### CONVENTIONS.md

No `CONVENTIONS.md` found at the repository root. No additional conventions to
apply.

---

## Persistence-Impact Analysis

### Trace: output to persistence boundary

```
compute_risk_score(total_deps, vulnerable_deps)    -- modules/risk/src/score.rs
  returns f64 (the incorrect score)
    |
    v
create_assessment(conn, sbom_id, total_deps, vulnerable_deps)   -- modules/risk/src/assessment.rs
  let score = compute_risk_score(total_deps, vulnerable_deps);
    |
    v
  diesel::insert_into(assessments::table)
    .values((
        assessments::sbom_id.eq(sbom_id),
        assessments::risk_score.eq(score),    <-- PERSISTENCE BOUNDARY
        assessments::created_at.eq(now),
    ))
    .get_result(conn)
```

### Persistence boundary found

| Property | Value |
|----------|-------|
| Table | `assessments` |
| Column | `risk_score` |
| Write operation location | `modules/risk/src/assessment.rs`, function `create_assessment()` |
| Write timing | Ingestion time (when assessment is first created) |
| Recomputed on read? | No -- `GET /api/v2/assessments/{id}` reads persisted value directly |

### Impact assessment

**Data migration is required.** The `risk_score` column stores the value computed
at assessment creation time. It is never recomputed on subsequent reads. All existing
assessments created while the bug was present contain inflated risk scores (the
reciprocal of the correct value).

The incorrect values follow a deterministic pattern: for each affected row, the
persisted `risk_score` equals `total_deps / vulnerable_deps` instead of
`vulnerable_deps / total_deps`. This means the correct value is `1.0 / risk_score`
(the reciprocal), provided `risk_score > 0`. The source data (`sbom_id` links to
the sboms table which contains the original dependency counts) can also be used for
a more robust recomputation.

Fixing `compute_risk_score()` alone will only correct future assessments. A data
migration must update all existing rows in the `assessments` table to correct the
`risk_score` values.
