## Jira API Metadata

```
jira.create_issue(
  project_key  = "ACME",
  issue_type   = "Task",
  summary      = "Fix inverted risk score computation and backfill stale assessments [ACME-520]",
  labels       = ["ai-generated-jira", "reported-by-user", "risk-engine"]
)
```

---

## Repository
acme-backend

## Target Branch
main

## Description

Fix an inverted division in `compute_risk_score()` that causes all risk scores to be
computed as `total_deps / vulnerable_deps` instead of the correct
`vulnerable_deps / total_deps`. Because the wrong value is persisted to the `assessments`
table at ingestion time (and never recomputed on read), a data migration must also
correct all existing assessment records that were created while the bug was active.

Fixes ACME-520.

## Files to Modify

- `modules/risk/src/score.rs` — swap operands in the `compute_risk_score()` division expression
- `modules/risk/tests/score_test.rs` — add a reproducer test with asymmetric inputs; update the existing degenerate test with a comment explaining why it passes regardless of operand order

## Files to Create

- `migration/2026-07-28-000004_fix_risk_score_values/up.sql` — data migration to recompute and overwrite stale `risk_score` values in the `assessments` table
- `migration/2026-07-28-000004_fix_risk_score_values/down.sql` — rollback migration that re-inverts the scores (restores the pre-migration state)

## Implementation Notes

### Code Fix

In `modules/risk/src/score.rs`, the function `compute_risk_score(total_deps, vulnerable_deps)`
currently reads:

```rust
total_deps as f64 / vulnerable_deps as f64
```

Change it to:

```rust
vulnerable_deps as f64 / total_deps as f64
```

No other changes are needed to the function signature or its call sites.

### Reproducer Test

Add to `modules/risk/tests/score_test.rs`:

```rust
#[test]
fn test_risk_score_asymmetric() {
    // BUG ACME-520: operands were swapped, giving 100/5 = 20.0 instead of 5/100 = 0.05
    let score = compute_risk_score(100, 5);
    assert!((score - 0.05).abs() < 1e-9, "expected 0.05, got {}", score);
}
```

This test **fails before the fix** (returns `20.0`) and **passes after the fix** (returns `0.05`).

The existing `test_risk_score_all_vulnerable` test (inputs `10, 10`) will continue to
pass before and after the fix because `10 / 10 == 1.0` regardless of operand order.
Add a comment to that test noting its limitation so future contributors are aware.

### Data Migration

**Why a migration is required:**

`create_assessment()` in `modules/risk/src/assessment.rs` writes the score returned
by `compute_risk_score()` directly to `assessments.risk_score` at ingestion time:

```rust
diesel::insert_into(assessments::table)
    .values(assessments::risk_score.eq(score))
    ...
```

The read endpoint (`get_assessment()` in `modules/risk/src/endpoints.rs`) reads
this persisted value without recomputation. Every row in `assessments` created while
the bug was active stores `total / vulnerable` instead of `vulnerable / total`.

**Migration logic:**

Because the bug is a pure operand swap, the reciprocal of the stored value is the
correct value:

```
correct = 1.0 / stored_wrong_value
```

This is exact — no approximation is introduced. Guard against any rows where
`risk_score = 0` to avoid division by zero.

**`migration/2026-07-28-000004_fix_risk_score_values/up.sql`:**

```sql
-- Correct risk_score values that were stored with inverted numerator/denominator.
-- The bug in compute_risk_score() stored (total_deps / vulnerable_deps) instead of
-- (vulnerable_deps / total_deps). The reciprocal corrects this exactly.
UPDATE assessments
SET risk_score = 1.0 / risk_score
WHERE risk_score != 0;
```

**`migration/2026-07-28-000004_fix_risk_score_values/down.sql`:**

```sql
-- Rollback: re-invert the scores to restore the pre-migration (incorrect) values.
UPDATE assessments
SET risk_score = 1.0 / risk_score
WHERE risk_score != 0;
```

**Migration file naming convention:** follow the Diesel pattern used by existing
migrations in the `migration/` directory:
`YYYY-MM-DD-NNNNNN_description/up.sql` and `/down.sql`. The next sequential number
after `000003` is `000004`.

### Existing Migration Pattern Reference

```
migration/
├── 2024-01-15-000001_create_sboms/
│   ├── up.sql
│   └── down.sql
├── 2024-02-20-000002_create_assessments/
│   ├── up.sql
│   └── down.sql
└── 2024-03-10-000003_add_severity_column/
    ├── up.sql
    └── down.sql
```

## Reuse Candidates

- `modules/risk/src/score.rs::compute_risk_score` — the function being fixed; no other callers need to change
- `modules/risk/tests/score_test.rs::test_risk_score_all_vulnerable` — use as the base pattern for the new reproducer test

## Acceptance Criteria

- [ ] **Reproducer test** `test_risk_score_asymmetric` fails against the unfixed code (returns `20.0` for inputs `total=100, vulnerable=5`) and passes after the fix (returns `0.05`).
- [ ] `compute_risk_score()` returns `vulnerable_deps / total_deps` (e.g., `compute_risk_score(100, 5) == 0.05`).
- [ ] The data migration `migration/2026-07-28-000004_fix_risk_score_values/up.sql` corrects all existing rows in `assessments` where `risk_score != 0`, setting each value to `1.0 / risk_score`.
- [ ] `GET /api/v2/assessments/{id}` returns the corrected `risk_score` for assessments that existed before the fix (after the migration runs).
- [ ] All pre-existing tests in `modules/risk/tests/score_test.rs` continue to pass.
- [ ] No regression in other modules.

## Test Requirements

- [ ] **Reproducer test (front-loaded):** Add `test_risk_score_asymmetric` to `modules/risk/tests/score_test.rs`. Call `compute_risk_score(100, 5)`. Assert the result is within `1e-9` of `0.05`. This test must be authored and verified to fail before the fix is applied.
- [ ] Unit test for the migration logic: verify that the SQL `UPDATE assessments SET risk_score = 1.0 / risk_score WHERE risk_score != 0` on a row with `risk_score = 20.0` produces `risk_score = 0.05`.
- [ ] Confirm `test_risk_score_all_vulnerable` still passes post-fix (non-regression).

## Verification Commands

- `cargo test -p risk -- score` — runs all tests in the score module; `test_risk_score_asymmetric` must pass
- `diesel migration run` — applies `000004_fix_risk_score_values` to the database
- `diesel migration redo` — verifies `up.sql` and `down.sql` are both idempotent

## Bug Context

- **Bug**: [ACME-520](https://mock-jira.example.com/browse/ACME-520)
- **Steps to Reproduce**: (1) Ingest an SBOM with 100 total dependencies, 5 vulnerable. (2) Create a risk assessment. (3) Retrieve via `GET /api/v2/assessments/{id}`. (4) Inspect `risk_score`.
- **Expected Result**: `risk_score = 0.05` (vulnerable / total = 5 / 100).
- **Actual Result**: `risk_score = 20.0` (total / vulnerable = 100 / 5). Numerator and denominator are swapped.
- **Root Cause**: `compute_risk_score()` in `modules/risk/src/score.rs` evaluates `total_deps as f64 / vulnerable_deps as f64` instead of `vulnerable_deps as f64 / total_deps as f64`. The result is persisted to `assessments.risk_score` at creation time by `create_assessment()` in `modules/risk/src/assessment.rs` and is never recomputed on read. All assessment records created before the fix contain inverted scores.
