# Steps 2-3: Codebase Investigation

## Step 2: Code-Path Tracing

The bug cannot be directly reproduced in this environment (no running service), so a code-path trace is performed.

### Entry point

The Steps to Reproduce describe creating a risk assessment for an SBOM and then retrieving it via `GET /api/v2/assessments/{id}`. The inflated risk score is observed in the response. The trace starts at the risk score computation and follows the value through persistence and retrieval.

### Trace

1. `compute_risk_score(total_deps, vulnerable_deps)` in `modules/risk/src/score.rs` -- performs `total_deps as f64 / vulnerable_deps as f64`, which is the inverse of the intended formula.
2. `create_assessment()` in `modules/risk/src/assessment.rs` -- calls `compute_risk_score()` and inserts the result into the `assessments` table via `diesel::insert_into(assessments::table).values(...)`, persisting the incorrect score at `assessments::risk_score`.
3. `get_assessment()` in `modules/risk/src/endpoints.rs` -- reads the `risk_score` directly from the database and returns it in the JSON response. It does NOT recompute the score.

### Divergence point

The divergence occurs in step 1: `compute_risk_score()` divides `total_deps / vulnerable_deps` instead of `vulnerable_deps / total_deps`. For the example in the bug report (100 total, 5 vulnerable), this produces `20.0` instead of `0.05`.

## Step 3: Codebase Investigation Findings

### Target repository

- **Repository**: acme-backend
- **Path**: /home/dev/repos/acme-backend
- **Serena Instance**: serena_backend (but Code Intelligence not available per CLAUDE.md)

### Finding 1: Swapped operands in compute_risk_score

**File**: `modules/risk/src/score.rs`
**Function**: `compute_risk_score(total_deps: u32, vulnerable_deps: u32) -> f64`

The division is `total_deps as f64 / vulnerable_deps as f64`. The correct formula should be `vulnerable_deps as f64 / total_deps as f64`. The operands are swapped.

### Finding 2: Existing test does not catch the bug

**File**: `modules/risk/tests/score_test.rs`
**Test**: `test_risk_score_all_vulnerable`

```rust
#[test]
fn test_risk_score_all_vulnerable() {
    let score = compute_risk_score(10, 10);
    assert_eq!(score, 1.0);
}
```

This test passes with both the correct and buggy formulas because `10 / 10 = 1.0` regardless of operand order. No test exercises the case where `total_deps != vulnerable_deps`, which would expose the inversion.

### Finding 3: No CONVENTIONS.md

The repository does not have a `CONVENTIONS.md` at its root. No project-specific conventions to incorporate.

### Finding 4: Existing migration patterns

**Directory**: `migration/`

Migrations follow the Diesel convention with timestamped directory names:
- `2024-01-15-000001_create_sboms/`
- `2024-02-20-000002_create_assessments/`
- `2024-03-10-000003_add_severity_column/`

Each migration directory contains `up.sql` and `down.sql` files.

## Persistence-Impact Analysis

### Trace: output to persistence boundary

1. `compute_risk_score()` returns `f64` in `modules/risk/src/score.rs`
2. `create_assessment()` in `modules/risk/src/assessment.rs` calls `compute_risk_score()` and immediately writes the result via:
   ```rust
   diesel::insert_into(assessments::table)
       .values((
           assessments::sbom_id.eq(sbom_id),
           assessments::risk_score.eq(score),  // <-- persistence boundary
           assessments::created_at.eq(now),
       ))
       .get_result(conn)
   ```

### Persistence boundary found

- **Table**: `assessments`
- **Column**: `risk_score` (DOUBLE PRECISION)
- **Write operation location**: `modules/risk/src/assessment.rs`, function `create_assessment()`
- **Write timing**: Ingestion time -- the score is computed and persisted once when the assessment is first created. It is NOT recomputed on read.

### Impact

All existing assessment records in the `assessments` table contain incorrect (inflated) risk scores. Fixing `compute_risk_score()` alone will only correct future assessments. Existing records retain the wrong value because `get_assessment()` reads the persisted score directly from the database without recomputation.

**A data migration is required** to correct the `risk_score` column for all existing rows in the `assessments` table. The correct score can be recomputed by joining with the source SBOM data (total and vulnerable dependency counts) and applying the corrected formula: `vulnerable_deps / total_deps`.
