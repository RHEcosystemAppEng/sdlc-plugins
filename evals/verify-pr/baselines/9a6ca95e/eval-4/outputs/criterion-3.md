# Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Result: FAIL

## Evidence

The task description specifies that the vulnerability count should be computed via a correlated subquery:

```sql
SELECT COUNT(DISTINCT a.id) FROM sbom_package sp
JOIN sbom_advisory sa ON sp.sbom_id = sa.sbom_id
JOIN advisory a ON sa.advisory_id = a.id
WHERE sp.package_id = p.id
```

However, the actual implementation in `modules/fundamental/src/package/service/mod.rs` is:

```rust
vulnerability_count: 0, // TODO: implement subquery
```

The vulnerability count is hardcoded to `0` with an explicit `// TODO: implement subquery` comment. No subquery is implemented. No join through `sbom_package`, `sbom_advisory`, or `advisory` tables is performed. There is no `COUNT(DISTINCT ...)` or any deduplication logic whatsoever.

The test `test_vulnerability_count_deduplicates_across_sboms` expects a count of 2 for a package with shared advisories across 3 SBOMs, but the implementation would return 0, causing the test to fail at runtime.

## Conclusion

This criterion is definitively not met. The core feature -- computing a unique advisory count via database query -- is entirely unimplemented. The hardcoded zero is a placeholder stub.
