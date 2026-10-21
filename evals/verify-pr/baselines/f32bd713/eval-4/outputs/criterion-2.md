# Criterion 2: Packages with no vulnerabilities show vulnerability_count: 0

## Verdict: PASS

## Analysis

The acceptance criterion requires that packages with no known vulnerabilities return `vulnerability_count: 0`.

### Evidence from PR Diff

In `modules/fundamental/src/package/service/mod.rs`, the mapping code sets:

```rust
vulnerability_count: 0, // TODO: implement subquery
```

Because the value is hardcoded to `0`, every package -- including those with no vulnerabilities -- will show `vulnerability_count: 0`. This satisfies the literal requirement for this specific criterion.

However, the hardcoded value is a stub implementation. While packages with no vulnerabilities will correctly show zero, this is only coincidentally correct -- the value is zero for ALL packages regardless of their actual vulnerability status. The broader correctness issue (non-zero counts not working) is captured in Criterion 3.

### Test Coverage

The test `test_package_without_vulnerabilities_has_zero_count` in `tests/api/package_vuln_count.rs` seeds a package with no advisories and asserts `vulnerability_count == 0`. This test would pass with the current hardcoded implementation.

### Conclusion

Packages with no vulnerabilities do show `vulnerability_count: 0`. This specific criterion is technically satisfied, though the implementation is a stub rather than a genuine computation.
