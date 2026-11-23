# Steps 2–3 — Reproduce/Trace and Codebase Investigation (ACME-520)

## Step 2 — Reproduce/Trace

### Runnable reproduction
The Steps to Reproduce require a running acme-backend with a database: ingest an SBOM, create an assessment, then call `GET /api/v2/assessments/{id}`. No such environment is available, and the eval forbids external calls, so the bug was **not run**. Outcome: **environment-dependent**. Code-path tracing was used instead.

### Code-path trace
1. **Entry point (assessment creation):** `modules/risk/src/assessment.rs::create_assessment(conn, sbom_id, total_deps, vulnerable_deps)`
2. It calls `modules/risk/src/score.rs::compute_risk_score(total_deps, vulnerable_deps)`:
   ```rust
   total_deps as f64 / vulnerable_deps as f64   // BUG: operands swapped
   ```
   With the bug's inputs (total = 100, vulnerable = 5) this returns `100 / 5 = 20.0`.
3. `create_assessment` writes the returned value with `diesel::insert_into(assessments::table).values((..., assessments::risk_score.eq(score), ...))`.
4. **Entry point (retrieval):** `modules/risk/src/endpoints.rs::get_assessment` runs `assessments::table.find(id).first::<Assessment>()` and serializes the stored row as-is. It does not recompute anything.
5. **Where the behavior diverges:** in `compute_risk_score`. The expected formula is `vulnerable / total` (0.05). The code computes `total / vulnerable` (20.0).

The traced behavior matches the reported Actual Result exactly.

## Step 3 — Codebase Investigation

### Target repository
- Component `risk-engine`, the bug's code references and the `/api/v2/assessments` endpoint all point to **acme-backend**.
- Registry entry: Serena instance `serena_backend`, path `/home/dev/repos/acme-backend`.
- The Code Intelligence section says no Serena servers are configured, so Read/Grep/Glob were used. In this eval, the simulated repository context in `repo-context-persistence-mock.md` stood in for them.

### Affected files and symbols

| File | Symbol | Role |
|---|---|---|
| `modules/risk/src/score.rs` | `compute_risk_score(total_deps: u32, vulnerable_deps: u32) -> f64` | **Defect.** The division operands are reversed. |
| `modules/risk/src/assessment.rs` | `create_assessment(...)` | Only caller found. Persists the score into `assessments.risk_score`. |
| `modules/risk/src/endpoints.rs` | `get_assessment(...)` | `GET /api/v2/assessments/{id}`. Returns the persisted score unchanged. |
| `modules/risk/tests/score_test.rs` | `test_risk_score_all_vulnerable` | Existing unit test. It cannot detect the bug: `compute_risk_score(10, 10)` returns 1.0 whichever way the operands go. |

### Impact analysis (callers/consumers)
- `compute_risk_score` → called by `create_assessment` (the only caller in the provided context).
- `assessments.risk_score` → read by `get_assessment` (`GET /api/v2/assessments/{id}`). That makes every API consumer of assessments exposed to the wrong values.

### Edge cases found
- **`vulnerable_deps == 0`:** the current code divides by zero and returns `+inf`. That means existing rows for SBOMs with no vulnerable dependencies may hold `Infinity`, when the correct score is `0.0`.
- **`total_deps == 0`:** after the fix, `0 / 0` gives `NaN`. The fix should guard this case and return `0.0`.
- **`total_deps == vulnerable_deps`:** gives 1.0 either way. These rows are already correct.

### Test patterns
- Tests live in `modules/risk/tests/score_test.rs`. They are plain `#[test]` functions that call `compute_risk_score` directly and use `assert_eq!` on the `f64` result.
- No test covers `total != vulnerable`. The reproducer belongs in this file.

### CONVENTIONS.md
There is no `CONVENTIONS.md` at the root of acme-backend, so the Implementation Notes follow the patterns already in the code.

### Reuse candidates
- `modules/risk/src/score.rs::compute_risk_score`: fix it in place. No new helper is needed.
- The existing Diesel migration layout under `migration/` provides the pattern for the data migration.

## Persistence-Impact Analysis

### Trace from the buggy function to the persistence boundary
```
compute_risk_score()                       (modules/risk/src/score.rs)
  → let score = compute_risk_score(...)    (modules/risk/src/assessment.rs::create_assessment)
  → diesel::insert_into(assessments::table)
        .values(assessments::risk_score.eq(score))
  → PERSISTENCE BOUNDARY FOUND: table `assessments`, column `risk_score`
```

### Findings
| Item | Value |
|---|---|
| Persistence boundary found? | **Yes** |
| Table | `assessments` |
| Column | `risk_score` (`DOUBLE PRECISION`) |
| Write operation | `modules/risk/src/assessment.rs::create_assessment`, a `diesel::insert_into(assessments::table)` call |
| Write timing | **Ingestion time.** The value is written once, when the assessment is created, and is never recomputed. |
| Read path | `modules/risk/src/endpoints.rs::get_assessment` reads the stored value directly, with no recomputation. |

### Consequence
Fixing `compute_risk_score()` only corrects assessments created after the fix. Every existing row in `assessments` keeps its inverted `risk_score`, and the data will not correct itself. **A data migration is required** alongside the code fix.

### Migration source data
- The `assessments` table stores only `id`, `sbom_id`, `risk_score` and `created_at`. It does not keep the original `total_deps` / `vulnerable_deps` inputs.
- Because the bug is a pure operand swap, every stored value is `total / vulnerable`, and the correct value is its exact reciprocal: `correct = 1 / stored`, whenever `stored` is finite and greater than 0.
- Special stored values:
  - `'Infinity'` (vulnerable = 0): the correct value is `0.0`.
  - `'NaN'` (0/0): the correct value is `0.0`.
  - `1.0` (total = vulnerable): the reciprocal is also `1.0`, so these rows are unaffected.
- Alternative: recompute from the source dependency/vulnerability data linked through `sbom_id`. This is only viable if those counts can be derived reliably in SQL. The reciprocal approach is exact and self-contained, so it is the recommended one.

### Existing migration convention
- Directory: `migration/` (Diesel).
- Naming: `YYYY-MM-DD-NNNNNN_description/` containing `up.sql` and `down.sql`.
- Existing migrations: `2024-01-15-000001_create_sboms`, `2024-02-20-000002_create_assessments`, `2024-03-10-000003_add_severity_column`.
- Next migration: sequence `000004`, dated on the day it is authored. Proposed: `migration/<YYYY-MM-DD>-000004_fix_inverted_risk_scores/`.

## Step 6 — Decomposition Guard check
There is one root cause (swapped operands in `compute_risk_score`). It shows up in stored data, which the migration addresses. The code fix and the data migration correct the same defect, so they are not independent root causes. **No decomposition prompt is needed**, and a single Task is appropriate.
