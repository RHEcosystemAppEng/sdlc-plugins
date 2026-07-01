# Criterion 2: No query parameters in response PURLs

**Criterion:** Response PURLs do not contain `?` query parameters (no qualifiers present)

**Verdict:** PASS

## Reasoning

The `without_qualifiers()` method is called on each PURL before serialization in the service layer, which removes all qualifier key-value pairs from the PURL string representation. Since qualifiers in PURL format appear after a `?` character, removing qualifiers means no `?` will appear in the output string.

Multiple tests explicitly assert this property using negative contains checks:

In `tests/api/purl_recommend.rs`:
```rust
assert!(!body.items[0].purl.contains('?'));
assert!(!body.items[1].purl.contains('?'));
```

In `tests/api/purl_simplify.rs`:
```rust
// test_simplified_purl_no_version
assert!(!body.items[0].purl.contains('?'));

// test_simplified_purl_mixed_types
assert!(!body.items[0].purl.contains("vcs_url"));

// test_simplified_purl_ordering_preserved
assert!(!body.items[0].purl.contains('?'));
assert!(!body.items[1].purl.contains('?'));
```

All CI checks pass, confirming these assertions succeed at runtime.
