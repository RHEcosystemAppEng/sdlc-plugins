# Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Verdict: FAIL

## Reasoning

This criterion requires that `vulnerability_count` be computed by counting unique (distinct) advisories affecting each package, properly deduplicating across multiple SBOMs. The task description specifies the implementation approach:

> Use a correlated subquery to count advisories: `SELECT COUNT(DISTINCT a.id) FROM sbom_package sp JOIN sbom_advisory sa ON sp.sbom_id = sa.sbom_id JOIN advisory a ON sa.advisory_id = a.id WHERE sp.package_id = p.id`

However, the PR diff in `modules/fundamental/src/package/service/mod.rs` shows:

```rust
+            vulnerability_count: 0, // TODO: implement subquery
```

The vulnerability count is **hardcoded to 0** with an explicit `// TODO: implement subquery` comment. The correlated subquery that would join through `sbom_package`, `sbom_advisory`, and `advisory` tables to compute the actual count of unique advisories is **not implemented**.

This means:
- Packages with vulnerabilities will incorrectly show `vulnerability_count: 0`
- The count does NOT reflect unique advisories because no counting occurs at all
- The `COUNT(DISTINCT a.id)` logic specified in the implementation notes is entirely absent

The test `test_vulnerability_count_deduplicates_across_sboms` in the test file asserts `pkg.vulnerability_count == 2`, but the hardcoded value of 0 would cause this test to fail at runtime, further confirming the implementation is incomplete.

Similarly, `test_package_with_vulnerabilities_has_count` asserts `pkg.vulnerability_count == 3`, which would also fail against the hardcoded 0.

## Evidence

- File: `modules/fundamental/src/package/service/mod.rs`
- Line: `vulnerability_count: 0, // TODO: implement subquery`
- The TODO comment explicitly acknowledges the subquery is not implemented
- No join through `sbom_package` / `sbom_advisory` / `advisory` tables exists in the diff
- Two of the three tests would fail at runtime due to asserting non-zero counts against the hardcoded 0
