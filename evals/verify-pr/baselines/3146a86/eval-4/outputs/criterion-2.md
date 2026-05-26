# Criterion 2: Packages with no vulnerabilities show `vulnerability_count: 0`

## Verdict: PASS (with caveat)

## Analysis

The PR diff for `modules/fundamental/src/package/service/mod.rs` shows the service implementation:

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

The field is hardcoded to `0` for all packages. While this technically means packages with no vulnerabilities will show `vulnerability_count: 0`, it does so only because ALL packages show 0 regardless of actual vulnerability status. The value is correct for zero-vulnerability packages but the implementation is incomplete -- the `// TODO: implement subquery` comment confirms the actual counting logic has not been implemented.

From the test file `tests/api/package_vuln_count.rs`, the test `test_package_without_vulnerabilities_has_zero_count` does verify that a package with no vulnerabilities returns zero:

```rust
async fn test_package_without_vulnerabilities_has_zero_count(ctx: &TestContext) {
    let pkg_id = ctx.seed_package("pkg-safe", "MIT").await;
    ...
    assert_eq!(pkg.vulnerability_count, 0);
}
```

This test would pass with the current implementation since the value is hardcoded to 0. However, this criterion is technically satisfied in isolation -- packages without vulnerabilities do show 0. The deeper issue (that all packages show 0) is captured by Criterion 3.

## Evidence

- File: `modules/fundamental/src/package/service/mod.rs` -- `vulnerability_count: 0` is hardcoded
- File: `tests/api/package_vuln_count.rs` -- test for zero-vulnerability package exists
