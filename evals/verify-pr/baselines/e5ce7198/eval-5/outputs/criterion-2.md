## Criterion 2: Response PURLs do not contain `?` query parameters (no qualifiers present)

**Result: PASS**

The PR adds explicit negative assertions in `test_recommend_purls_basic`:
```rust
assert!(!body.items[0].purl.contains('?'));
assert!(!body.items[1].purl.contains('?'));
```

These assertions verify that no PURL in the response contains the `?` character, which is the delimiter that precedes qualifier key-value pairs in PURL syntax. If any qualifier leaked through, the `?` would be present and these assertions would fail.

The same pattern is repeated in the new `tests/api/purl_simplify.rs` file:
- `test_simplified_purl_no_version`: `assert!(!body.items[0].purl.contains('?'))`
- `test_simplified_purl_mixed_types`: `assert!(!body.items[0].purl.contains("vcs_url"))`
- `test_simplified_purl_ordering_preserved`: `assert!(!body.items[0].purl.contains('?'))` and `assert!(!body.items[1].purl.contains('?'))`

The production implementation achieves this via the `without_qualifiers()` method call in the service layer, which strips all qualifier parameters before constructing the `PurlSummary`.
