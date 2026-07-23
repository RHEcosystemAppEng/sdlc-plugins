# Criterion 2: Packages with no vulnerabilities show `vulnerability_count: 0`

## Verdict: PASS (trivially, due to hardcoding -- see Criterion 3 for the deeper issue)

## Reasoning

The PR diff for `modules/fundamental/src/package/service/mod.rs` shows:

```rust
+            vulnerability_count: 0, // TODO: implement subquery
```

The value is hardcoded to `0` for all packages. This means that packages with no vulnerabilities will indeed show `vulnerability_count: 0`. However, this is only trivially correct -- the value is `0` for ALL packages, including those that DO have vulnerabilities. The hardcoding means this criterion passes in a narrow, literal sense, but the implementation is incomplete.

The real problem (that the subquery is not implemented) is captured under Criterion 3, which requires the count to reflect actual advisory data. This criterion, strictly evaluated, is satisfied: packages with no vulnerabilities will show 0.

A test exists that verifies this behavior: `test_package_without_vulnerabilities_has_zero_count` in `tests/api/package_vuln_count.rs`. However, this test would pass even with the hardcoded value, masking the incompleteness.

## Evidence

- File: `modules/fundamental/src/package/service/mod.rs`
- Line: `vulnerability_count: 0, // TODO: implement subquery`
- The value is always 0, so packages with no vulnerabilities will correctly show 0
- This is trivially correct due to hardcoding rather than genuine computation
