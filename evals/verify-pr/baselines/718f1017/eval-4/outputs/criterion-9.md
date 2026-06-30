# Criterion 9 (Test Requirement): Test package with no vulnerabilities returns zero

**Status**: PASS (trivially, due to hardcoding)

## Evidence

The test `test_package_without_vulnerabilities_has_zero_count` in `tests/api/package_vuln_count.rs` seeds a package with no advisories and asserts:

```rust
assert_eq!(pkg.vulnerability_count, 0);
```

Since the service hardcodes `vulnerability_count: 0`, this test will pass. However, it passes for the wrong reason -- not because the subquery correctly computes zero, but because the value is always hardcoded to zero regardless of actual data.
