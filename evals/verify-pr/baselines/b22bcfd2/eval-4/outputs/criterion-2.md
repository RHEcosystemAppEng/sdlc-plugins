# Criterion 2: Packages with no vulnerabilities show vulnerability_count: 0

## Verdict: PASS (trivially, due to hardcoded value -- see Criterion 3 for the underlying issue)

## Reasoning

In `modules/fundamental/src/package/service/mod.rs`, the vulnerability_count is hardcoded to `0`:

```rust
vulnerability_count: 0, // TODO: implement subquery
```

This means ALL packages will show `vulnerability_count: 0`, including those with no vulnerabilities. So technically this criterion passes -- packages with no vulnerabilities will indeed show zero. However, this is only true because the value is hardcoded rather than computed. The deeper problem (that packages WITH vulnerabilities will also incorrectly show 0) is captured under Criterion 3.

The test `test_package_without_vulnerabilities_has_zero_count` in `tests/api/package_vuln_count.rs` does assert `vulnerability_count == 0` for a package seeded without advisories, but this test would pass only because the value is hardcoded, not because the logic is correctly implemented.

## Evidence

- File: `modules/fundamental/src/package/service/mod.rs` -- `vulnerability_count: 0, // TODO: implement subquery`
- File: `tests/api/package_vuln_count.rs` -- `test_package_without_vulnerabilities_has_zero_count` asserts `pkg.vulnerability_count == 0`
