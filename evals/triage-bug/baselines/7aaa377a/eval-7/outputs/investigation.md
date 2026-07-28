# Codebase Investigation — ACME-520 (Steps 2–3)

## Step 2 – Reproduce / Trace

**Approach:** Code-path tracing (the bug is a logic error in a Rust function; it
cannot be reproduced by running a command in this environment).

**Trace entry point:** `GET /api/v2/assessments/{id}` — the endpoint the reporter
uses to observe the wrong `risk_score` value.

**Observed trace:**

1. Reporter ingests an SBOM (100 total deps, 5 vulnerable).
2. A risk assessment is created by calling `create_assessment()` in
   `modules/risk/src/assessment.rs`.
3. `create_assessment()` calls `compute_risk_score(total_deps, vulnerable_deps)`.
4. `compute_risk_score()` evaluates `total_deps as f64 / vulnerable_deps as f64`,
   i.e. `100.0 / 5.0 = 20.0`, and returns that value.
5. `create_assessment()` stores the returned score in the database via Diesel's
   `insert_into(assessments::table).values(...assessments::risk_score.eq(score)...)`.
6. `GET /api/v2/assessments/{id}` reads the persisted row and returns `risk_score: 20.0`.

The divergence from expected behavior (`0.05`) occurs in step 4: the operands in
the division are inverted.

**Existing test gap:** `modules/risk/tests/score_test.rs` contains only
`test_risk_score_all_vulnerable`, which calls `compute_risk_score(10, 10)`.
When `total == vulnerable`, the result is `1.0` regardless of operand order, so
this test passes even with the bug. No test exercises the case where `total != vulnerable`.

---

## Step 3 – Codebase Investigation

### Target Repository

Component `risk-engine` maps to the **acme-backend** repository
(Serena Instance: serena_backend, Path: `/home/dev/repos/acme-backend`).

Note: CLAUDE.md states "No Serena MCP servers are configured." Falling back to
Read/Grep/Glob-equivalent analysis of the repository context provided.

### Affected Files and Symbols

#### modules/risk/src/score.rs — `compute_risk_score()`

```rust
pub fn compute_risk_score(total_deps: u32, vulnerable_deps: u32) -> f64 {
    // BUG: numerator and denominator are swapped
    total_deps as f64 / vulnerable_deps as f64
}
```

**Defect:** The return expression divides `total_deps` by `vulnerable_deps`.
The correct formula is `vulnerable_deps / total_deps`.

#### modules/risk/src/assessment.rs — `create_assessment()`

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

This is the direct caller of the buggy function. It persists the score to the
database at ingestion time.

#### modules/risk/src/endpoints.rs — `get_assessment()`

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

This endpoint reads the persisted `risk_score` directly from the database without
recomputing it. Fixing `compute_risk_score()` alone does NOT correct records already
in the database.

#### modules/risk/tests/score_test.rs — existing tests

```rust
#[test]
fn test_risk_score_all_vulnerable() {
    let score = compute_risk_score(10, 10);
    assert_eq!(score, 1.0);
}
```

Only covers the degenerate case where `total == vulnerable`. The reproducer test
must use `total != vulnerable` to expose the bug (e.g., `total=100, vulnerable=5`).

### Database Schema

**Table:** `assessments`

| Column | Type | Description |
|--------|------|-------------|
| id | BIGSERIAL | Primary key |
| sbom_id | BIGINT | Foreign key to sboms table |
| risk_score | DOUBLE PRECISION | Computed risk score (persisted at creation) |
| created_at | TIMESTAMPTZ | Creation timestamp |

### Migration Convention

**Directory:** `migration/` (Diesel convention: `YYYY-MM-DD-NNNNNN_description/`)

Existing migrations:
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

Next migration number: **000004**. Today's date: **2026-07-28**.
New migration directory: `migration/2026-07-28-000004_fix_risk_score_values/`

### CONVENTIONS.md

No `CONVENTIONS.md` found at the repository root.

---

## Persistence-Impact Analysis

### Trace from buggy function to persistence boundary

```
compute_risk_score(total_deps, vulnerable_deps)   [modules/risk/src/score.rs]
  └─► return value (f64: the wrong score)
        └─► create_assessment() assigns it to `score`   [modules/risk/src/assessment.rs:38]
              └─► diesel::insert_into(assessments::table)
                    .values(assessments::risk_score.eq(score))   [assessment.rs:41]
```

**Persistence boundary found.**

| Property | Value |
|----------|-------|
| Table | `assessments` |
| Column | `risk_score` |
| Write operation | `diesel::insert_into(assessments::table)` in `create_assessment()` |
| Write location | `modules/risk/src/assessment.rs` |
| Write timing | **Ingestion time** — written once when the assessment is first created |
| Self-correcting? | **No** — `get_assessment()` reads the stored value; it never recomputes |

### Implication

Every assessment created since the bug was introduced has a `risk_score` value that
is `(total / vulnerable)` instead of `(vulnerable / total)`. These records will not
be corrected by a code fix alone. A **data migration** is required to recompute and
overwrite the stale `risk_score` values for all existing rows in the `assessments`
table.

The correct value for each row is:

```sql
-- For each assessment row, look up the SBOM's dependency counts and recompute:
-- new_score = vulnerable_deps / total_deps
```

Because `total_deps` and `vulnerable_deps` are not stored in the `assessments`
table itself (only the derived `risk_score` is stored), the migration must either:
- Join against the `sboms` table if dependency counts are stored there, or
- Recompute from the inverse: `new_risk_score = 1.0 / old_risk_score` — which is
  mathematically equivalent since `(total/vulnerable)^-1 = vulnerable/total`.

The inverse approach (`1.0 / risk_score`) is safe as a migration, avoids joining
additional tables, and produces the exact correct value given the specific bug
(a pure operand swap). The migration should guard against division-by-zero for
any rows where `risk_score = 0`.
