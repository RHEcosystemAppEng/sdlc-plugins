# Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Verdict: FAIL

## Analysis

This criterion requires that `vulnerability_count` is computed by joining through `sbom_package`, `sbom_advisory`, and `advisory` tables, counting distinct advisories to avoid duplicates across SBOMs.

The implementation in `modules/fundamental/src/package/service/mod.rs` does NOT implement any subquery. Instead, the vulnerability count is hardcoded to 0:

```rust
+            PackageSummary {
+                id: p.id,
+                name: p.name,
+                version: p.version,
+                license: p.license,
+                vulnerability_count: 0, // TODO: implement subquery
+            }
```

The `// TODO: implement subquery` comment explicitly confirms that the required correlated subquery has not been implemented. The task's Implementation Notes specify:

> Use a correlated subquery to count advisories: `SELECT COUNT(DISTINCT a.id) FROM sbom_package sp JOIN sbom_advisory sa ON sp.sbom_id = sa.sbom_id JOIN advisory a ON sa.advisory_id = a.id WHERE sp.package_id = p.id`

This subquery is entirely absent from the implementation. The count does not reflect unique advisories because it does not reflect any advisories at all -- it is a static zero for every package regardless of actual vulnerability data.

The test `test_vulnerability_count_deduplicates_across_sboms` seeds a package with 2 shared advisories across 3 SBOMs and asserts `vulnerability_count == 2`, but the hardcoded implementation would return 0, causing this test to fail. Similarly, `test_package_with_vulnerabilities_has_count` expects `vulnerability_count == 3` but would receive 0.

## Evidence

- File: `modules/fundamental/src/package/service/mod.rs`
- `vulnerability_count: 0` is hardcoded with a `// TODO: implement subquery` comment
- No database query joins through `sbom_package`, `sbom_advisory`, or `advisory` tables
- No `COUNT(DISTINCT ...)` subquery exists in the diff
- Tests asserting non-zero vulnerability counts would fail at runtime against this implementation
