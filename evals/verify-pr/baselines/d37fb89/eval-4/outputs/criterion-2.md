# Criterion 2: Packages with no vulnerabilities show vulnerability_count: 0

## Verdict: PASS (trivially, due to hardcoding defect)

## Reasoning

The service layer in `modules/fundamental/src/package/service/mod.rs` hardcodes `vulnerability_count: 0` for ALL packages:

```rust
vulnerability_count: 0, // TODO: implement subquery
```

This means packages with no vulnerabilities will indeed show `vulnerability_count: 0`, but only because ALL packages show 0 regardless of their actual vulnerability count. This criterion is trivially satisfied due to the hardcoding, but the implementation is fundamentally broken -- the value is not computed from actual data.

The test `test_package_without_vulnerabilities_has_zero_count` asserts `pkg.vulnerability_count == 0`, which would pass with the hardcoded implementation, but this is coincidental correctness rather than genuine functionality.

## Evidence

- File: `modules/fundamental/src/package/service/mod.rs`
- The `vulnerability_count` is set to literal `0` for every package
- This satisfies the letter of criterion 2 but fails the spirit -- the zero should come from an actual query finding no vulnerabilities, not from a hardcoded default
