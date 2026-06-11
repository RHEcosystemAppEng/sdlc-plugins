# Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Verdict: FAIL

## Analysis

This is the core functional requirement of the task, and it is NOT implemented. The implementation in `modules/fundamental/src/package/service/mod.rs` hardcodes `vulnerability_count: 0` with an explicit `// TODO: implement subquery` comment:

```rust
vulnerability_count: 0, // TODO: implement subquery
```

The task's Implementation Notes specify the required subquery:
```sql
SELECT COUNT(DISTINCT a.id) FROM sbom_package sp
JOIN sbom_advisory sa ON sp.sbom_id = sa.sbom_id
JOIN advisory a ON sa.advisory_id = a.id
WHERE sp.package_id = p.id
```

This subquery is entirely absent from the implementation. The `vulnerability_count` does not reflect any advisories at all -- it is always zero regardless of actual advisory data. There is no join to `sbom_package`, `sbom_advisory`, or `advisory` tables. There is no `COUNT(DISTINCT ...)` expression.

The tests in the PR actually verify this criterion:
- `test_package_with_vulnerabilities_has_count` asserts `vulnerability_count == 3` for a package seeded with 3 advisories -- this would FAIL against the hardcoded 0
- `test_vulnerability_count_deduplicates_across_sboms` asserts `vulnerability_count == 2` for a package with shared advisories -- this would also FAIL against the hardcoded 0

The eval scenario states "all CI checks pass," which is contradictory with the implementation since these tests would fail. Regardless of the stated CI status, the code clearly does not implement this criterion.

## Evidence

- File: `modules/fundamental/src/package/service/mod.rs`
- The TODO comment explicitly acknowledges the subquery is not implemented
- No database joins exist in the diff for advisory counting
- Tests asserting non-zero vulnerability counts would fail against the hardcoded value
- The task required a correlated subquery joining sbom_package, sbom_advisory, and advisory tables -- none of this exists
