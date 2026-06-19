# Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Verdict: FAIL

## Reasoning

This criterion requires that `vulnerability_count` accurately reflects the number of unique advisories affecting each package, computed via a correlated subquery joining through `sbom_package`, `sbom_advisory`, and `advisory` tables (as described in the Implementation Notes).

The PR diff in `modules/fundamental/src/package/service/mod.rs` shows:

```rust
+                vulnerability_count: 0, // TODO: implement subquery
```

The `vulnerability_count` is hardcoded to `0` for every package. The TODO comment explicitly acknowledges that the subquery to compute the actual count has not been implemented. This means:

1. Packages WITH vulnerabilities will incorrectly show `vulnerability_count: 0`
2. There is no deduplication logic because there is no counting logic at all
3. The correlated subquery described in the Implementation Notes (`SELECT COUNT(DISTINCT a.id) FROM sbom_package sp JOIN sbom_advisory sa ...`) is entirely absent

The test `test_vulnerability_count_deduplicates_across_sboms` asserts `vulnerability_count == 2` for a package with shared advisories, but with the hardcoded value of 0 this test would fail at runtime.

Similarly, `test_package_with_vulnerabilities_has_count` asserts `vulnerability_count == 3` which would also fail against the hardcoded 0.

This is a fundamental correctness gap: the core feature described in the task summary is not implemented. Only the data model (struct field) is in place; the business logic is missing.
