## Criterion 2: Response PURLs do not contain `?` query parameters

**Verdict: PASS**

### Analysis

The second acceptance criterion requires that response PURLs do not contain `?` query parameters (no qualifiers present).

### Evidence from PR Diff

**Service layer** (`modules/fundamental/src/purl/service/mod.rs`):
The `without_qualifiers()` method strips all qualifier key-value pairs from the PURL. Since qualifiers are encoded as query parameters after the `?` character in the PURL string representation, calling `without_qualifiers()` before `to_string()` ensures no `?` appears in the serialized PURL.

Additionally, the qualifier join was removed from the query:
```rust
// Removed:
.join(JoinType::LeftJoin, purl::Relation::PurlQualifier.def());
```

This means qualifier data is no longer fetched from the database at all, providing a second layer of assurance that qualifiers cannot leak into the response.

**Test coverage** (`tests/api/purl_recommend.rs`):
The `test_recommend_purls_basic` test explicitly asserts the absence of `?` in response PURLs:

```rust
assert!(!body.items[0].purl.contains('?'));
assert!(!body.items[1].purl.contains('?'));
```

These assertions directly verify this criterion by checking that no query parameter separator exists in any returned PURL.

**Additional test coverage** (`tests/api/purl_simplify.rs`):
Multiple tests in the new file also assert the absence of qualifiers:
- `test_simplified_purl_no_version`: `assert!(!body.items[0].purl.contains('?'));`
- `test_simplified_purl_mixed_types`: `assert!(!body.items[0].purl.contains("vcs_url"));`
- `test_simplified_purl_ordering_preserved`: `assert!(!body.items[0].purl.contains('?'));` and `assert!(!body.items[1].purl.contains('?'));`

### Conclusion

The code strips qualifiers at the service layer and removes the database join for qualifier data. Multiple tests explicitly assert that response PURLs do not contain `?` or specific qualifier keys. This criterion is satisfied.
