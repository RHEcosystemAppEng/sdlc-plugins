# Criterion 2: Packages with no vulnerabilities show vulnerability_count: 0

## Verdict: PASS (trivially, due to hardcoding)

## Reasoning

The service layer in `modules/fundamental/src/package/service/mod.rs` hardcodes `vulnerability_count: 0` for all packages:

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

Because the value is hardcoded to 0 for every package, packages with no vulnerabilities will indeed show `vulnerability_count: 0`. This criterion passes trivially, but the hardcoding means the implementation is incomplete -- the value is always 0 regardless of actual vulnerability count. This is addressed as a FAIL in Criterion 3.

A test exists (`test_package_without_vulnerabilities_has_zero_count`) that asserts `vulnerability_count == 0`, which would pass against the hardcoded implementation. However, the test `test_package_with_vulnerabilities_has_count` expects `vulnerability_count == 3`, which would FAIL against this hardcoded implementation.

## Evidence

- File: `modules/fundamental/src/package/service/mod.rs`
- Line: `vulnerability_count: 0, // TODO: implement subquery`
- The zero case works, but only because ALL values are hardcoded to 0
