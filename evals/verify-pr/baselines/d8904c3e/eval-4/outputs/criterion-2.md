# Criterion 2: Packages with no vulnerabilities show `vulnerability_count: 0`

## Verdict: PASS (coincidental)

## Analysis

The implementation in `modules/fundamental/src/package/service/mod.rs` hardcodes `vulnerability_count: 0` for all packages:

```rust
vulnerability_count: 0, // TODO: implement subquery
```

For packages that genuinely have no vulnerabilities, this returns the correct value (0). However, this is satisfied coincidentally by the hardcoded default, not by a correctly implemented subquery that computes the actual count. The value happens to be correct for the zero-vulnerability case because the stub value is 0.

The test `test_package_without_vulnerabilities_has_zero_count` in the new test file asserts `vulnerability_count == 0`, which would pass against the hardcoded implementation.

While technically the criterion is met for the zero-vulnerability case, this is a fragile pass -- the same hardcoded value causes Criterion 3 to fail because packages WITH vulnerabilities also incorrectly show 0.

## Evidence

- File: `modules/fundamental/src/package/service/mod.rs`, line with `vulnerability_count: 0, // TODO: implement subquery`
- The hardcoded 0 is correct for the zero-vulnerability case but is not computed from actual data.
