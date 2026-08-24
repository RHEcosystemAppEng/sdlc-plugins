# Codebase Investigation — ACME-520

## Step 2 — Reproduce / Trace

### Code-path tracing

The bug cannot be directly reproduced (no runnable environment), so we trace through the code paths described in the Steps to Reproduce.

**Entry point**: Ingesting an SBOM and creating a risk assessment, then retrieving it via `GET /api/v2/assessments/{id}`.

**Trace path**:

1. An SBOM with 100 total dependencies and 5 vulnerable dependencies is ingested.
2. A risk assessment is created, which calls `create_assessment()` in `modules/risk/src/assessment.rs`.
3. `create_assessment()` calls `compute_risk_score(total_deps, vulnerable_deps)` in `modules/risk/src/score.rs`.
4. `compute_risk_score()` performs `total_deps as f64 / vulnerable_deps as f64`, which yields `100 / 5 = 20.0`.
5. The correct computation should be `vulnerable_deps as f64 / total_deps as f64`, which would yield `5 / 100 = 0.05`.
6. The result (20.0) is persisted to the `assessments` table via `diesel::insert_into(assessments::table)`.
7. `GET /api/v2/assessments/{id}` reads the persisted `risk_score` directly from the database without recomputing.

**Divergence point**: `compute_risk_score()` in `modules/risk/src/score.rs` — the numerator and denominator are swapped in the division.

**Trace finding**: Confirmed. The bug is in the division operand order in `compute_risk_score()`. Every assessment created since this function was introduced has an incorrect risk score.

## Step 3 — Codebase Investigation

### Target repository

- **Repository**: acme-backend
- **Role**: Rust backend service
- **Serena Instance**: serena_backend (but Code Intelligence is not available per CLAUDE.md)
- **Path**: /home/dev/repos/acme-backend

Since no Serena instances are configured, investigation uses Read/Grep/Glob fallback.

### Affected files and symbols

| File | Symbol | Role |
|------|--------|------|
| `modules/risk/src/score.rs` | `compute_risk_score()` | Buggy function — division operands swapped |
| `modules/risk/src/assessment.rs` | `create_assessment()` | Caller — persists the incorrect score to database |
| `modules/risk/src/endpoints.rs` | `get_assessment()` | Query endpoint — reads persisted score, does NOT recompute |

### Code paths involved

1. `compute_risk_score(total_deps, vulnerable_deps)` returns `total_deps / vulnerable_deps` (WRONG)
2. `create_assessment()` calls `compute_risk_score()` and writes the result to `assessments::risk_score` via `diesel::insert_into(assessments::table)`
3. `get_assessment()` reads `risk_score` directly from the `assessments` table and returns it in the HTTP response

### Existing test files and patterns

- **Test file**: `modules/risk/tests/score_test.rs`
- **Existing test**: `test_risk_score_all_vulnerable` — tests the case where `total == vulnerable` (10/10 = 1.0), which passes regardless of operand order. This test does not catch the bug.
- **Gap**: No test exercises the case where `total != vulnerable`, which is the scenario that exposes the swapped operands.

### CONVENTIONS.md

The repository does not have a CONVENTIONS.md at its root.

### Reusable utilities

- `diesel::prelude::*` — the Diesel ORM is used throughout for database operations
- Existing test pattern in `modules/risk/tests/score_test.rs` provides the assertion style to follow

## Persistence-Impact Analysis

### Trace: output to persistence boundary

```
compute_risk_score(total_deps, vulnerable_deps)   [modules/risk/src/score.rs]
  --> return value assigned to `score`
    --> create_assessment()                        [modules/risk/src/assessment.rs]
      --> diesel::insert_into(assessments::table)
            .values(assessments::risk_score.eq(score))
```

**Persistence boundary found.**

### Persistence boundary details

- **Table**: `assessments`
- **Column**: `risk_score` (type: `DOUBLE PRECISION`)
- **Write operation location**: `modules/risk/src/assessment.rs`, function `create_assessment()`
- **Write timing**: Ingestion time — the risk score is computed and persisted when the assessment is first created. It is NOT recomputed on read.

### Impact

Fixing `compute_risk_score()` alone will only correct **future** assessments. All existing assessments created before the fix retain the incorrect (inflated) risk score in the `assessments.risk_score` column. A **data migration** is needed to recompute and correct existing records.

### Existing migration convention

- **Migration directory**: `migration/`
- **Naming convention**: `YYYY-MM-DD-NNNNNN_description/up.sql` (Diesel convention)
- **Existing migrations**:
  - `migration/2024-01-15-000001_create_sboms/`
  - `migration/2024-02-20-000002_create_assessments/`
  - `migration/2024-03-10-000003_add_severity_column/`
- **Next migration**: Should follow the pattern, e.g., `migration/2026-08-24-000004_fix_risk_scores/up.sql`
