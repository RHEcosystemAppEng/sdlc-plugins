# Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Verdict: FAIL

## Reasoning

The implementation in `modules/fundamental/src/package/service/mod.rs` does NOT implement the required subquery to count unique advisories. Instead, `vulnerability_count` is hardcoded to `0` with an explicit TODO comment:

```rust
vulnerability_count: 0, // TODO: implement subquery
```

The task description specifies a correlated subquery to compute the count:

```sql
SELECT COUNT(DISTINCT a.id) FROM sbom_package sp
JOIN sbom_advisory sa ON sp.sbom_id = sa.sbom_id
JOIN advisory a ON sa.advisory_id = a.id
WHERE sp.package_id = p.id
```

This subquery was never implemented. The `vulnerability_count` field always returns 0 regardless of the actual number of advisories affecting a package. This means:

1. The count does NOT reflect unique advisories -- it reflects nothing; it is a hardcoded constant.
2. The `COUNT(DISTINCT ...)` deduplication logic is entirely absent.
3. The tests that verify non-zero counts (`test_package_with_vulnerabilities_has_count` asserts `vulnerability_count == 3` and `test_vulnerability_count_deduplicates_across_sboms` asserts `vulnerability_count == 2`) will FAIL at runtime because the implementation always returns 0.

This is a clear implementation gap -- the core logic of the feature is missing.

## Evidence

- File: `modules/fundamental/src/package/service/mod.rs`, line with `vulnerability_count: 0, // TODO: implement subquery`
- No database join or subquery logic exists in the diff
- The task's Implementation Notes specify a `SELECT COUNT(DISTINCT a.id)` subquery that was not implemented
- Test `test_package_with_vulnerabilities_has_count` expects `vulnerability_count == 3` but will get `0`
- Test `test_vulnerability_count_deduplicates_across_sboms` expects `vulnerability_count == 2` but will get `0`
