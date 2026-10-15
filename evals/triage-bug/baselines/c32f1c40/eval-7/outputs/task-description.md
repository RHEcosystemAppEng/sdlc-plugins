<!-- Jira API Metadata Block -->
<!-- jira.create_issue parameters: -->
<!-- project: ACME -->
<!-- issue_type: Task -->
<!-- labels: ["ai-generated-jira"] -->

```
jira.create_issue(
  project_key: "ACME",
  issue_type: "Task",
  summary: "Fix swapped division in compute_risk_score() and migrate stale assessments",
  labels: ["ai-generated-jira"],
  description: <see below>
)
```

---

## Repository
acme-backend

## Target Branch
main

## Description
Fix the reversed division operands in `compute_risk_score()` which produces inflated
risk scores (divides `total_deps / vulnerable_deps` instead of
`vulnerable_deps / total_deps`). Because the incorrect score is persisted to the
`assessments` table at ingestion time and never recomputed on read, a data migration
is also required to correct all existing assessment records. Fixes ACME-520.

## Files to Modify
- `modules/risk/src/score.rs` -- swap division operands in `compute_risk_score()` to `vulnerable_deps as f64 / total_deps as f64`
- `modules/risk/tests/score_test.rs` -- add reproducer test exercising `total_deps != vulnerable_deps`

## Files to Create
- `migration/2024-04-01-000004_fix_risk_score_values/up.sql` -- data migration to correct existing `risk_score` values in the `assessments` table
- `migration/2024-04-01-000004_fix_risk_score_values/down.sql` -- reversibility migration (restore original values if needed)

## Implementation Notes

### Code fix

In `modules/risk/src/score.rs`, the `compute_risk_score()` function has the division
operands reversed:

```rust
// Current (buggy):
pub fn compute_risk_score(total_deps: u32, vulnerable_deps: u32) -> f64 {
    total_deps as f64 / vulnerable_deps as f64
}

// Correct:
pub fn compute_risk_score(total_deps: u32, vulnerable_deps: u32) -> f64 {
    vulnerable_deps as f64 / total_deps as f64
}
```

Swap `total_deps` and `vulnerable_deps` in the division expression. Consider adding
a guard for `total_deps == 0` to avoid division by zero (return `0.0`).

### Reproducer test

In `modules/risk/tests/score_test.rs`, add a test that exercises the case where
`total_deps != vulnerable_deps`. The existing test `test_risk_score_all_vulnerable`
uses `(10, 10)` which equals `1.0` regardless of operand order and does not catch
the bug.

Reproducer test guidance derived from Steps to Reproduce:

- **Input**: `compute_risk_score(100, 5)` (100 total deps, 5 vulnerable)
- **Before fix (Actual Result)**: returns `20.0` (100 / 5)
- **After fix (Expected Result)**: returns `0.05` (5 / 100)
- **Assertion**: `assert!((compute_risk_score(100, 5) - 0.05).abs() < f64::EPSILON)`

Additional test cases to consider:
- `compute_risk_score(200, 1)` should return `0.005`
- `compute_risk_score(50, 50)` should return `1.0` (regression check)
- `compute_risk_score(10, 0)` should return `0.0` (edge case: no vulnerable deps)

### Data migration

The migration corrects existing `risk_score` values in the `assessments` table.
Follow the existing Diesel migration convention observed in the `migration/` directory
(e.g., `2024-03-10-000003_add_severity_column/up.sql`).

**Migration logic for `up.sql`:**

Since the buggy formula computed `total_deps / vulnerable_deps` instead of
`vulnerable_deps / total_deps`, the stored value is the reciprocal of the correct
value. The migration can invert existing scores:

```sql
UPDATE assessments
SET risk_score = CASE
    WHEN risk_score != 0 THEN 1.0 / risk_score
    ELSE 0
END;
```

**Important caveat**: The reciprocal inversion (`1 / old_score`) is mathematically
correct only if the original computation was strictly `total / vulnerable` with no
additional transformations. Verify this holds for all records. If any assessments
were created with `vulnerable_deps = 0` (which would cause division by zero in the
original code), those records may need special handling.

An alternative approach (more robust but slower) is to join the `assessments` table
with the source SBOM data and recompute the score from the original `total_deps` and
`vulnerable_deps` values:

```sql
UPDATE assessments a
SET risk_score = s.vulnerable_deps::double precision / s.total_deps::double precision
FROM sboms s
WHERE a.sbom_id = s.id
  AND s.total_deps > 0;
```

**Migration logic for `down.sql`:**

```sql
UPDATE assessments
SET risk_score = CASE
    WHEN risk_score != 0 THEN 1.0 / risk_score
    ELSE 0
END;
```

The down migration inverts again to restore the original (incorrect) values, since the
reciprocal operation is its own inverse.

## Acceptance Criteria
- [ ] Reproducer test: a test calling `compute_risk_score(100, 5)` asserts the result is `0.05` (fails before fix, passes after)
- [ ] `compute_risk_score()` returns `vulnerable_deps / total_deps` instead of `total_deps / vulnerable_deps`
- [ ] Existing assessment records with incorrect `risk_score` values are corrected by the data migration
- [ ] Existing test `test_risk_score_all_vulnerable` continues to pass (no regression)
- [ ] No regression in other existing tests

## Test Requirements
- [ ] Reproducer test: call `compute_risk_score(100, 5)` and assert the result equals `0.05` (within floating-point tolerance). This test must fail on the current code and pass after the fix.
- [ ] Additional edge case tests: `compute_risk_score(200, 1)` returns `0.005`; `compute_risk_score(50, 50)` returns `1.0`
- [ ] Division-by-zero guard: verify `compute_risk_score(0, 0)` and `compute_risk_score(N, 0)` handle zero inputs gracefully
- [ ] Verify existing test `test_risk_score_all_vulnerable` still passes

## Bug Context

- **Bug**: [ACME-520](https://mock-jira.example.com/browse/ACME-520)
- **Steps to Reproduce**: Ingest an SBOM with 100 total dependencies (5 vulnerable), create a risk assessment, retrieve it via `GET /api/v2/assessments/{id}`, and inspect the `risk_score` field.
- **Expected Result**: Risk score should be `5 / 100 = 0.05` (vulnerable / total).
- **Actual Result**: Risk score is `100 / 5 = 20.0` (total / vulnerable). Numerator and denominator are swapped.
- **Root Cause**: `compute_risk_score()` in `modules/risk/src/score.rs` divides `total_deps / vulnerable_deps` instead of `vulnerable_deps / total_deps`. The incorrect score is persisted to `assessments.risk_score` at ingestion time and never recomputed on read, so all existing records contain inflated values.
