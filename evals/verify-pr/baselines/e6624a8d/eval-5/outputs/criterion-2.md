## Criterion 2: Response PURLs do not contain ? query parameters

**Criterion:** Response PURLs do not contain `?` query parameters (no qualifiers present)

**Verdict:** PASS

### Reasoning

The `without_qualifiers()` method called in the service layer strips all qualifier key-value pairs from the PURL string. Since qualifiers are appended after a `?` delimiter in the PURL specification, removing qualifiers means the resulting string will never contain a `?` character.

The code change in `modules/fundamental/src/purl/service/mod.rs`:

```rust
let simplified = p.without_qualifiers();
PurlSummary {
    purl: simplified.to_string(),
}
```

This ensures every PURL in the response goes through qualifier removal before serialization.

### Test Coverage

The updated `test_recommend_purls_basic` test includes explicit assertions that no `?` character appears in any response PURL:

```rust
assert!(!body.items[0].purl.contains('?'));
assert!(!body.items[1].purl.contains('?'));
```

Additionally, the new `tests/api/purl_simplify.rs` file includes similar assertions across multiple test scenarios:

- `test_simplified_purl_no_version` asserts `!body.items[0].purl.contains('?')`
- `test_simplified_purl_mixed_types` asserts `!body.items[0].purl.contains("vcs_url")`
- `test_simplified_purl_ordering_preserved` asserts `!body.items[0].purl.contains('?')` and `!body.items[1].purl.contains('?')`

These assertions confirm that no qualifiers leak through in any of the tested scenarios.
