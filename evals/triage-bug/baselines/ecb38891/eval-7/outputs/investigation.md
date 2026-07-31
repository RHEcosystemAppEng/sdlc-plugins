# Steps 2-3 -- Codebase Investigation Findings

## Step 2 -- Reproduce/Trace

### Reproduction approach

The Steps to Reproduce describe API interactions (ingesting an SBOM, creating an assessment,
querying via GET endpoint). This is a code-path tracing scenario -- the bug involves a
computation error in `compute_risk_score()` whose output is persisted to the database.

### Code-path trace

**Entry point**: The risk assessment creation flow is triggered when a user creates an
assessment for an ingested SBOM. The `create_assessment()` function in
`modules/risk/src/assessment.rs` calls `compute_risk_score()` and persists the result.

**Trace through risk score computation**:

1. `create_assessment()` receives `total_deps` and `vulnerable_deps` as parameters.
2. It calls `compute_risk_score(total_deps, vulnerable_deps)` in `modules/risk/src/score.rs`.
3. `compute_risk_score()` computes `total_deps as f64 / vulnerable_deps as f64`.
4. For input (total=100, vulnerable=5), this produces `100.0 / 5.0 = 20.0`.
5. The correct computation should be `vulnerable_deps as f64 / total_deps as f64`,
   which would produce `5.0 / 100.0 = 0.05`.

**Divergence point**: The division operands in `compute_risk_score()` are reversed.
The numerator (`total_deps`) and denominator (`vulnerable_deps`) are swapped.

**Trace through persistence**:

6. The result (20.0) is returned to `create_assessment()`.
7. `create_assessment()` writes this value to `assessments::risk_score` via
   `diesel::insert_into(assessments::table)`.
8. The `GET /api/v2/assessments/{id}` endpoint in `modules/risk/src/endpoints.rs`
   reads this persisted value directly from the database -- it does NOT recompute
   the score.

### Reproduction outcome

**Confirmed via code-path trace.** The division operands in `compute_risk_score()` are
reversed: `total_deps / vulnerable_deps` instead of `vulnerable_deps / total_deps`.
This produces inflated risk scores (20.0 instead of 0.05 for the given example).

## Step 3 -- Codebase Investigation

### Target repository

- **Repository**: acme-backend
- **Serena Instance**: serena_backend
- **Path**: /home/dev/repos/acme-backend
- **Component**: risk-engine

### Affected files and symbols

| File | Symbol/Location | Issue |
|------|-----------------|-------|
| `modules/risk/src/score.rs` | `compute_risk_score()` | Division operands are swapped: `total_deps / vulnerable_deps` instead of `vulnerable_deps / total_deps` |
| `modules/risk/src/assessment.rs` | `create_assessment()` | Persists the incorrect risk score to `assessments::risk_score` column via Diesel insert |
| `modules/risk/src/endpoints.rs` | `get_assessment()` | Reads persisted `risk_score` from database -- does not recompute, so existing incorrect values are served as-is |

### Existing test coverage

| Test File | Coverage |
|-----------|----------|
| `modules/risk/tests/score_test.rs` | Contains `test_risk_score_all_vulnerable` which tests `compute_risk_score(10, 10)` -- this passes even with the bug because `10 / 10 = 1.0` regardless of operand order. No test exercises the case where `total != vulnerable`. |

### CONVENTIONS.md lookup

The repository does not have a `CONVENTIONS.md` at its root. No additional conventions
apply to the fix task.

### Persistence-impact analysis

**Persistence boundary found.**

1. **Trace output to persistence boundary**:
   - `compute_risk_score()` returns an `f64` risk score.
   - `create_assessment()` in `modules/risk/src/assessment.rs` receives this return value
     and writes it to the database via:
     ```rust
     diesel::insert_into(assessments::table)
         .values((
             assessments::sbom_id.eq(sbom_id),
             assessments::risk_score.eq(score),  // <-- persistence boundary
             assessments::created_at.eq(now),
         ))
         .get_result(conn)
     ```

2. **Persistence details**:
   - **Table**: `assessments`
   - **Column**: `risk_score` (type: `DOUBLE PRECISION`)
   - **Write operation location**: `modules/risk/src/assessment.rs`, `create_assessment()` function
   - **Write timing**: Ingestion time -- the risk score is computed and persisted once when
     the assessment is first created. It is NOT recomputed on read.

3. **Impact**: All existing assessments in the database have incorrect (inflated) risk scores.
   Fixing `compute_risk_score()` alone will only correct future assessments. A data migration
   is required to recompute and correct the `risk_score` column for all existing records.

4. **Migration pattern**: Existing migrations follow the Diesel convention in the `migration/`
   directory with format `YYYY-MM-DD-NNNNNN_description/{up.sql,down.sql}`. The latest
   migration is `2024-03-10-000003_add_severity_column/`.

### Reuse candidates

- `modules/risk/tests/score_test.rs` -- existing test file for `compute_risk_score()`;
  the reproducer test should be added here
- `migration/` directory -- existing Diesel migration infrastructure for the data migration
- `modules/risk/src/assessment.rs::create_assessment()` -- caller that demonstrates how the
  score is computed from `total_deps` and `vulnerable_deps`, informing the migration's
  recomputation logic

### Key findings

1. **Single root cause**: The bug has a single root cause (swapped division operands in
   `compute_risk_score()`) that manifests in one code path. No decomposition is needed.
2. **Persistence impact**: The incorrect risk scores are persisted to the `assessments`
   table at ingestion time. A data migration is required to correct existing records.
3. **Insufficient test coverage**: The only existing test uses equal values for both
   parameters (`10, 10`), which masks the bug. A reproducer test with unequal values
   is needed.
4. **Fix is localized**: The code fix requires swapping the operands in one function.
   The data migration requires an UPDATE query to recompute scores from source data.
