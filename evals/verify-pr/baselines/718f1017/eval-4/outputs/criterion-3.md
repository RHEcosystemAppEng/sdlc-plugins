# Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

**Status**: FAIL

## Evidence

In `modules/fundamental/src/package/service/mod.rs`, the vulnerability count is hardcoded to zero:

```rust
vulnerability_count: 0, // TODO: implement subquery
```

There is no subquery implementation at all. The task description specifies a correlated subquery using `SELECT COUNT(DISTINCT a.id) FROM sbom_package sp JOIN sbom_advisory sa ON sp.sbom_id = sa.sbom_id JOIN advisory a ON sa.advisory_id = a.id WHERE sp.package_id = p.id`, but this was never implemented. Since no query exists, there is no deduplication logic, and the count cannot reflect unique advisories. The `// TODO: implement subquery` comment explicitly acknowledges this is unfinished work.

The integration test `test_vulnerability_count_deduplicates_across_sboms` seeds a package with 2 unique advisories across 3 SBOMs and asserts `vulnerability_count == 2`, which would fail against the hardcoded zero.
