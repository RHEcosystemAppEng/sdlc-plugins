# Criterion 10 (Test Requirement): Test that duplicate advisories across SBOMs are not double-counted

**Status**: FAIL

## Evidence

The test `test_vulnerability_count_deduplicates_across_sboms` in `tests/api/package_vuln_count.rs` seeds a package with 2 unique advisories shared across 3 SBOMs and asserts:

```rust
assert_eq!(pkg.vulnerability_count, 2);
```

However, the service implementation in `modules/fundamental/src/package/service/mod.rs` hardcodes:

```rust
vulnerability_count: 0, // TODO: implement subquery
```

This test will fail at runtime because it expects `vulnerability_count == 2` but will receive `0`. The deduplication logic via `COUNT(DISTINCT a.id)` was never implemented.
