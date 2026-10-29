# Criterion 2: Packages with no vulnerabilities show `vulnerability_count: 0`

## Verdict: PASS (but see Criterion 3 for related concern)

## Analysis

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

The field is hardcoded to `0` for ALL packages. This means packages with no vulnerabilities will indeed show `vulnerability_count: 0`.

However, this is only trivially true — the value is hardcoded to 0 regardless of actual vulnerability count. While the criterion's literal text ("packages with no vulnerabilities show 0") is satisfied by the current implementation, the hardcoded zero is a significant concern addressed in Criterion 3.

## Evidence

- **File:** `modules/fundamental/src/package/service/mod.rs`
- **Line:** `vulnerability_count: 0, // TODO: implement subquery`
- The TODO comment explicitly acknowledges the subquery is not implemented
- Zero is returned for ALL packages, not just those without vulnerabilities
