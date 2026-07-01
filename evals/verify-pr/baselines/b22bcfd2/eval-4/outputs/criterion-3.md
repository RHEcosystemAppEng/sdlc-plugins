# Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Verdict: FAIL

## Reasoning

The task's implementation notes specify a correlated subquery to count advisories:

```sql
SELECT COUNT(DISTINCT a.id) FROM sbom_package sp
JOIN sbom_advisory sa ON sp.sbom_id = sa.sbom_id
JOIN advisory a ON sa.advisory_id = a.id
WHERE sp.package_id = p.id
```

However, the actual implementation in `modules/fundamental/src/package/service/mod.rs` hardcodes the vulnerability_count to 0:

```rust
vulnerability_count: 0, // TODO: implement subquery
```

The `// TODO: implement subquery` comment explicitly acknowledges that the subquery has not been implemented. This means:

1. The count does NOT reflect unique advisories -- it reflects nothing at all; it is always 0.
2. The deduplication logic (`COUNT(DISTINCT a.id)`) is not implemented.
3. Packages with known vulnerabilities will incorrectly report 0 vulnerabilities.

The test `test_vulnerability_count_deduplicates_across_sboms` seeds a package with 2 shared advisories across 3 SBOMs and expects `vulnerability_count == 2`, but this test would FAIL at runtime because the hardcoded value is 0, not 2.

Similarly, `test_package_with_vulnerabilities_has_count` expects `vulnerability_count == 3` for a package with 3 advisories, which would also fail because the value is always 0.

This is a critical correctness failure -- the core feature (counting vulnerabilities) is not implemented.

## Evidence

- File: `modules/fundamental/src/package/service/mod.rs` -- `vulnerability_count: 0, // TODO: implement subquery`
- The subquery described in Implementation Notes is completely absent from the diff
- Tests `test_package_with_vulnerabilities_has_count` and `test_vulnerability_count_deduplicates_across_sboms` would fail at runtime
