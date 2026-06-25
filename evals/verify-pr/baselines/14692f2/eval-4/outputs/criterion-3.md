# Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Verdict: FAIL

## Evidence

The task description specifies that the vulnerability count should be computed via a correlated subquery:

> Use a correlated subquery to count advisories: `SELECT COUNT(DISTINCT a.id) FROM sbom_package sp JOIN sbom_advisory sa ON sp.sbom_id = sa.sbom_id JOIN advisory a ON sa.advisory_id = a.id WHERE sp.package_id = p.id`

However, in `modules/fundamental/src/package/service/mod.rs`, the implementation hardcodes the count to 0:

```rust
+                vulnerability_count: 0, // TODO: implement subquery
```

The `// TODO: implement subquery` comment explicitly acknowledges that the actual query has not been implemented. The count does not reflect unique advisories because it does not query any advisories at all -- it always returns 0 regardless of how many advisories exist.

The test `test_vulnerability_count_deduplicates_across_sboms` seeds a package with 2 unique advisories across 3 SBOMs and asserts `pkg.vulnerability_count == 2`. With the hardcoded implementation returning 0, this test would fail at runtime.

Similarly, `test_package_with_vulnerabilities_has_count` seeds a package with 3 advisories and asserts `pkg.vulnerability_count == 3`, which would also fail with the hardcoded 0.

## Conclusion

This criterion FAILS. The vulnerability count is hardcoded to 0 with an explicit TODO comment acknowledging the subquery is not implemented. The count does not reflect unique advisories -- it reflects nothing. Two of the three integration tests would fail at runtime with this implementation.
