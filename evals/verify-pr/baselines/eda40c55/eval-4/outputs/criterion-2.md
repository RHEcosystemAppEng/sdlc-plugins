## Criterion 2: Packages with no vulnerabilities show `vulnerability_count: 0`

### Verdict: PASS (with caveat)

### Analysis

The PR diff for `modules/fundamental/src/package/service/mod.rs` shows:

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

The `vulnerability_count` is hardcoded to `0` for all packages. For packages with no vulnerabilities, this produces the correct value of `0`. The test `test_package_without_vulnerabilities_has_zero_count` in `tests/api/package_vuln_count.rs` also asserts `assert_eq!(pkg.vulnerability_count, 0)`, confirming this behavior.

However, this result is only coincidentally correct for the zero-vulnerability case because the value is hardcoded to `0` for ALL packages, not because the code actually queries for vulnerability presence. The `// TODO: implement subquery` comment confirms the implementation is a stub. While the letter of this criterion is met (packages with no vulnerabilities DO show 0), the spirit is undermined by the fact that no actual computation occurs. The deeper issue is captured by Criterion 3.

### Evidence

- **File:** `modules/fundamental/src/package/service/mod.rs`
- **Behavior:** All packages receive `vulnerability_count: 0` regardless of actual vulnerability count
- **Zero-case correctness:** Packages with no vulnerabilities do show `0` (trivially satisfied by the hardcoded value)
- **Test coverage:** `test_package_without_vulnerabilities_has_zero_count` would pass with the hardcoded value

### Conclusion

This criterion is technically satisfied for the zero-vulnerability case, though the underlying implementation is a stub. The real problem is exposed by Criterion 3.
