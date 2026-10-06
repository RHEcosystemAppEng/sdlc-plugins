# Criterion 2: Packages with no vulnerabilities show `vulnerability_count: 0`

## Criterion Text
Packages with no vulnerabilities show `vulnerability_count: 0`

## Verdict: PASS (trivially)

## Analysis

In `modules/fundamental/src/package/service/mod.rs`, the `vulnerability_count` field is hardcoded to `0`:

```rust
vulnerability_count: 0, // TODO: implement subquery
```

Because the value is hardcoded to `0` for all packages regardless of their actual vulnerability status, packages with no vulnerabilities will indeed show `vulnerability_count: 0`. However, this is a trivial pass -- the criterion is satisfied only because every package returns 0, not because the implementation correctly distinguishes between packages with and without vulnerabilities.

The test `test_package_without_vulnerabilities_has_zero_count` in `tests/api/package_vuln_count.rs` asserts `vulnerability_count == 0` for a package seeded without advisories, which would pass against the current implementation. However, the companion test `test_package_with_vulnerabilities_has_count` would fail, indicating the implementation is incomplete.

This criterion passes on its face, but the underlying implementation is a stub.
