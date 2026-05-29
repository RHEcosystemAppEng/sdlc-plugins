# Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Result: FAIL

## Analysis

This criterion requires that the vulnerability count correctly counts unique advisories, deduplicating across multiple SBOMs. The task description specifies using `COUNT(DISTINCT a.id)` in a correlated subquery joining through `sbom_package`, `sbom_advisory`, and `advisory` tables.

The diff shows NO subquery implementation whatsoever. The vulnerability_count is hardcoded to 0:

```rust
vulnerability_count: 0, // TODO: implement subquery
```

Since the value is always 0 and never queries the database, it cannot reflect unique advisories or any advisories at all. The deduplication logic is entirely absent.

The test file includes `test_vulnerability_count_deduplicates_across_sboms` which seeds a package with 2 unique advisories across 3 SBOMs and expects `vulnerability_count == 2`. This test would FAIL with the current implementation (it would get 0 instead of 2).

## Evidence

- No `COUNT(DISTINCT ...)` subquery in the diff
- No join to `sbom_package`, `sbom_advisory`, or `advisory` tables
- `vulnerability_count: 0, // TODO: implement subquery` confirms the feature is unimplemented
- Test `test_vulnerability_count_deduplicates_across_sboms` expects 2, would receive 0

## Verdict

FAIL -- the count does not reflect any advisories, unique or otherwise. The deduplication requirement cannot be met when the count is hardcoded to 0.
