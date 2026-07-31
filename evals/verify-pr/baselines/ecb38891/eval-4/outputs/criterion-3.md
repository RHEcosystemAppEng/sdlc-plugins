# Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Verdict: FAIL

## Reasoning

This criterion requires that `vulnerability_count` correctly computes the number of unique vulnerability advisories affecting each package by joining through the `sbom_package`, `sbom_advisory`, and `advisory` tables, as specified in the task's Implementation Notes.

The PR diff in `modules/fundamental/src/package/service/mod.rs` reveals that the vulnerability count is **hardcoded to 0** with an explicit TODO comment:

```rust
+        let items = items.into_iter().map(|p| {
+            PackageSummary {
+                id: p.id,
+                name: p.name,
+                version: p.version,
+                license: p.license,
+                vulnerability_count: 0, // TODO: implement subquery
+            }
+        }).collect();
```

The required correlated subquery (`SELECT COUNT(DISTINCT a.id) FROM sbom_package sp JOIN sbom_advisory sa ON sp.sbom_id = sa.sbom_id JOIN advisory a ON sa.advisory_id = a.id WHERE sp.package_id = p.id`) was never implemented. The `// TODO: implement subquery` comment explicitly acknowledges this omission.

As a result:
- Packages with actual vulnerabilities will incorrectly show `vulnerability_count: 0`
- There is no deduplication logic because there is no counting logic at all
- The tests `test_package_with_vulnerabilities_has_count` (expects 3) and `test_vulnerability_count_deduplicates_across_sboms` (expects 2) would fail at runtime since the code always returns 0

This is a critical functional gap — the core feature described by the task (computing vulnerability counts) is not implemented.

## Evidence

- File: `modules/fundamental/src/package/service/mod.rs`
- Code: `vulnerability_count: 0, // TODO: implement subquery`
- No subquery, no join through sbom_package/sbom_advisory/advisory tables
- No use of `COUNT(DISTINCT ...)` or any aggregation
- Tests assert non-zero values (3 and 2) that the hardcoded implementation cannot produce
