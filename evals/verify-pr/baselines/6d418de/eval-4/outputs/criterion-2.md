# Criterion 2: Packages with no vulnerabilities show vulnerability_count: 0

## Verdict: PASS

## Analysis

The service layer in `modules/fundamental/src/package/service/mod.rs` maps every package to `vulnerability_count: 0`:

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

Since the implementation currently hardcodes `vulnerability_count: 0` for ALL packages, packages with no vulnerabilities will correctly show `vulnerability_count: 0`. This criterion is technically satisfied, though only trivially -- the hardcoded zero means this specific behavior is correct, even though the broader implementation is incomplete.

Additionally, the test `test_package_without_vulnerabilities_has_zero_count` explicitly verifies this behavior by seeding a package with no advisories and asserting `vulnerability_count == 0`, which would pass with the current implementation.

## Evidence

- File: `modules/fundamental/src/package/service/mod.rs`
- Line: `vulnerability_count: 0, // TODO: implement subquery`
- Test: `test_package_without_vulnerabilities_has_zero_count` in `tests/api/package_vuln_count.rs` asserts `assert_eq!(pkg.vulnerability_count, 0);`
- The zero value is correct for packages with no vulnerabilities, regardless of the TODO stub
