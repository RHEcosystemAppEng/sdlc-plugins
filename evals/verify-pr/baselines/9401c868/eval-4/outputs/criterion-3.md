## Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

**Result: FAIL**

### Analysis

This criterion requires that the `vulnerability_count` field accurately reflects the number of unique advisories affecting a package, correctly deduplicating advisories that appear across multiple SBOMs.

The implementation in `modules/fundamental/src/package/service/mod.rs` does NOT implement the required subquery:

```rust
+                vulnerability_count: 0, // TODO: implement subquery
```

The value is hardcoded to `0` with an explicit TODO comment acknowledging the subquery is not yet implemented. The task description specifies the required query:

```sql
SELECT COUNT(DISTINCT a.id) FROM sbom_package sp
JOIN sbom_advisory sa ON sp.sbom_id = sa.sbom_id
JOIN advisory a ON sa.advisory_id = a.id
WHERE sp.package_id = p.id
```

This query (or equivalent SeaORM code) is entirely absent from the PR. As a result:

1. The count does not reflect unique advisories -- it reflects nothing (always zero).
2. The deduplication logic (`COUNT(DISTINCT ...)`) is not implemented.
3. The test `test_vulnerability_count_deduplicates_across_sboms` expects `vulnerability_count == 2` but the implementation would return `0`, causing a test failure.
4. The test `test_package_with_vulnerabilities_has_count` expects `vulnerability_count == 3` but the implementation would return `0`, causing a test failure.

This is an incomplete implementation that would fail its own tests at runtime.
