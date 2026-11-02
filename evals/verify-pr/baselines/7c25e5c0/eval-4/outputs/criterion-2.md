# Criterion 2: Packages with no vulnerabilities show vulnerability_count: 0

## Verdict: PASS (trivially, due to hardcoded value)

## Analysis

In `modules/fundamental/src/package/service/mod.rs`, the `vulnerability_count` is hardcoded to `0`:

```rust
+                vulnerability_count: 0, // TODO: implement subquery
```

This means ALL packages return `vulnerability_count: 0`, including those with no vulnerabilities. The criterion is technically satisfied — packages with no vulnerabilities do show zero — but only because every package shows zero regardless of actual vulnerability count. The implementation is incomplete.

## Evidence

- File: `modules/fundamental/src/package/service/mod.rs`, line 32 of the diff
- The hardcoded `0` satisfies the zero-vulnerability case but masks missing functionality
- Test `test_package_without_vulnerabilities_has_zero_count` in tests/api/package_vuln_count.rs asserts `vulnerability_count == 0`, which would pass with the hardcoded value
