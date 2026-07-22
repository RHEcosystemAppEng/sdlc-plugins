# Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Criterion Text

> The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Verdict: FAIL

## Reasoning

This criterion requires that `vulnerability_count` be computed by counting unique (distinct) advisories linked to each package through the `sbom_package` -> `sbom_advisory` -> `advisory` join chain. The task's Implementation Notes specify the exact subquery:

```sql
SELECT COUNT(DISTINCT a.id) FROM sbom_package sp
JOIN sbom_advisory sa ON sp.sbom_id = sa.sbom_id
JOIN advisory a ON sa.advisory_id = a.id
WHERE sp.package_id = p.id
```

However, the PR diff in `modules/fundamental/src/package/service/mod.rs` shows that no such subquery was implemented. Instead, the vulnerability count is hardcoded to zero:

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

The `// TODO: implement subquery` comment explicitly acknowledges that the implementation is incomplete. The count does not reflect unique advisories -- it does not reflect advisories at all. It is a static zero value for every package regardless of actual vulnerability data.

Furthermore, the test that is supposed to verify this behavior (`test_vulnerability_count_deduplicates_across_sboms`) would fail at runtime:

```rust
async fn test_vulnerability_count_deduplicates_across_sboms(ctx: &TestContext) {
    let pkg_id = ctx.seed_package_with_shared_advisories("pkg-dedup", 2, 3).await;
    // ...
    assert_eq!(pkg.vulnerability_count, 2); // Would get 0, not 2
}
```

Similarly, `test_package_with_vulnerabilities_has_count` would also fail:

```rust
assert_eq!(pkg.vulnerability_count, 3); // Would get 0, not 3
```

These test failures confirm that the core computation logic is missing.

## Evidence

- **File:** `modules/fundamental/src/package/service/mod.rs`
- **Code:** `vulnerability_count: 0, // TODO: implement subquery`
- **Missing:** No database subquery joining `sbom_package`, `sbom_advisory`, and `advisory` tables
- **Missing:** No `COUNT(DISTINCT ...)` computation
- **Test impact:** `test_package_with_vulnerabilities_has_count` and `test_vulnerability_count_deduplicates_across_sboms` would fail at runtime (asserting 3 and 2 respectively against hardcoded 0)
