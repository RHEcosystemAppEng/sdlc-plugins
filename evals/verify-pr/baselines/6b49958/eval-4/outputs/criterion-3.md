# Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Verdict: FAIL

## Analysis

The task requires that `vulnerability_count` be computed via a correlated subquery joining through `sbom_package -> sbom_advisory -> advisory` tables, using `COUNT(DISTINCT a.id)` to deduplicate advisories across multiple SBOMs.

The PR diff in `modules/fundamental/src/package/service/mod.rs` shows:

```rust
vulnerability_count: 0, // TODO: implement subquery
```

The vulnerability count is hardcoded to `0` for every package. No subquery is implemented. The `// TODO: implement subquery` comment explicitly acknowledges that this logic is missing. The count does NOT reflect unique advisories because it does not query advisories at all -- it simply returns zero unconditionally.

The test `test_vulnerability_count_deduplicates_across_sboms` in `tests/api/package_vuln_count.rs` seeds a package with 2 unique advisories shared across 3 SBOMs and asserts `vulnerability_count == 2`. This test would FAIL at runtime because the implementation always returns 0, not the expected 2.

Similarly, `test_package_with_vulnerabilities_has_count` seeds a package with 3 advisories and expects `vulnerability_count == 3`, which would also fail since the hardcoded value is 0.

## Evidence

- File: `modules/fundamental/src/package/service/mod.rs`
- Line: `vulnerability_count: 0, // TODO: implement subquery`
- No correlated subquery exists in the diff
- No join through `sbom_package`, `sbom_advisory`, or `advisory` tables
- No `COUNT(DISTINCT ...)` expression anywhere in the diff
- Tests that verify non-zero counts (`test_package_with_vulnerabilities_has_count`, `test_vulnerability_count_deduplicates_across_sboms`) would fail at runtime
- The implementation notes specified: "Use a correlated subquery to count advisories: SELECT COUNT(DISTINCT a.id) FROM sbom_package sp JOIN sbom_advisory sa ON sp.sbom_id = sa.sbom_id JOIN advisory a ON sa.advisory_id = a.id WHERE sp.package_id = p.id" -- this is entirely absent from the implementation
