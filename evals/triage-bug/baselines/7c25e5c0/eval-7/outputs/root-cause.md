# Root Cause Analysis: ACME-520

## Root Cause

The numerator and denominator are swapped in `compute_risk_score()` in
`modules/risk/src/score.rs`.

The function currently computes:

```
total_deps / vulnerable_deps
```

It should compute:

```
vulnerable_deps / total_deps
```

For an SBOM with 100 total dependencies and 5 vulnerable, the current code produces
`100 / 5 = 20.0` instead of the correct `5 / 100 = 0.05`.

## Why It Went Undetected

The only existing test (`test_risk_score_all_vulnerable`) uses equal values for both
parameters (`total_deps = 10`, `vulnerable_deps = 10`), so `10 / 10 = 1.0` passes
regardless of operand order. No test exercises the asymmetric case.

## Impact

Because the incorrect score is persisted to the `assessments.risk_score` database
column at creation time and is not recomputed on read, all existing assessments in
the database contain inflated risk scores. A code fix alone will only correct future
assessments; a data migration is also required to fix existing records.
