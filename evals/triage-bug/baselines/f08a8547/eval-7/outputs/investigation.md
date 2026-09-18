# Steps 2-3 -- Codebase Investigation

## Target Repository

| Repository    | Role                 | Serena Instance  | Path                           |
|---------------|----------------------|------------------|--------------------------------|
| acme-backend  | Rust backend service | serena_backend   | /home/dev/repos/acme-backend   |

## Step 2 -- Code-Path Tracing

The Steps to Reproduce describe an API-level workflow (ingest SBOM, create assessment,
retrieve via GET endpoint). Direct reproduction is not possible in this environment,
so code-path tracing was performed instead.

### Trace from entry point

1. **Entry point**: The bug manifests when a risk assessment is created for an ingested
   SBOM. The `create_assessment()` function in `modules/risk/src/assessment.rs` is the
   entry point that orchestrates score computation and persistence.

2. **Buggy computation**: `create_assessment()` calls `compute_risk_score(total_deps, vulnerable_deps)`
   in `modules/risk/src/score.rs`. This function performs:
   ```rust
   total_deps as f64 / vulnerable_deps as f64
   ```
   The operands are reversed. For inputs (total=100, vulnerable=5), it computes
   `100 / 5 = 20.0` instead of the correct `5 / 100 = 0.05`.

3. **Divergence point**: The divergence from expected behavior occurs at the division
   in `compute_risk_score()`. The function signature correctly names the parameters
   (`total_deps`, `vulnerable_deps`) but the division body swaps them.

4. **Query endpoint**: `GET /api/v2/assessments/{id}` in `modules/risk/src/endpoints.rs`
   reads the persisted `risk_score` directly from the `assessments` table. It does NOT
   recompute the score. This confirms the Actual Result: clients see the inflated value
   stored at creation time.

### Trace conclusion

Bug confirmed by code-path analysis. The numerator and denominator in
`compute_risk_score()` are swapped, producing scores that are the reciprocal of the
correct value (or worse, inflated by orders of magnitude when vulnerable << total).

## Step 3 -- Codebase Investigation

### Affected files and symbols

| File                                  | Symbol                  | Role                                      |
|---------------------------------------|-------------------------|-------------------------------------------|
| `modules/risk/src/score.rs`           | `compute_risk_score()`  | Buggy function -- swapped division operands |
| `modules/risk/src/assessment.rs`      | `create_assessment()`   | Caller that persists result to database    |
| `modules/risk/src/endpoints.rs`       | `get_assessment()`      | Query endpoint -- reads persisted score    |

### Existing test analysis

| File                                       | Test                               | Status                          |
|--------------------------------------------|------------------------------------|---------------------------------|
| `modules/risk/tests/score_test.rs`         | `test_risk_score_all_vulnerable`   | Passes with bug (10/10 = 1.0 is symmetric) |

The existing test only exercises the case where `total_deps == vulnerable_deps` (both 10),
so the division produces 1.0 regardless of operand order. No test covers the asymmetric
case where `total != vulnerable`, which is the scenario that exposes the bug.

### CONVENTIONS.md lookup

No `CONVENTIONS.md` file found at the repository root (`/home/dev/repos/acme-backend`).

### Persistence-Impact Analysis

#### Trace: compute_risk_score() output to persistence boundary

```
compute_risk_score(total_deps, vulnerable_deps)
    --> returns f64 score
        --> create_assessment() binds to local variable `score`
            --> diesel::insert_into(assessments::table)
                .values(assessments::risk_score.eq(score))
                    --> PERSISTENCE BOUNDARY: assessments table, risk_score column
```

#### Persistence boundary found

| Property               | Value                                                     |
|------------------------|-----------------------------------------------------------|
| Table                  | `assessments`                                             |
| Column                 | `risk_score` (DOUBLE PRECISION)                           |
| Write operation        | `diesel::insert_into(assessments::table).values(...)` in `create_assessment()` |
| Write location         | `modules/risk/src/assessment.rs`, `create_assessment()` function |
| Write timing           | Ingestion time (once, when assessment is first created)   |
| Recomputed on read?    | No -- `get_assessment()` reads directly from database     |

#### Impact assessment

The `risk_score` value is written to the `assessments` table at ingestion time and is
never recomputed. Fixing `compute_risk_score()` alone will only correct **future**
assessments. All **existing** assessments in the database retain the incorrect
(inflated) risk score. A data migration is required to recompute and correct the
`risk_score` column for all existing rows.

#### Migration conventions

Existing migrations follow the Diesel convention:
- Directory: `migration/`
- Naming pattern: `YYYY-MM-DD-NNNNNN_description/up.sql` and `down.sql`
- Existing migrations:
  - `2024-01-15-000001_create_sboms/`
  - `2024-02-20-000002_create_assessments/`
  - `2024-03-10-000003_add_severity_column/`

A new migration should be created following this pattern, e.g.:
`migration/2024-XX-XX-000004_fix_risk_scores/up.sql`

The migration must recalculate `risk_score` for all existing assessments using the
correct formula: `vulnerable_deps / total_deps` (i.e., inverting the current stored
value, or recomputing from the source SBOM data if available).
