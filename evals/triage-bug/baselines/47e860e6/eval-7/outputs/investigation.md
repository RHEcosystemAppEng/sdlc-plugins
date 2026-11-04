# Steps 2–3 — Reproduce/Trace and Codebase Investigation: ACME-520

## Step 2 — Reproduce/Trace

### Runnable reproduction

The Steps to Reproduce require a running acme-backend instance with a database (ingest SBOM, create an assessment, call `GET /api/v2/assessments/{id}`). In this eval no service is running and no external tools are invoked, so direct reproduction is **environment-dependent / not performed**. Code-path tracing is used instead.

### Code-path trace

Entry point: `GET /api/v2/assessments/{id}` (Steps to Reproduce, step 3), with the value having been produced by assessment creation (step 2).

1. **Assessment creation (write path)**
   `modules/risk/src/assessment.rs::create_assessment(conn, sbom_id, total_deps, vulnerable_deps)`
   → calls `compute_risk_score(total_deps, vulnerable_deps)`
2. **Score computation (defect)**
   `modules/risk/src/score.rs::compute_risk_score(total_deps: u32, vulnerable_deps: u32) -> f64`
   → returns `total_deps as f64 / vulnerable_deps as f64`
   With the reproduction input (`total_deps = 100`, `vulnerable_deps = 5`): `100 / 5 = 20.0`. Expected is `5 / 100 = 0.05`.
   **This is where actual behavior diverges from expected behavior.**
3. **Persistence**
   `create_assessment` → `diesel::insert_into(assessments::table).values((..., assessments::risk_score.eq(score), ...))`
   → the wrong value `20.0` is stored in `assessments.risk_score`.
4. **Read path**
   `modules/risk/src/endpoints.rs::get_assessment` → `assessments::table.find(id).first::<Assessment>(...)` → serializes the row as JSON.
   The stored `risk_score` (20.0) is returned as-is; no recomputation.

Trace result: the Actual Result (`20.0`) is fully explained by the swapped operands in `compute_risk_score`. Confirmed by code inspection.

## Step 3 — Codebase Investigation

### Target repository

- Component `risk-engine` and file paths in the description (`compute_risk_score()`) point to **acme-backend**.
- Registry: `acme-backend` | Serena instance `serena_backend` | Path `/home/dev/repos/acme-backend`.
- The Code Intelligence section states no Serena MCP servers are configured, so the **Read/Grep/Glob fallback** applies (simulated here from repo-context-persistence-mock.md). With Serena available, the equivalent calls would be `mcp__serena_backend__find_symbol(name_path_pattern="compute_risk_score", substring_matching=true)` and `mcp__serena_backend__find_referencing_symbols(...)`.

### Affected files and symbols

| File | Symbol | Role |
|---|---|---|
| `modules/risk/src/score.rs` | `compute_risk_score` | **Defect** — operands of the division are swapped |
| `modules/risk/src/assessment.rs` | `create_assessment` | Sole caller found; persists the score to the DB |
| `modules/risk/src/endpoints.rs` | `get_assessment` | Read endpoint `GET /api/v2/assessments/{id}`; returns the persisted value without recomputing |
| `modules/risk/tests/score_test.rs` | `test_risk_score_all_vulnerable` | Existing test — passes despite the bug (`10/10 == 1.0` either way) |
| `migration/` | Diesel migrations | Location for the data-correction migration |

### Impact analysis (references to `compute_risk_score`)

- `modules/risk/src/assessment.rs::create_assessment` — the only caller in the mock context. It uses the result directly as `assessments::risk_score`.
- Every assessment ever created has an inflated score (total/vulnerable ≥ 1 whenever total ≥ vulnerable), so all API consumers of `risk_score` are affected.

### Additional edge case found during investigation

`compute_risk_score` performs unguarded `f64` division:
- Current code with `vulnerable_deps == 0` → `total / 0.0 = +Infinity` (persisted as `'Infinity'` in a `DOUBLE PRECISION` column).
- Current code with `total_deps == 0 && vulnerable_deps == 0` → `NaN`.
- After the fix, `vulnerable_deps / total_deps` with `total_deps == 0` → `NaN` (or `Infinity` if vulnerable > 0, which should be impossible).
This is part of the same function and is worth handling in the fix (return `0.0` when `total_deps == 0`), and the migration must handle existing `'Infinity'` rows.

### Existing test patterns

- `modules/risk/tests/score_test.rs` contains `#[test] fn test_risk_score_all_vulnerable()` using `assert_eq!(compute_risk_score(10, 10), 1.0)`.
- Gap: no test covers `total != vulnerable`, which is why the swap went undetected. The reproducer should be added to this file following the same `#[test]` + direct-call + `assert_eq!` pattern.

### Reusable code / patterns

- `modules/risk/src/score.rs::compute_risk_score` — fix in place; no new helper needed.
- `migration/2024-02-20-000002_create_assessments/up.sql` — defines the `assessments` table; reference for column names/types.
- `migration/2024-03-10-000003_add_severity_column/` — most recent migration; naming/sequence reference.

### CONVENTIONS.md

No `CONVENTIONS.md` exists at the root of acme-backend. Implementation Notes rely on observed patterns (Diesel migrations, `#[test]` unit tests in `modules/risk/tests/`).

---

## Persistence-Impact Analysis

### 1. Trace output to persistence boundary

```
compute_risk_score(total_deps, vulnerable_deps) -> f64          [modules/risk/src/score.rs]
  └─ caller: create_assessment(...)                             [modules/risk/src/assessment.rs]
       let score = compute_risk_score(total_deps, vulnerable_deps);
       diesel::insert_into(assessments::table)
           .values(( ..., assessments::risk_score.eq(score), ... ))   <-- PERSISTENCE BOUNDARY
```

Read side (confirms no recomputation):

```
GET /api/v2/assessments/{id} -> get_assessment(...)             [modules/risk/src/endpoints.rs]
  └─ assessments::table.find(id).first::<Assessment>(...)       reads stored risk_score verbatim
```

### 2. Persistence boundary found

| Attribute | Value |
|---|---|
| **Table** | `assessments` |
| **Column** | `risk_score` (`DOUBLE PRECISION`) |
| **Write operation** | `modules/risk/src/assessment.rs::create_assessment` — `diesel::insert_into(assessments::table).values(... assessments::risk_score.eq(score) ...)` |
| **Write timing** | **Ingestion time** — written once when the assessment is created; never updated or recomputed on read |
| **Read path** | `modules/risk/src/endpoints.rs::get_assessment` returns the stored value directly |

### 3. Conclusion

**Data migration required.** Fixing `compute_risk_score()` only corrects assessments created after the fix is deployed. All existing rows in `assessments.risk_score` hold the inverted value (`total / vulnerable`) and are never self-correcting because the read endpoint does not recompute.

### Migration feasibility (carried forward to Step 5)

- The `assessments` table does **not** store `total_deps` or `vulnerable_deps`, so the score cannot be recomputed from columns on the same row.
- However, the bug is a pure operand swap: stored = `total / vulnerable`, correct = `vulnerable / total` = `1 / stored`. The correct value can be derived exactly from the stored value:
  - `stored > 1` (finite) → correct = `1.0 / stored`
  - `stored = 'Infinity'` (vulnerable = 0) → correct = `0.0` (in PostgreSQL `1.0 / 'Infinity'::float8 = 0`)
  - `stored = 1.0` → unchanged (total == vulnerable)
  - `stored = 'NaN'` (total = vulnerable = 0) → leave unchanged (or set to `0.0` to match the fixed function's zero-total guard)
- Because correct scores are always in `[0, 1]` and buggy scores are always `>= 1` (vulnerable ≤ total), the predicate `risk_score > 1` identifies exactly the rows needing correction, making the migration **idempotent** and safe against rows written after the fix.
- Alternative (if higher fidelity is preferred): recompute from source SBOM dependency data via `assessments.sbom_id` → `sboms`. The mock context does not expose the dependency/vulnerability tables, so the reciprocal approach is recommended; the implementer should confirm.
- Existing migration convention: Diesel, `migration/YYYY-MM-DD-NNNNNN_description/{up.sql,down.sql}`; latest is `2024-03-10-000003_add_severity_column`, so the next is sequence `000004`.

## Step 6 — Decomposition Guard (evaluated during investigation)

Single root cause (swapped division operands in `compute_risk_score`). The code fix and the data migration both address that one defect (the migration remediates its persisted consequences). The zero-denominator guard is in the same function. **Decomposition guard not triggered** — a single Task is appropriate.
