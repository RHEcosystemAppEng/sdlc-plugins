# Criterion 2: Response PURLs do not contain `?` query parameters

**Criterion:** Response PURLs do not contain `?` query parameters (no qualifiers present)

**Verdict:** PASS

## Reasoning

### Code Implementation

The service layer in `modules/fundamental/src/purl/service/mod.rs` calls `p.without_qualifiers()` on every PURL before serialization. This method strips all qualifier key-value pairs, which are the portion of a PURL that appears after the `?` character. Since qualifiers are the only component of a PURL that introduces `?` query parameters, applying `without_qualifiers()` guarantees no `?` appears in the resulting string.

### Test Assertions

The PR adds explicit negative assertions in `test_recommend_purls_basic` to confirm no qualifiers are present:

```rust
assert!(!body.items[0].purl.contains('?'));
assert!(!body.items[1].purl.contains('?'));
```

These assertions directly test the criterion -- they verify the response PURLs contain no `?` character, which means no query parameters (qualifiers) are present.

Additionally, the new test file `tests/api/purl_simplify.rs` includes similar assertions across multiple test scenarios:
- `test_simplified_purl_no_version`: `assert!(!body.items[0].purl.contains('?'));`
- `test_simplified_purl_mixed_types`: `assert!(!body.items[0].purl.contains("vcs_url"));` (checks specific qualifier absence)
- `test_simplified_purl_ordering_preserved`: `assert!(!body.items[0].purl.contains('?'));` and `assert!(!body.items[1].purl.contains('?'));`

### Conclusion

The implementation strips qualifiers at the service layer, and multiple test functions across two test files assert the absence of `?` in response PURLs. This criterion is satisfied.
