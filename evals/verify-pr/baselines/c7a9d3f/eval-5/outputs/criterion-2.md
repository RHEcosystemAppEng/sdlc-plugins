# Criterion 2: Response PURLs do not contain `?` query parameters (no qualifiers present)

## Verdict: PASS

## Reasoning

The PR implements qualifier removal through the `without_qualifiers()` method in the service layer. This method constructs a new PURL representation that excludes the query string portion (everything after `?` in a PURL).

The tests explicitly verify the absence of `?` characters in response PURLs using negative assertions:

In `tests/api/purl_recommend.rs`, `test_recommend_purls_basic`:
```rust
assert!(!body.items[0].purl.contains('?'));
assert!(!body.items[1].purl.contains('?'));
```

In `tests/api/purl_simplify.rs`, `test_simplified_purl_no_version`:
```rust
assert!(!body.items[0].purl.contains('?'));
```

In `tests/api/purl_simplify.rs`, `test_simplified_purl_mixed_types`:
```rust
assert!(!body.items[0].purl.contains("vcs_url"));
```

In `tests/api/purl_simplify.rs`, `test_simplified_purl_ordering_preserved`:
```rust
assert!(!body.items[0].purl.contains('?'));
assert!(!body.items[1].purl.contains('?'));
```

These assertions collectively confirm that across all test scenarios (basic, dedup, no-version, mixed-types, ordering), response PURLs never contain `?` query parameters.

The implementation is sound: by calling `without_qualifiers()` on every PURL before serialization, any qualifier information is stripped at the service layer before the response is constructed.

## Evidence

- `modules/fundamental/src/purl/service/mod.rs`: `p.without_qualifiers()` strips all qualifier data
- Multiple test files assert `!purl.contains('?')` across different scenarios
- The `without_qualifiers()` method is the single point of qualifier removal, applied to every item in the response
