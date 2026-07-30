# Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Verdict: FAIL

## Analysis

The implementation in `modules/fundamental/src/package/service/mod.rs` hardcodes `vulnerability_count` to 0 for every package:

```rust
vulnerability_count: 0, // TODO: implement subquery
```

The task's Implementation Notes specify a correlated subquery to compute the count:

```sql
SELECT COUNT(DISTINCT a.id) FROM sbom_package sp
JOIN sbom_advisory sa ON sp.sbom_id = sa.sbom_id
JOIN advisory a ON sa.advisory_id = a.id
WHERE sp.package_id = p.id
```

This subquery has not been implemented. The `// TODO: implement subquery` comment in the code explicitly acknowledges this. As a result:

1. The count does NOT reflect unique advisories -- it is always 0 regardless of actual vulnerability data.
2. The deduplication logic (`COUNT(DISTINCT a.id)`) has not been implemented.
3. The test `test_package_with_vulnerabilities_has_count` expects `vulnerability_count == 3` for a package linked to 3 advisories, but the current implementation would return 0, causing this test to fail at runtime.
4. The test `test_vulnerability_count_deduplicates_across_sboms` expects `vulnerability_count == 2` for a package with shared advisories, but would also receive 0.

This is a clear implementation gap -- the core functionality requested by the task is incomplete.

## Evidence

- File: `modules/fundamental/src/package/service/mod.rs`
- Line: `vulnerability_count: 0, // TODO: implement subquery`
- No database join or subquery exists to compute the actual vulnerability count
- The TODO comment confirms the developer acknowledged this was not implemented
- Tests that assert non-zero counts (`test_package_with_vulnerabilities_has_count`, `test_vulnerability_count_deduplicates_across_sboms`) would fail at runtime
