# Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Verdict: FAIL

## Analysis

The acceptance criterion requires that the `vulnerability_count` field reflects the number of unique advisories affecting each package, computed by joining through `sbom_package`, `sbom_advisory`, and `advisory` tables, and that duplicate advisories across multiple SBOMs are not double-counted.

### Evidence from PR Diff

In `modules/fundamental/src/package/service/mod.rs`, the implementation shows:

```rust
vulnerability_count: 0, // TODO: implement subquery
```

The vulnerability count is **hardcoded to zero**. The subquery described in the task's Implementation Notes -- `SELECT COUNT(DISTINCT a.id) FROM sbom_package sp JOIN sbom_advisory sa ON sp.sbom_id = sa.sbom_id JOIN advisory a ON sa.advisory_id = a.id WHERE sp.package_id = p.id` -- is **not implemented**. The `// TODO: implement subquery` comment explicitly acknowledges this.

### Impact

1. **The count does not reflect advisories at all.** It returns 0 for every package, regardless of how many advisories exist. Packages with known vulnerabilities will incorrectly report zero.

2. **Deduplication is moot.** Since no count is computed, the question of whether duplicates are handled is irrelevant -- the feature is unimplemented.

3. **Tests would fail.** The test `test_package_with_vulnerabilities_has_count` expects `vulnerability_count == 3` for a package seeded with 3 advisories. With the hardcoded value of 0, this assertion will fail. Similarly, `test_vulnerability_count_deduplicates_across_sboms` expects `vulnerability_count == 2`, which would also fail.

### Conclusion

This criterion is NOT satisfied. The core functionality of the feature -- computing the vulnerability count from the database -- is entirely missing. The hardcoded zero is a placeholder stub, not a working implementation. This is the most critical gap in the PR.
