# Criterion 2: Packages with no vulnerabilities show `vulnerability_count: 0`

## Verdict: PASS

## Analysis

The acceptance criterion requires that packages with no associated vulnerabilities display a `vulnerability_count` of 0.

## Evidence

The PR diff for `modules/fundamental/src/package/service/mod.rs` shows:

```diff
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

The `vulnerability_count` field is hardcoded to `0` for all packages. This means packages with no vulnerabilities will indeed show `vulnerability_count: 0`.

However, it is important to note that this behavior is only coincidentally correct: the value is hardcoded to 0 for ALL packages regardless of their actual vulnerability count. The implementation satisfies this specific criterion (zero-vulnerability packages show 0) but fails to correctly handle the general case (packages WITH vulnerabilities also show 0). This issue is captured in Criterion 3.

The test `test_package_without_vulnerabilities_has_zero_count` in `tests/api/package_vuln_count.rs` also validates this behavior:

```rust
async fn test_package_without_vulnerabilities_has_zero_count(ctx: &TestContext) {
    let pkg_id = ctx.seed_package("pkg-safe", "MIT").await;
    // ...
    assert_eq!(pkg.vulnerability_count, 0);
}
```

This criterion is technically satisfied, though the underlying implementation is incomplete.
