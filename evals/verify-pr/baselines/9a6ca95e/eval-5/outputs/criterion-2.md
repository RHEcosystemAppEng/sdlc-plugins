## Criterion 2: Response PURLs do not contain `?` query parameters (no qualifiers present)

**Verdict: PASS**

### Analysis

The PR adds explicit negative assertions in the modified test `test_recommend_purls_basic` to verify that no qualifier separator character (`?`) appears in the response PURLs:

```rust
assert!(!body.items[0].purl.contains('?'));
assert!(!body.items[1].purl.contains('?'));
```

These assertions confirm that the `?` character, which separates the PURL path from qualifiers, is absent from all returned PURLs. This is a stronger check than just asserting the expected PURL string, because it also guards against any unexpected qualifiers being appended.

The same pattern is used in the new test file `tests/api/purl_simplify.rs`:
- `test_simplified_purl_no_version`: `assert!(!body.items[0].purl.contains('?'))`
- `test_simplified_purl_mixed_types`: `assert!(!body.items[0].purl.contains("vcs_url"))` (checks a specific qualifier key is absent)
- `test_simplified_purl_ordering_preserved`: `assert!(!body.items[0].purl.contains('?'))` and `assert!(!body.items[1].purl.contains('?'))`

The implementation achieves this by calling `p.without_qualifiers()` in the service layer before serializing each PURL, which produces a PURL string that structurally cannot contain `?` qualifier separators.

CI passes, confirming all these assertions hold.
