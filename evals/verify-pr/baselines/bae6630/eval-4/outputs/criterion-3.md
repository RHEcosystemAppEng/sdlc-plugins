# Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Result: FAIL

## Evidence

The diff for `modules/fundamental/src/package/service/mod.rs` shows:

```rust
+                vulnerability_count: 0, // TODO: implement subquery
```

The `vulnerability_count` field is hardcoded to `0` for every package. There is no subquery, no database join, no `COUNT(DISTINCT ...)` expression, and no logic whatsoever to compute the actual vulnerability count.

## Reasoning

This criterion requires that the count reflects unique advisories, implying:
1. There must be a query that counts advisories (there is none).
2. The query must deduplicate advisories that appear across multiple SBOMs (there is no query at all).

The implementation notes in the task specify using: `SELECT COUNT(DISTINCT a.id) FROM sbom_package sp JOIN sbom_advisory sa ON sp.sbom_id = sa.sbom_id JOIN advisory a ON sa.advisory_id = a.id WHERE sp.package_id = p.id`

None of this is implemented. The `// TODO: implement subquery` comment explicitly acknowledges that this work has not been done.

The test `test_vulnerability_count_deduplicates_across_sboms` asserts `assert_eq!(pkg.vulnerability_count, 2)` for a package seeded with 2 unique advisories across 3 SBOMs. This test would FAIL at runtime because the hardcoded value of 0 does not equal 2. Similarly, `test_package_with_vulnerabilities_has_count` asserts `vulnerability_count == 3` which would also fail.

This is a clear implementation gap. The core feature — computing actual vulnerability counts — is not implemented.
