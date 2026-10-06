# Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Verdict: FAIL

## Analysis

The acceptance criterion requires that `vulnerability_count` reflects the number of unique advisories affecting each package, computed via a correlated subquery that deduplicates across multiple SBOMs.

### Expected implementation

Per the Implementation Notes, the count should use:
```sql
SELECT COUNT(DISTINCT a.id)
FROM sbom_package sp
JOIN sbom_advisory sa ON sp.sbom_id = sa.sbom_id
JOIN advisory a ON sa.advisory_id = a.id
WHERE sp.package_id = p.id
```

This subquery would join through `sbom_package -> sbom_advisory -> advisory` tables and use `COUNT(DISTINCT a.id)` to ensure advisories shared across multiple SBOMs are not double-counted.

### Evidence from the diff

In `modules/fundamental/src/package/service/mod.rs`:

```diff
+                vulnerability_count: 0, // TODO: implement subquery
```

The `vulnerability_count` is hardcoded to `0` for every package. The `// TODO: implement subquery` comment explicitly confirms the subquery is not implemented. There is no database query, no join through `sbom_package`/`sbom_advisory`/`advisory` tables, and no deduplication logic.

### Test inconsistency

The test file `tests/api/package_vuln_count.rs` contains tests that expect non-zero counts:

- `test_package_with_vulnerabilities_has_count` seeds a package with 3 advisories and asserts `vulnerability_count == 3`
- `test_vulnerability_count_deduplicates_across_sboms` seeds a package with 2 unique advisories across 3 SBOMs and asserts `vulnerability_count == 2`

Both tests would fail at runtime because the code always returns 0, contradicting the stated "all CI checks pass" claim. This suggests the tests are not actually running or the CI status is inaccurate.

### Conclusion

The criterion is NOT satisfied. The core feature -- computing actual vulnerability counts from the database -- is not implemented. The count is hardcoded to 0 with a TODO comment.
