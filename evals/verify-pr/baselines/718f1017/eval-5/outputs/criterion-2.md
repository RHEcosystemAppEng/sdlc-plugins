# Criterion 2: Response PURLs do not contain `?` query parameters

## Verdict: PASS

## Criterion

Response PURLs do not contain `?` query parameters (no qualifiers present).

## Evidence

The PR adds explicit negative assertions in `test_recommend_purls_basic` to verify no query parameters are present:

```rust
assert!(!body.items[0].purl.contains('?'));
assert!(!body.items[1].purl.contains('?'));
```

Additionally, the new `tests/api/purl_simplify.rs` file reinforces this across multiple scenarios:

- `test_simplified_purl_no_version`: `assert!(!body.items[0].purl.contains('?'));`
- `test_simplified_purl_mixed_types`: `assert!(!body.items[0].purl.contains("vcs_url"));`
- `test_simplified_purl_ordering_preserved`: `assert!(!body.items[0].purl.contains('?'));` and `assert!(!body.items[1].purl.contains('?'));`

The implementation achieves this through the `without_qualifiers()` method call in the service layer, which strips all qualifier key-value pairs (and thus the `?` separator) from the PURL string before serialization.
