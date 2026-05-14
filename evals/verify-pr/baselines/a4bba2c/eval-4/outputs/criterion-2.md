# Criterion 2: Packages with no vulnerabilities show `vulnerability_count: 0`

## Verdict: PASS (trivially, due to hardcoding defect)

## Analysis

The PR diff for `modules/fundamental/src/package/service/mod.rs` shows:

```rust
+                vulnerability_count: 0, // TODO: implement subquery
```

The value is hardcoded to `0` for ALL packages, not just those without vulnerabilities. While this means packages with no vulnerabilities will indeed show `vulnerability_count: 0`, this is only coincidentally correct -- the implementation hardcodes zero for every package regardless of actual vulnerability count.

This criterion technically passes in isolation (packages without vulnerabilities do get 0), but the hardcoding approach is the root cause of failure for Criterion 3 (unique advisory counting) since the actual subquery is not implemented. The `// TODO: implement subquery` comment explicitly acknowledges this is incomplete.

## Evidence

- File: `modules/fundamental/src/package/service/mod.rs`
- Line: `vulnerability_count: 0, // TODO: implement subquery`
- The zero value is hardcoded, not computed from database state
- A test exists (`test_package_without_vulnerabilities_has_zero_count`) that would pass with this hardcoded value, but it would also pass for packages WITH vulnerabilities, masking the defect
