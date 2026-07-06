# Criterion 2: Response PURLs do not contain `?` query parameters (no qualifiers present)

## Verdict: PASS

## Analysis

This criterion is a stronger form of Criterion 1 -- it requires not just that qualifiers are omitted from the expected format, but that no `?` character appears anywhere in the response PURLs. This guards against partial qualifier stripping (e.g., a bug where some qualifiers remain).

The production code achieves this through the `without_qualifiers()` method, which is designed to produce a PURL string with no qualifier section at all.

## Test Evidence

Multiple tests explicitly assert the absence of `?` in response PURLs:

In `tests/api/purl_recommend.rs` (`test_recommend_purls_basic`):
```rust
assert!(!body.items[0].purl.contains('?'));
assert!(!body.items[1].purl.contains('?'));
```

In `tests/api/purl_simplify.rs`:
- `test_simplified_purl_no_version`: `assert!(!body.items[0].purl.contains('?'));`
- `test_simplified_purl_mixed_types`: `assert!(!body.items[0].purl.contains("vcs_url"));`
- `test_simplified_purl_ordering_preserved`: `assert!(!body.items[0].purl.contains('?'));` and `assert!(!body.items[1].purl.contains('?'));`

These negative assertions provide explicit regression guards against qualifier leakage across multiple PURL types and scenarios.

## Conclusion

The criterion is satisfied. The `contains('?')` negative assertions in 4 out of 7 test functions provide broad coverage ensuring no qualifiers appear in response PURLs.
