# Criterion 2: No query parameters in response PURLs

**Criterion:** Response PURLs do not contain `?` query parameters (no qualifiers present)

**Verdict:** PASS

**Reasoning:**

The service layer applies `without_qualifiers()` to every PURL before including it in the response (see `modules/fundamental/src/purl/service/mod.rs` diff). This method strips all qualifier key-value pairs that would follow the `?` delimiter in a PURL string.

Multiple test assertions explicitly verify the absence of `?`:

In `tests/api/purl_recommend.rs` (`test_recommend_purls_basic`):
```rust
assert!(!body.items[0].purl.contains('?'));
assert!(!body.items[1].purl.contains('?'));
```

In `tests/api/purl_simplify.rs` (`test_simplified_purl_no_version`):
```rust
assert!(!body.items[0].purl.contains('?'));
```

In `tests/api/purl_simplify.rs` (`test_simplified_purl_ordering_preserved`):
```rust
assert!(!body.items[0].purl.contains('?'));
assert!(!body.items[1].purl.contains('?'));
```

The pattern is consistent across all test cases: every response PURL is verified to not contain `?`, confirming qualifiers are absent.
