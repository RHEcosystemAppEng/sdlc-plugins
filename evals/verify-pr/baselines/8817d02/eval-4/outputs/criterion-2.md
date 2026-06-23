# Criterion 2: Packages with no vulnerabilities show `vulnerability_count: 0`

## Verdict: PASS (vacuously, due to hardcoded value)

## Reasoning

The implementation in `modules/fundamental/src/package/service/mod.rs` hardcodes `vulnerability_count: 0` for all packages:

```rust
vulnerability_count: 0, // TODO: implement subquery
```

Because the value is hardcoded to 0 for every package, packages with no vulnerabilities will indeed show `vulnerability_count: 0`. However, this is a trivially satisfied condition -- it passes only because *all* packages return 0, not because the system correctly distinguishes between packages with and without vulnerabilities.

This criterion technically passes in isolation, but the hardcoded value is the root cause of Criterion 3's failure. The implementation does not compute the actual vulnerability count; it simply returns 0 unconditionally.

## Evidence

- **File:** `modules/fundamental/src/package/service/mod.rs`, diff line 31
- The `TODO: implement subquery` comment confirms the actual counting logic was not implemented.
- The test `test_package_without_vulnerabilities_has_zero_count` in `tests/api/package_vuln_count.rs` asserts `vulnerability_count == 0`, which would pass given the hardcoded value.
