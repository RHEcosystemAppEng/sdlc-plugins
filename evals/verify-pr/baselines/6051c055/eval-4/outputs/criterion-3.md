## Criterion 3

**Text:** The count reflects unique advisories only (no duplicates from multiple SBOMs)

**Verdict:** FAIL

**Reasoning:**

In `modules/fundamental/src/package/service/mod.rs`, the `vulnerability_count` is hardcoded to `0` with an explicit TODO comment:

```rust
vulnerability_count: 0, // TODO: implement subquery
```

The subquery to count unique advisories affecting each package has NOT been implemented. The count will always be `0` regardless of how many advisories (unique or duplicate) are associated with a package.

This means:
1. There is no subquery joining packages to advisories
2. There is no deduplication logic (e.g., `COUNT(DISTINCT advisory_id)`)
3. The count does not reflect reality in any way -- it is a static placeholder value

The test `test_package_with_vulnerabilities_has_count` asserts `vulnerability_count == 3` for a package with 3 advisories, and `test_vulnerability_count_deduplicates_across_sboms` asserts `vulnerability_count == 2` for a package with shared advisories. Both of these tests would fail at runtime because the hardcoded value is always 0.

This criterion is definitively NOT satisfied.
