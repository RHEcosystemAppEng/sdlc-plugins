# Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Verdict: FAIL

## Analysis

This criterion requires that the `vulnerability_count` field accurately reflects the number of unique advisories affecting each package, computed via a database query that joins through `sbom_package -> sbom_advisory -> advisory` tables with deduplication (as specified in the Implementation Notes with `COUNT(DISTINCT a.id)`).

The PR diff for `modules/fundamental/src/package/service/mod.rs` shows:

```rust
+                vulnerability_count: 0, // TODO: implement subquery
```

The vulnerability count is **hardcoded to 0** for all packages. The required correlated subquery specified in the Implementation Notes (`SELECT COUNT(DISTINCT a.id) FROM sbom_package sp JOIN sbom_advisory sa ON sp.sbom_id = sa.sbom_id JOIN advisory a ON sa.advisory_id = a.id WHERE sp.package_id = p.id`) has NOT been implemented.

The `// TODO: implement subquery` comment explicitly confirms this is an incomplete placeholder. No deduplication logic exists because no counting logic exists at all.

The test `test_vulnerability_count_deduplicates_across_sboms` seeds a package with shared advisories across SBOMs and asserts `vulnerability_count == 2`, but since the implementation always returns 0, this test would FAIL at runtime.

Similarly, `test_package_with_vulnerabilities_has_count` asserts `vulnerability_count == 3` for a package with 3 advisories, which would also FAIL at runtime because the hardcoded value is 0.

## Evidence

- File: `modules/fundamental/src/package/service/mod.rs`
- Line: `vulnerability_count: 0, // TODO: implement subquery`
- No database query exists to count advisories
- No `COUNT(DISTINCT ...)` logic implemented
- The TODO comment explicitly acknowledges the implementation is incomplete
- Tests `test_package_with_vulnerabilities_has_count` and `test_vulnerability_count_deduplicates_across_sboms` would fail at runtime due to hardcoded zero
