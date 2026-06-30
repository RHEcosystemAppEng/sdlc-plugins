# Criterion 8 (Test Requirement): Test package with known vulnerabilities returns correct count

**Status**: FAIL

## Evidence

The test `test_package_with_vulnerabilities_has_count` in `tests/api/package_vuln_count.rs` seeds a package linked to 3 advisories and asserts:

```rust
assert_eq!(pkg.vulnerability_count, 3);
```

However, the service implementation in `modules/fundamental/src/package/service/mod.rs` hardcodes:

```rust
vulnerability_count: 0, // TODO: implement subquery
```

This test will fail at runtime because it expects `vulnerability_count == 3` but will receive `0`. The subquery to compute the actual count was never implemented.
