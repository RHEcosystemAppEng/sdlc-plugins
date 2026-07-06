## Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

### Verdict: FAIL

### Analysis

This criterion requires that the `vulnerability_count` field accurately reflects the number of unique advisories affecting each package, computed via a correlated subquery joining through `sbom_package -> sbom_advisory -> advisory` tables, using `COUNT(DISTINCT a.id)` to deduplicate across SBOMs.

The PR diff for `modules/fundamental/src/package/service/mod.rs` shows:

```rust
+                vulnerability_count: 0, // TODO: implement subquery
```

The `vulnerability_count` is hardcoded to `0` with an explicit `// TODO: implement subquery` comment. No correlated subquery exists. No join through `sbom_package`, `sbom_advisory`, or `advisory` tables is performed. The count does not reflect any advisories at all -- it is a static zero value regardless of how many vulnerability advisories exist for a given package.

The task's Implementation Notes explicitly specified the required subquery:

> Use a correlated subquery to count advisories: `SELECT COUNT(DISTINCT a.id) FROM sbom_package sp JOIN sbom_advisory sa ON sp.sbom_id = sa.sbom_id JOIN advisory a ON sa.advisory_id = a.id WHERE sp.package_id = p.id`

This subquery was not implemented. The TODO comment confirms the developer acknowledged this work remains undone.

### Test Evidence

Two of the three integration tests would fail with this implementation:

1. `test_package_with_vulnerabilities_has_count` -- asserts `vulnerability_count == 3`, but the hardcoded value returns `0`. This test FAILS.
2. `test_vulnerability_count_deduplicates_across_sboms` -- asserts `vulnerability_count == 2`, but the hardcoded value returns `0`. This test FAILS.

Only `test_package_without_vulnerabilities_has_zero_count` (expects `0`) would pass, and only coincidentally.

### Evidence

- **File:** `modules/fundamental/src/package/service/mod.rs`
- **Line:** `vulnerability_count: 0, // TODO: implement subquery`
- **Missing implementation:** No correlated subquery joining `sbom_package -> sbom_advisory -> advisory`
- **Missing deduplication:** No `COUNT(DISTINCT ...)` logic
- **Test failures:** 2 of 3 tests would fail (`test_package_with_vulnerabilities_has_count` and `test_vulnerability_count_deduplicates_across_sboms`)

### Conclusion

This criterion is NOT satisfied. The vulnerability count is hardcoded to 0 and does not perform any actual computation. This is the primary defect in this PR.
