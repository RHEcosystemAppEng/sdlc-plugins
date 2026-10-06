# Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Criterion Text
The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Verdict: FAIL

## Analysis

The task's implementation notes specify a correlated subquery to count distinct advisories:

```sql
SELECT COUNT(DISTINCT a.id) FROM sbom_package sp
JOIN sbom_advisory sa ON sp.sbom_id = sa.sbom_id
JOIN advisory a ON sa.advisory_id = a.id
WHERE sp.package_id = p.id
```

However, the actual implementation in `modules/fundamental/src/package/service/mod.rs` does not implement this subquery at all. Instead, the `vulnerability_count` is hardcoded to `0`:

```rust
vulnerability_count: 0, // TODO: implement subquery
```

The `// TODO: implement subquery` comment explicitly acknowledges that the computation is not yet implemented. Because the count is hardcoded to zero, it cannot reflect the unique count of advisories -- it reflects nothing at all.

The test `test_vulnerability_count_deduplicates_across_sboms` in the test file asserts `vulnerability_count == 2` for a package with shared advisories, which would fail against this stub implementation, further confirming the criterion is not met.

This is the core deficiency of the PR: the feature's primary business logic is missing.
