# Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Verdict: FAIL

## Criterion Text

> The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Analysis

The PR diff for `modules/fundamental/src/package/service/mod.rs` shows that `vulnerability_count` is hardcoded to `0` with an explicit TODO comment indicating the subquery has not been implemented:

```rust
+                vulnerability_count: 0, // TODO: implement subquery
```

The task description specifies that the count should be computed via a correlated subquery:

> Use a correlated subquery to count advisories: `SELECT COUNT(DISTINCT a.id) FROM sbom_package sp JOIN sbom_advisory sa ON sp.sbom_id = sa.sbom_id JOIN advisory a ON sa.advisory_id = a.id WHERE sp.package_id = p.id`

This subquery was never implemented. The vulnerability count does NOT reflect unique advisories because it does not reflect ANY advisories -- it is always 0 regardless of the actual data.

The test file includes a test (`test_vulnerability_count_deduplicates_across_sboms`) that would verify deduplication behavior, but this test would fail at runtime because `vulnerability_count` is always 0, while the test expects a count of 2:

```rust
async fn test_vulnerability_count_deduplicates_across_sboms(ctx: &TestContext) {
    let pkg_id = ctx.seed_package_with_shared_advisories("pkg-dedup", 2, 3).await;
    // ...
    assert_eq!(pkg.vulnerability_count, 2);  // Would fail: actual is always 0
}
```

Similarly, the test `test_package_with_vulnerabilities_has_count` expects `vulnerability_count` to be 3 for a package with 3 advisories, which would also fail at runtime:

```rust
assert_eq!(pkg.vulnerability_count, 3);  // Would fail: actual is always 0
```

## Evidence

- File: `modules/fundamental/src/package/service/mod.rs` -- `vulnerability_count: 0, // TODO: implement subquery`
- No correlated subquery joining `sbom_package`, `sbom_advisory`, and `advisory` tables exists anywhere in the diff
- Tests in `tests/api/package_vuln_count.rs` assert non-zero counts that would fail against the hardcoded 0

## Conclusion

FAIL -- The vulnerability count does not reflect unique advisories. It is hardcoded to 0 with a TODO comment, meaning the core computation required by this criterion was never implemented. Two of the three tests in the PR would fail at runtime due to this gap.
