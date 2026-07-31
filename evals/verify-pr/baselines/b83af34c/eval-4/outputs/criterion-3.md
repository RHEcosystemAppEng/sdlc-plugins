# Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Verdict: FAIL

## Analysis

The acceptance criterion requires that `vulnerability_count` reflects the number of unique advisories affecting each package, computed by joining through `sbom_package`, `sbom_advisory`, and `advisory` tables, with deduplication to avoid double-counting advisories that appear across multiple SBOMs.

### Evidence from PR Diff

In `modules/fundamental/src/package/service/mod.rs`, the implementation hardcodes the vulnerability count to zero:

```rust
+                vulnerability_count: 0, // TODO: implement subquery
```

The `// TODO: implement subquery` comment explicitly acknowledges that the actual computation has not been implemented. The task's implementation notes specify the required correlated subquery:

```sql
SELECT COUNT(DISTINCT a.id) FROM sbom_package sp
JOIN sbom_advisory sa ON sp.sbom_id = sa.sbom_id
JOIN advisory a ON sa.advisory_id = a.id
WHERE sp.package_id = p.id
```

This subquery is entirely absent from the PR. The `vulnerability_count` field always returns `0` regardless of the actual number of advisories, meaning:

1. Packages WITH vulnerabilities will incorrectly show `vulnerability_count: 0`
2. There is no deduplication logic because there is no counting logic at all
3. The `DISTINCT` keyword that would prevent duplicate counting is never used

### Test Implications

The tests in `tests/api/package_vuln_count.rs` assert specific non-zero counts:

- `test_package_with_vulnerabilities_has_count` asserts `vulnerability_count == 3`
- `test_vulnerability_count_deduplicates_across_sboms` asserts `vulnerability_count == 2`

Both of these tests would fail at runtime because the implementation always returns `0`. The fact that CI is reported as passing suggests these tests may not yet be wired into the test suite, or the test database seeding functions are stubs.

### Conclusion

The criterion is definitively not satisfied. The vulnerability count is hardcoded to `0` with a TODO comment indicating the subquery implementation was deferred. No computation of unique advisory counts exists in the diff. FAIL.
