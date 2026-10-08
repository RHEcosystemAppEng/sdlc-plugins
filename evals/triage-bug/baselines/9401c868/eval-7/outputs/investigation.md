# Steps 2-3 -- Codebase Investigation: ACME-520

## Step 2 -- Reproduce/Trace

### Reproduction method: Code-path tracing

The Steps to Reproduce reference API-level operations (SBOM ingestion, assessment creation, GET endpoint) that require a running service. Direct reproduction is not possible in this context. Code-path tracing is used instead.

### Trace findings

**Entry point**: The Steps to Reproduce describe creating a risk assessment for an ingested SBOM and then retrieving it via `GET /api/v2/assessments/{id}`.

**Execution path traced**:

1. Assessment creation calls `create_assessment()` in `modules/risk/src/assessment.rs`.
2. `create_assessment()` calls `compute_risk_score(total_deps, vulnerable_deps)` in `modules/risk/src/score.rs`.
3. The buggy function computes `total_deps as f64 / vulnerable_deps as f64` -- the operands are swapped.
4. For the example inputs (total=100, vulnerable=5), this produces `100 / 5 = 20.0` instead of `5 / 100 = 0.05`.
5. The incorrect score is persisted to the `assessments` table via Diesel `insert_into`.
6. The GET endpoint at `modules/risk/src/endpoints.rs` reads the persisted `risk_score` directly from the database -- it does NOT recompute the score.

**Divergence point**: The bug is in `compute_risk_score()` at `modules/risk/src/score.rs`. The division `total_deps / vulnerable_deps` should be `vulnerable_deps / total_deps`.

**Trace outcome**: Bug behavior confirmed through code-path analysis. The numerator and denominator are swapped in the division.

## Step 3 -- Codebase Investigation

### Target repository

- **Repository**: acme-backend
- **Role**: Rust backend service
- **Serena Instance**: serena_backend
- **Path**: /home/dev/repos/acme-backend

### Affected files and symbols

| File | Symbol | Role |
|------|--------|------|
| `modules/risk/src/score.rs` | `compute_risk_score()` | Buggy function -- division operands swapped |
| `modules/risk/src/assessment.rs` | `create_assessment()` | Caller that persists the incorrect score to DB |
| `modules/risk/src/endpoints.rs` | `get_assessment()` | GET endpoint that reads persisted score (does NOT recompute) |

### Existing test files

| File | Test | Coverage gap |
|------|------|-------------|
| `modules/risk/tests/score_test.rs` | `test_risk_score_all_vulnerable()` | Only tests `compute_risk_score(10, 10)` where `10/10 = 1.0` regardless of operand order. No test exercises the case where `total != vulnerable`. |

### CONVENTIONS.md lookup

No `CONVENTIONS.md` file found at the repository root.

### Persistence-impact analysis

#### Trace: output to persistence boundary

```
compute_risk_score(total_deps, vulnerable_deps)
  -> returns f64 score
    -> create_assessment() in modules/risk/src/assessment.rs
      -> diesel::insert_into(assessments::table)
           .values(assessments::risk_score.eq(score))
         ** PERSISTENCE BOUNDARY FOUND **
```

#### Persistence boundary details

- **Table**: `assessments`
- **Column**: `risk_score` (type: `DOUBLE PRECISION`)
- **Write operation location**: `modules/risk/src/assessment.rs`, function `create_assessment()`
- **Write timing**: Ingestion time -- the score is computed and written once when the assessment is first created. It is NOT recomputed on subsequent reads.

#### Impact assessment

Because the incorrect risk score is persisted at ingestion time, all existing assessment records in the `assessments` table contain inflated (swapped) risk scores. Fixing `compute_risk_score()` alone will only correct **future** assessments. A **data migration** is required to correct existing records.

The migration must:
1. Recompute the `risk_score` column for all existing rows in the `assessments` table.
2. The correct formula is `vulnerable_deps / total_deps`, but since the stored value is `total_deps / vulnerable_deps`, the corrected value is `1.0 / risk_score` (the reciprocal) for any row where `risk_score != 0`.

#### Existing migration pattern

Migration files follow the Diesel convention in `migration/` directory:
```
migration/
  YYYY-MM-DD-NNNNNN_description/
    up.sql
    down.sql
```

Most recent migration: `2024-03-10-000003_add_severity_column/`

The new migration should follow this naming convention, e.g.:
`migration/2024-XX-XX-000004_fix_risk_score_values/up.sql` and `down.sql`.
