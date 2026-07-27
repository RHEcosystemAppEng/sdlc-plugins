# Criterion 2: Packages with no vulnerabilities show vulnerability_count: 0

## Verdict: PASS (with caveat)

## Reasoning

The implementation in `modules/fundamental/src/package/service/mod.rs` hardcodes `vulnerability_count: 0` for all packages:

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

Packages with no vulnerabilities will indeed show `vulnerability_count: 0`. However, this is only coincidentally correct -- the value is hardcoded to 0 for ALL packages, not computed from the database. The mechanism is wrong even though the output happens to satisfy this specific criterion for the zero-vulnerability case.

The companion test `test_package_without_vulnerabilities_has_zero_count` would pass at runtime since the hardcoded value matches the expected zero.

The fundamental implementation flaw (hardcoded value, no subquery) is captured by criterion 3's FAIL verdict. This criterion is narrowly satisfied in its observable behavior.

## Evidence

- File: `modules/fundamental/src/package/service/mod.rs`
- `vulnerability_count: 0` is hardcoded with a `// TODO: implement subquery` comment
- The test `test_package_without_vulnerabilities_has_zero_count` asserts `vulnerability_count == 0`, which would pass
- The criterion is met for the zero-vulnerability case, but only coincidentally
