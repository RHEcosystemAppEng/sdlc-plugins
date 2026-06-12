# Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Verdict: FAIL

## Analysis

The task's Implementation Notes specify a correlated subquery to count advisories:

```sql
SELECT COUNT(DISTINCT a.id) FROM sbom_package sp 
JOIN sbom_advisory sa ON sp.sbom_id = sa.sbom_id 
JOIN advisory a ON sa.advisory_id = a.id 
WHERE sp.package_id = p.id
```

The PR diff shows that no such subquery (or any query) was implemented. Instead, the service hardcodes `vulnerability_count: 0` with an explicit TODO comment:

```rust
vulnerability_count: 0, // TODO: implement subquery
```

This means:
- The count does NOT reflect unique advisories -- it does not reflect anything at all.
- The `COUNT(DISTINCT a.id)` deduplication logic was never implemented.
- The join through `sbom_package -> sbom_advisory -> advisory` tables was never implemented.

A test exists (`test_vulnerability_count_deduplicates_across_sboms`) that seeds a package with 2 unique advisories shared across 3 SBOMs and asserts `vulnerability_count == 2`. This test would FAIL with the current implementation because the hardcoded value is 0, not 2.

## Evidence

- File: `modules/fundamental/src/package/service/mod.rs`
- Line: `vulnerability_count: 0, // TODO: implement subquery`
- No database query or join logic is present in the diff.
- The test `test_vulnerability_count_deduplicates_across_sboms` expects `vulnerability_count == 2` but would receive `0`.
- The test `test_package_with_vulnerabilities_has_count` expects `vulnerability_count == 3` but would receive `0`.
