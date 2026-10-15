# Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Verdict: FAIL

## Analysis

This criterion requires that `vulnerability_count` is computed by counting unique (distinct) advisories affecting each package, avoiding double-counting when the same advisory appears across multiple SBOMs. The task's implementation notes specify the following subquery:

```sql
SELECT COUNT(DISTINCT a.id) FROM sbom_package sp 
JOIN sbom_advisory sa ON sp.sbom_id = sa.sbom_id 
JOIN advisory a ON sa.advisory_id = a.id 
WHERE sp.package_id = p.id
```

However, examining the diff in `modules/fundamental/src/package/service/mod.rs`, the `vulnerability_count` field is hardcoded to `0` with an explicit TODO comment:

```rust
vulnerability_count: 0, // TODO: implement subquery
```

The subquery to compute the actual count of unique advisories was never implemented. The field always returns `0`, regardless of how many advisories (unique or duplicate) exist for the package.

This means:
- A package with 5 unique advisories across 3 SBOMs would incorrectly show `vulnerability_count: 0`
- The deduplication logic (COUNT DISTINCT) was never built
- The test `test_vulnerability_count_deduplicates_across_sboms` expects `vulnerability_count == 2` but would receive `0` at runtime, failing
- The test `test_package_with_vulnerabilities_has_count` expects `vulnerability_count == 3` but would receive `0` at runtime, failing

The implementation is incomplete. The core functional requirement of this feature -- computing the actual vulnerability count -- is missing.

## Evidence

- File: `modules/fundamental/src/package/service/mod.rs`
- Line: `vulnerability_count: 0, // TODO: implement subquery`
- No database subquery, join, or COUNT expression exists in the diff
- Tests expecting non-zero counts (`test_package_with_vulnerabilities_has_count` expects 3, `test_vulnerability_count_deduplicates_across_sboms` expects 2) would fail at runtime
