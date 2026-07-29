# Steps 2-3 -- Codebase Investigation: ACME-520

## Step 2 -- Reproduce/Trace

### Reproduction method: Code-path tracing

The Steps to Reproduce describe an API-based workflow (SBOM ingestion, assessment
creation, assessment retrieval) that cannot be directly executed in this context.
Code-path tracing is used instead.

### Trace findings

**Entry point**: SBOM ingestion triggers `create_assessment()`, which calls
`compute_risk_score()` and persists the result.

**Divergence point**: In `compute_risk_score(total_deps, vulnerable_deps)`, the
function computes `total_deps as f64 / vulnerable_deps as f64`. For the scenario
in Steps to Reproduce (100 total, 5 vulnerable):

- **Expected**: `5 / 100 = 0.05` (vulnerable / total)
- **Actual**: `100 / 5 = 20.0` (total / vulnerable)

The numerator and denominator are swapped. The trace confirms the bug as described.

**Reproduction outcome**: Confirmed via code-path tracing. The division operands
are reversed in the function body.

## Step 3 -- Codebase Investigation

### Target repository

- **Repository**: acme-backend
- **Role**: Rust backend service
- **Serena Instance**: serena_backend (not available in this context)
- **Path**: /home/dev/repos/acme-backend
- **Component match**: risk-engine maps to `modules/risk/`

### Affected files and symbols

| File | Symbol | Role |
|------|--------|------|
| `modules/risk/src/score.rs` | `compute_risk_score()` | Buggy function -- division operands swapped |
| `modules/risk/src/assessment.rs` | `create_assessment()` | Caller that persists the buggy result to DB |
| `modules/risk/src/endpoints.rs` | `get_assessment()` | Query endpoint -- reads persisted value, does NOT recompute |

### Code path analysis

1. `compute_risk_score(total_deps, vulnerable_deps)` in `modules/risk/src/score.rs`
   returns `total_deps as f64 / vulnerable_deps as f64` (incorrect).

2. `create_assessment()` in `modules/risk/src/assessment.rs` calls
   `compute_risk_score(total_deps, vulnerable_deps)` and binds the result to `score`.

3. `create_assessment()` then executes `diesel::insert_into(assessments::table)`
   with `.values((..., assessments::risk_score.eq(score), ...))`, persisting the
   incorrect score to the `assessments` table, `risk_score` column.

4. `get_assessment()` in `modules/risk/src/endpoints.rs` reads the `risk_score`
   directly from the database via `assessments::table.find(id).first()` -- it does
   NOT recompute the score.

### Persistence-impact analysis

**Trace**: `compute_risk_score()` return value --> `create_assessment()` local
variable `score` --> `diesel::insert_into(assessments::table).values(assessments::risk_score.eq(score))`

**Persistence boundary found**:
- **Table**: `assessments`
- **Column**: `risk_score` (type: `DOUBLE PRECISION`)
- **Write operation location**: `modules/risk/src/assessment.rs`, function `create_assessment()`
- **Write timing**: Ingestion time -- the score is computed and written once when the
  assessment is first created. It is never recomputed or updated on subsequent reads.

**Consequence**: Fixing `compute_risk_score()` alone will only correct future
assessments. All existing assessments in the `assessments` table have inflated
`risk_score` values (total/vulnerable instead of vulnerable/total). A data migration
is required to correct the existing records.

**Migration correction logic**: For each existing assessment, the correct risk score
can be recomputed as `vulnerable_deps / total_deps`. Since the incorrect value is
`total_deps / vulnerable_deps`, the correct value is `1.0 / risk_score` (the
reciprocal of the stored value). However, this reciprocal approach only works if
`risk_score > 0`. Alternatively, the migration can join with the source SBOM data
to recompute from the original `total_deps` and `vulnerable_deps` values.

### Existing test analysis

**File**: `modules/risk/tests/score_test.rs`

```rust
#[test]
fn test_risk_score_all_vulnerable() {
    let score = compute_risk_score(10, 10);
    assert_eq!(score, 1.0);
}
```

This test passes even with the bug because `10 / 10 = 1.0` regardless of operand
order. No test exercises the case where `total_deps != vulnerable_deps`, which is
what would expose the swapped operands.

### Existing migration conventions

Migrations are in the `migration/` directory and follow the Diesel convention:
`YYYY-MM-DD-NNNNNN_description/up.sql` with corresponding `down.sql` files.

Existing migrations:
- `2024-01-15-000001_create_sboms/`
- `2024-02-20-000002_create_assessments/`
- `2024-03-10-000003_add_severity_column/`

A new migration file should follow this pattern, e.g.,
`2026-07-29-000004_fix_risk_score_values/up.sql`.

### CONVENTIONS.md

No `CONVENTIONS.md` file found at the repository root.
