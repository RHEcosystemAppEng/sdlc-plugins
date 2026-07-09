# Criterion 2: Packages with no vulnerabilities show vulnerability_count: 0

## Verdict: PASS

## Criterion Text

> Packages with no vulnerabilities show `vulnerability_count: 0`

## Analysis

The PR diff for `modules/fundamental/src/package/service/mod.rs` shows that `vulnerability_count` is hardcoded to `0` for all packages:

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

Because the value is hardcoded to 0 for ALL packages, packages with no vulnerabilities will indeed show `vulnerability_count: 0`. This criterion is technically satisfied, although the implementation is incomplete -- the value is 0 for all packages regardless of actual vulnerability count (see Criterion 3 for the failure this causes).

A test also confirms this behavior:

```rust
async fn test_package_without_vulnerabilities_has_zero_count(ctx: &TestContext) {
    let pkg_id = ctx.seed_package("pkg-safe", "MIT").await;
    // ...
    assert_eq!(pkg.vulnerability_count, 0);
}
```

## Evidence

- File: `modules/fundamental/src/package/service/mod.rs` -- `vulnerability_count: 0` hardcoded
- File: `tests/api/package_vuln_count.rs` -- test asserts zero count for safe package

## Conclusion

PASS -- Packages with no vulnerabilities do show `vulnerability_count: 0`. However, this is a trivial consequence of all packages being hardcoded to 0, not a result of correct computation. The underlying implementation gap is captured in Criterion 3.
