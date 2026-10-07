# Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Verdict: FAIL

## Analysis

The task description specifies that the `vulnerability_count` should be computed using a correlated subquery:

```sql
SELECT COUNT(DISTINCT a.id) FROM sbom_package sp
JOIN sbom_advisory sa ON sp.sbom_id = sa.sbom_id
JOIN advisory a ON sa.advisory_id = a.id
WHERE sp.package_id = p.id
```

However, the PR diff for `modules/fundamental/src/package/service/mod.rs` shows that `vulnerability_count` is hardcoded to `0` with a TODO comment indicating the subquery has NOT been implemented:

```rust
+                vulnerability_count: 0, // TODO: implement subquery
```

This is a clear implementation gap. The count does not reflect unique advisories because it does not reflect anything at all -- it is a static value. The `TODO` comment explicitly acknowledges the missing implementation.

The test file includes `test_vulnerability_count_deduplicates_across_sboms` which asserts that a package with 2 unique advisories across 3 SBOMs returns `vulnerability_count: 2`. With the hardcoded `0`, this test would fail at runtime.

Similarly, `test_package_with_vulnerabilities_has_count` seeds a package with 3 advisories and asserts `vulnerability_count == 3`. This test would also fail with the hardcoded value of `0`.

## Evidence

- File: `modules/fundamental/src/package/service/mod.rs`, line: `vulnerability_count: 0, // TODO: implement subquery`
- No correlated subquery is present anywhere in the diff
- No join through `sbom_package`, `sbom_advisory`, `advisory` tables exists
- Two tests would fail at runtime: `test_package_with_vulnerabilities_has_count` (expects 3, gets 0) and `test_vulnerability_count_deduplicates_across_sboms` (expects 2, gets 0)

## Conclusion

This criterion is NOT satisfied. The vulnerability count subquery has not been implemented. The field always returns 0 regardless of actual vulnerability data.
