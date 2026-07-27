# Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Verdict: FAIL

## Analysis

The implementation in `modules/fundamental/src/package/service/mod.rs` hardcodes `vulnerability_count` to 0:

```rust
vulnerability_count: 0, // TODO: implement subquery
```

The `TODO` comment explicitly acknowledges that the subquery has not been implemented. The task's Implementation Notes specify a correlated subquery joining through `sbom_package -> sbom_advisory -> advisory` tables with `COUNT(DISTINCT a.id)` to ensure unique advisory counting. None of this logic is present in the code.

Because the value is hardcoded to 0, the count does not reflect actual vulnerability data at all, let alone deduplicated counts. Packages with known vulnerabilities will incorrectly show `vulnerability_count: 0`.

The test `test_vulnerability_count_deduplicates_across_sboms` expects `vulnerability_count == 2` for a package with 2 shared advisories across 3 SBOMs, but the hardcoded implementation would return 0, causing a test failure.

Similarly, `test_package_with_vulnerabilities_has_count` expects `vulnerability_count == 3` but would receive 0.

## Evidence

- File: `modules/fundamental/src/package/service/mod.rs`
- Code: `vulnerability_count: 0, // TODO: implement subquery`
- The TODO comment confirms the subquery is not yet implemented.
- The task specifies: `SELECT COUNT(DISTINCT a.id) FROM sbom_package sp JOIN sbom_advisory sa ON sp.sbom_id = sa.sbom_id JOIN advisory a ON sa.advisory_id = a.id WHERE sp.package_id = p.id`
- This query is completely absent from the implementation.
- Tests that assert non-zero counts would fail against the hardcoded value.
