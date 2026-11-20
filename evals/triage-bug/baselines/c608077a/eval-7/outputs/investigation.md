# Steps 2–3 — Reproduce/Trace and Codebase Investigation (ACME-520)

## Step 2 — Reproduce/Trace

### Runnable reproduction

The Steps to Reproduce require a running acme-backend service and database: ingest an SBOM, create an assessment, then call `GET /api/v2/assessments/{id}`. Neither is available in this session, and the skill is read-only, so the bug was **not run directly**. Outcome: **environment-dependent**. Code-path tracing was used instead.

### Code-path trace

1. **Entry point (write path)**: creating an assessment calls `create_assessment(conn, sbom_id, total_deps, vulnerable_deps)` in `modules/risk/src/assessment.rs`.
2. `create_assessment` calls `compute_risk_score(total_deps, vulnerable_deps)` in `modules/risk/src/score.rs`.
3. `compute_risk_score` returns `total_deps as f64 / vulnerable_deps as f64`. **This is where actual behavior diverges from expected.** With inputs `(100, 5)` it returns `20.0`; the expected value is `0.05`.
4. `create_assessment` writes the returned score with `diesel::insert_into(assessments::table)` into `assessments.risk_score`.
5. **Entry point (read path)**: `GET /api/v2/assessments/{id}` is handled by `get_assessment` in `modules/risk/src/endpoints.rs`. It loads the row with `assessments::table.find(id).first::<Assessment>()` and returns it as JSON. **The score is not recomputed on read.**

The trace matches the reported Actual Result exactly: `100 / 5 = 20.0`.

## Step 3 — Codebase Investigation

### Target repository

- Component `risk-engine`, plus the symbol named in the description (`compute_risk_score`), point to **acme-backend**.
- Registry entry: `acme-backend`, Serena instance `serena_backend`, path `/home/dev/repos/acme-backend`.
- Code Intelligence says no Serena servers are configured. The investigation therefore used the **Read/Grep/Glob fallback**, run against the mock repository context.

### Affected files and symbols

| File | Symbol | Role |
|---|---|---|
| `modules/risk/src/score.rs` | `compute_risk_score(total_deps: u32, vulnerable_deps: u32) -> f64` | **Defect**: the division operands are reversed |
| `modules/risk/src/assessment.rs` | `create_assessment(conn, sbom_id, total_deps, vulnerable_deps) -> Result<Assessment, Error>` | Only caller found; persists the score |
| `modules/risk/src/endpoints.rs` | `get_assessment(path, db)` (`GET /api/v2/assessments/{id}`) | Reads the persisted score and returns it unchanged |
| `modules/risk/tests/score_test.rs` | `test_risk_score_all_vulnerable` | Existing unit test; it does not catch the bug |

### Reference / impact analysis (`find_referencing_symbols` equivalent)

- `compute_risk_score` → referenced by `create_assessment` (`modules/risk/src/assessment.rs`, via `use crate::score::compute_risk_score;`).
- `create_assessment` → writes to the `assessments` table.
- `assessments.risk_score` → read by `get_assessment` (`modules/risk/src/endpoints.rs`).

No other callers of `compute_risk_score` appear in the repository context.

### Existing tests and patterns

- `modules/risk/tests/score_test.rs` contains:
  ```rust
  #[test]
  fn test_risk_score_all_vulnerable() {
      let score = compute_risk_score(10, 10);
      assert_eq!(score, 1.0);
  }
  ```
- This test passes even with the bug, because `10 / 10 == 1.0` in either operand order. **No test covers `total != vulnerable`**, which is why the defect was not caught.
- The reproducer test should follow this file's pattern: a plain `#[test]` function calling `compute_risk_score` directly and checking the result with `assert_eq!`.

### Edge cases found during investigation

- The buggy code divides by `vulnerable_deps`. When an SBOM has **0 vulnerable deps**, it yields `+inf` (f64 division by zero), which Postgres `DOUBLE PRECISION` stores as `Infinity`. The correct value in that case is `0.0`.
- After the fix the divisor becomes `total_deps`. An SBOM with **0 total deps** would then yield `NaN` (0/0). The fix should define this case explicitly; returning `0.0` is the natural choice.

### Reusable utilities

None found beyond `compute_risk_score` itself. The fix is a one-line operand correction plus a zero guard.

### Migration conventions

- Migration directory: `migration/` at the repository root.
- Existing migrations:
  - `migration/2024-01-15-000001_create_sboms/{up.sql,down.sql}`
  - `migration/2024-02-20-000002_create_assessments/{up.sql,down.sql}`
  - `migration/2024-03-10-000003_add_severity_column/{up.sql,down.sql}`
- Convention: Diesel, `YYYY-MM-DD-NNNNNN_description/` containing `up.sql` and `down.sql`. The sequence number increments across migrations, so the next one is `000004`.

### CONVENTIONS.md

The acme-backend root has **no CONVENTIONS.md**. No additional conventions apply.

---

## Persistence-impact analysis

### Trace from buggy output to persistence boundary

```
compute_risk_score(total_deps, vulnerable_deps)        [modules/risk/src/score.rs]
  └─> let score = ...                                  [modules/risk/src/assessment.rs::create_assessment]
        └─> diesel::insert_into(assessments::table)
              .values(assessments::risk_score.eq(score))  ← PERSISTENCE BOUNDARY FOUND
```

Read path, which confirms there is no recomputation:

```
GET /api/v2/assessments/{id}  [modules/risk/src/endpoints.rs::get_assessment]
  └─> assessments::table.find(id).first::<Assessment>()  → returns stored risk_score as-is
```

### Findings carried forward to Step 5

| Item | Value |
|---|---|
| Persistence boundary found | **Yes** |
| Table | `assessments` |
| Column | `risk_score` (`DOUBLE PRECISION`) |
| Write operation location | `modules/risk/src/assessment.rs::create_assessment`, `diesel::insert_into(assessments::table).values((... assessments::risk_score.eq(score) ...))` |
| Write timing | **Ingestion time**: written once when the assessment is created and never recomputed on read or updated afterwards |
| Self-correcting? | **No.** Fixing `compute_risk_score()` only fixes assessments created after the fix. Every existing row keeps its inflated `risk_score`. |
| Data migration required | **Yes** |

### Implications for the migration

- The `assessments` table stores only `id`, `sbom_id`, `risk_score` and `created_at`. It does **not** store `total_deps` or `vulnerable_deps`, so the score cannot be recomputed from that table alone.
- **Option A (preferred if source data is reachable in SQL):** recompute `vulnerable / total` from the SBOM's dependency and vulnerability data, joined via `sbom_id`. This is the most accurate approach. The implementer must confirm which tables hold the dependency and vulnerability counts; they were not part of the investigated context.
- **Option B (algebraic correction):** every stored value equals `total / vulnerable`, so the correct value is its reciprocal, `vulnerable / total = 1 / stored`. Two special cases:
  - stored `Infinity` (vulnerable = 0) → correct value `0.0`
  - stored `NaN` (total = 0 and vulnerable = 0) → correct value `0.0`
- **Idempotency risk:** Option B is not idempotent. Applying it twice, or to rows written after the code fix, would corrupt correct values. The migration must run exactly once, in the same deployment as the code fix and before any new assessments are created with the fixed code. Diesel's migration tracking helps here. Alternatively, a `created_at` cutoff could be used.
- The correct score lies in `[0, 1]`, since vulnerable ≤ total. The buggy score is always `>= 1` (or `Infinity`/`NaN`). A `WHERE risk_score > 1` filter therefore also protects already-correct rows; the exception is the `10/10 = 1.0` case, where both formulas agree and no change is needed anyway.

### Decomposition Guard (Step 6) assessment

There is one root cause, the swapped operands in `compute_risk_score`. The data migration is a direct consequence of that same defect, not an independent issue, so the decomposition guard does **not** trigger. A single Task is appropriate.
