# Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Verdict: FAIL

## Reasoning

The task's Implementation Notes specify that the vulnerability count should be computed via a correlated subquery:

```sql
SELECT COUNT(DISTINCT a.id) FROM sbom_package sp
JOIN sbom_advisory sa ON sp.sbom_id = sa.sbom_id
JOIN advisory a ON sa.advisory_id = a.id
WHERE sp.package_id = p.id
```

The `COUNT(DISTINCT a.id)` is specifically designed to ensure unique advisories are counted even when a package appears in multiple SBOMs.

However, the actual implementation in `modules/fundamental/src/package/service/mod.rs` does NOT implement this subquery at all. Instead, it hardcodes the value to 0:

```rust
vulnerability_count: 0, // TODO: implement subquery
```

The `// TODO: implement subquery` comment explicitly acknowledges the subquery has NOT been implemented. Without the subquery, there is no deduplication logic -- there is no counting logic at all. The count does not reflect unique advisories because it does not reflect advisories whatsoever.

The test `test_vulnerability_count_deduplicates_across_sboms` seeds a package with 2 shared advisories across 3 SBOMs and asserts `vulnerability_count == 2`. With the hardcoded value of 0, this test would fail, confirming the implementation does not satisfy this criterion.

## Evidence

- File: `modules/fundamental/src/package/service/mod.rs`, line with `vulnerability_count: 0, // TODO: implement subquery`
- No subquery implementation exists anywhere in the diff
- Test `test_vulnerability_count_deduplicates_across_sboms` expects `vulnerability_count == 2` but would get `0`
- Test `test_package_with_vulnerabilities_has_count` expects `vulnerability_count == 3` but would get `0`
