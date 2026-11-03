# Steps 2-3 — Reproduce/Trace and Codebase Investigation: ACME-520

## Step 2 — Reproduce / Trace

### Runnable reproduction

The Steps to Reproduce require a running acme-backend service with a database (SBOM
ingestion + assessment creation + `GET /api/v2/assessments/{id}`). That environment is not
available in this triage session, so the bug was not run directly. Code-path tracing was used
instead.

### Code-path trace

Entry point: `GET /api/v2/assessments/{id}` (Steps to Reproduce step 3), backed by assessment
creation (step 2).

1. **Assessment creation** — `modules/risk/src/assessment.rs::create_assessment(conn, sbom_id, total_deps, vulnerable_deps)`
   calls `compute_risk_score(total_deps, vulnerable_deps)`.
2. **Score computation** — `modules/risk/src/score.rs::compute_risk_score(total_deps: u32, vulnerable_deps: u32) -> f64`
   returns `total_deps as f64 / vulnerable_deps as f64`.
   - With the bug's inputs (total = 100, vulnerable = 5): `100 / 5 = 20.0`.
   - Expected: `vulnerable / total = 5 / 100 = 0.05`.
   - **Divergence point**: the division operands are reversed here.
3. **Persistence** — `create_assessment` inserts the score into `assessments.risk_score` via
   `diesel::insert_into(assessments::table).values((..., assessments::risk_score.eq(score), ...))`.
4. **Read path** — `modules/risk/src/endpoints.rs::get_assessment` loads the row with
   `assessments::table.find(id).first::<Assessment>(...)` and serializes it directly. It does
   **not** recompute the score, so it returns the stored `20.0`.

Trace outcome: the Actual Result (`20.0`) is fully explained by the reversed operands in
`compute_risk_score`. Behavior confirmed by code tracing (not by execution).

## Step 3 — Codebase Investigation

### Target repository

- Component `risk-engine` and the referenced symbol `compute_risk_score()` point to
  **acme-backend** (Repository Registry: Serena instance `serena_backend`, path
  `/home/dev/repos/acme-backend`).
- The Code Intelligence section says no Serena servers are configured, so the investigation
  used the Read/Grep/Glob fallback against the repository path.

### Affected files and symbols

| File | Symbol | Role |
|---|---|---|
| `modules/risk/src/score.rs` | `compute_risk_score` | **Defect location**: returns `total_deps / vulnerable_deps` instead of `vulnerable_deps / total_deps` |
| `modules/risk/src/assessment.rs` | `create_assessment` | Caller; persists the computed score to `assessments.risk_score` |
| `modules/risk/src/endpoints.rs` | `get_assessment` | Read endpoint `GET /api/v2/assessments/{id}`; returns the persisted value as-is |

### Callers / impact analysis (`find_referencing_symbols` equivalent via Grep)

- `compute_risk_score` <- `create_assessment` (`modules/risk/src/assessment.rs`), imported via
  `use crate::score::compute_risk_score;`.
- `create_assessment` writes to the `assessments` table. `get_assessment` reads from the same table.
- No other callers of `compute_risk_score` showed up in the repository context.

### Existing tests and patterns

- `modules/risk/tests/score_test.rs::test_risk_score_all_vulnerable` asserts
  `compute_risk_score(10, 10) == 1.0`.
- **Gap**: this test passes even with the bug, because `10 / 10 == 1.0` in either operand
  order. No test covers `total != vulnerable`, which is why the swap went undetected.
- The reproducer test should follow the same pattern: a plain `#[test]` function in
  `modules/risk/tests/score_test.rs` that calls `compute_risk_score` directly.

### Edge case observed

- `compute_risk_score` does no zero-guarding. Today, `vulnerable_deps == 0` causes division by
  zero (`+inf`, or `NaN` when both are 0). After the operands are swapped back, the risky case
  becomes `total_deps == 0` (an SBOM with no dependencies). The fix should guard this case
  (for example, return `0.0` when `total_deps == 0`).

### CONVENTIONS.md

- No `CONVENTIONS.md` exists at the root of acme-backend. Conventions are inferred from existing
  code: Diesel ORM, Diesel migrations, and Rust `#[test]` integration tests under `modules/risk/tests/`.

### Reusable utilities

- `modules/risk/src/score.rs::compute_risk_score`: fix it in place. No new helper is needed.
- The existing Diesel migration layout under `migration/` is the pattern for the data-correction migration.

---

## Persistence-impact analysis

### 1. Trace output to the persistence boundary

```
compute_risk_score(total_deps, vulnerable_deps)        [modules/risk/src/score.rs]
  -> let score = compute_risk_score(...)               [modules/risk/src/assessment.rs::create_assessment]
  -> diesel::insert_into(assessments::table)
       .values(( assessments::risk_score.eq(score), ... ))
  -> PERSISTENCE BOUNDARY FOUND: table `assessments`, column `risk_score`
```

Read side:

```
GET /api/v2/assessments/{id}                           [modules/risk/src/endpoints.rs::get_assessment]
  -> assessments::table.find(id).first::<Assessment>()  (reads stored risk_score, no recomputation)
```

### 2. Persistence boundary details (carried forward to Step 5)

| Attribute | Value |
|---|---|
| Table | `assessments` |
| Column | `risk_score` (`DOUBLE PRECISION`) |
| Write operation | `modules/risk/src/assessment.rs::create_assessment`, `diesel::insert_into(assessments::table)` |
| Write timing | **Ingestion time**: written once when the assessment is created and never recomputed on read or updated afterward |
| Read path | `modules/risk/src/endpoints.rs::get_assessment` returns the stored value directly |

### 3. Impact

- Every assessment created before the fix has a stored `risk_score` equal to
  `total / vulnerable` instead of `vulnerable / total`. These rows never correct themselves.
- Fixing `compute_risk_score()` alone only corrects **future** assessments.
- **A data migration is required** to correct existing `assessments.risk_score` values.

### Recomputation source for the migration

- The `assessments` table stores only `id`, `sbom_id`, `risk_score`, and `created_at`. It does
  **not** store `total_deps` or `vulnerable_deps`.
- Because the bug is a pure operand swap, the stored value is the exact reciprocal of the correct
  value: `stored = total / vulnerable`, so `correct = vulnerable / total = 1 / stored`.
  - Finite, non-zero stored values: correct value is `1.0 / risk_score`.
  - `'Infinity'` stored (vulnerable = 0, total > 0): correct value is `0.0`.
  - `'NaN'` stored (total = 0 and vulnerable = 0): correct value is `0.0`, matching the zero-guard in the code fix.
- Alternative: recompute from source data by joining to the SBOM's dependency and vulnerability
  data via `sbom_id`. This is more robust but depends on tables not covered in this context. The
  implementer should prefer it if the source tables reliably reproduce the counts used at creation
  time. Otherwise, use the reciprocal approach.

### Existing migration convention

- Directory: `migration/` (Diesel)
- Naming: `YYYY-MM-DD-NNNNNN_description/` containing `up.sql` and `down.sql`
- Existing entries: `2024-01-15-000001_create_sboms`, `2024-02-20-000002_create_assessments`,
  `2024-03-10-000003_add_severity_column`
- Next migration: `migration/<YYYY-MM-DD>-000004_fix_assessment_risk_score/{up.sql,down.sql}`
