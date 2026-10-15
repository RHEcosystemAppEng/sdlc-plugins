# Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Criterion Text
The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Verdict: FAIL

## Analysis

This criterion requires the vulnerability count to be computed via a subquery that counts distinct advisories. The task's implementation notes specify the following subquery:

```sql
SELECT COUNT(DISTINCT a.id)
FROM sbom_package sp
JOIN sbom_advisory sa ON sp.sbom_id = sa.sbom_id
JOIN advisory a ON sa.advisory_id = a.id
WHERE sp.package_id = p.id
```

However, the actual implementation in `modules/fundamental/src/package/service/mod.rs` hardcodes the value:

```rust
vulnerability_count: 0, // TODO: implement subquery
```

The `// TODO: implement subquery` comment explicitly acknowledges that the required subquery has NOT been implemented. The count does not reflect unique advisories -- it reflects nothing, as it is always zero regardless of the actual data.

### Test Impact

Two of the three tests in `tests/api/package_vuln_count.rs` would fail at runtime due to this:

1. `test_package_with_vulnerabilities_has_count` asserts `vulnerability_count == 3` but the hardcoded value is 0.
2. `test_vulnerability_count_deduplicates_across_sboms` asserts `vulnerability_count == 2` but the hardcoded value is 0.

This is a critical implementation gap. The field was added to the model but the core computation logic is missing.
