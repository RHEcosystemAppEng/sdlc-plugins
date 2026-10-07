# Criterion 2: Packages with no vulnerabilities show `vulnerability_count: 0`

## Verdict: PASS

## Analysis

The PR diff for `modules/fundamental/src/package/service/mod.rs` shows that `vulnerability_count` is hardcoded to `0`:

```rust
+                vulnerability_count: 0, // TODO: implement subquery
```

Because the value is hardcoded to `0` for all packages, packages with no vulnerabilities will trivially show `vulnerability_count: 0`. While this satisfies the literal criterion, it does so only because the implementation is incomplete -- the value is always 0 regardless of actual vulnerability data.

The test file `tests/api/package_vuln_count.rs` includes `test_package_without_vulnerabilities_has_zero_count` which asserts `pkg.vulnerability_count == 0`, and this test would pass with the current implementation.

However, it is important to note that this criterion passes only coincidentally due to the hardcoded value. The related test `test_package_with_vulnerabilities_has_count` (which expects `vulnerability_count == 3`) would fail, indicating the implementation is fundamentally incomplete. This broader issue is captured in Criterion 3.

## Evidence

- File: `modules/fundamental/src/package/service/mod.rs` -- `vulnerability_count: 0`
- The hardcoded value satisfies this specific criterion but not the overall feature intent
- Test: `test_package_without_vulnerabilities_has_zero_count` would pass

## Conclusion

Criterion is technically satisfied, though only because of incomplete implementation. The deeper issue is tracked under Criterion 3.
