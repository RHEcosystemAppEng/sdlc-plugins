# Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Verdict: FAIL

## Evidence

In `modules/fundamental/src/package/service/mod.rs`, the vulnerability count is hardcoded to zero:

```rust
+                vulnerability_count: 0, // TODO: implement subquery
```

The task description specifies that the count should be computed via a correlated subquery:

```sql
SELECT COUNT(DISTINCT a.id) FROM sbom_package sp
JOIN sbom_advisory sa ON sp.sbom_id = sa.sbom_id
JOIN advisory a ON sa.advisory_id = a.id
WHERE sp.package_id = p.id
```

This subquery was never implemented. The `COUNT(DISTINCT a.id)` would ensure deduplication across SBOMs, but since no query exists at all, the deduplication requirement is not met.

## Reasoning

The core requirement of this criterion is that the count is computed from real data and properly deduplicated. Since no database query is performed and the value is always 0, the criterion cannot be considered satisfied. The test `test_vulnerability_count_deduplicates_across_sboms` expects a count of 2, but the hardcoded implementation would always return 0, causing the test to fail.

This is a clear FAIL -- the implementation does not perform any counting at all, let alone deduplicated counting.
