# Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Verdict: FAIL

## Analysis

This criterion requires that the `vulnerability_count` field accurately reflects the number of unique advisories affecting each package, with deduplication across SBOMs. The task description specifies using a correlated subquery:

```sql
SELECT COUNT(DISTINCT a.id) FROM sbom_package sp
JOIN sbom_advisory sa ON sp.sbom_id = sa.sbom_id
JOIN advisory a ON sa.advisory_id = a.id
WHERE sp.package_id = p.id
```

However, the actual implementation in `modules/fundamental/src/package/service/mod.rs` is:

```rust
vulnerability_count: 0, // TODO: implement subquery
```

The value is hardcoded to `0` with an explicit TODO comment indicating the subquery has not been implemented. This means:

1. The vulnerability count does not reflect any real data -- it is always 0.
2. No database query is performed to count advisories.
3. There is no deduplication logic because there is no counting logic at all.
4. The tests `test_package_with_vulnerabilities_has_count` (expects 3) and `test_vulnerability_count_deduplicates_across_sboms` (expects 2) would fail at runtime because the hardcoded 0 would not match the expected counts.

This is an incomplete implementation that does not satisfy the acceptance criterion.
