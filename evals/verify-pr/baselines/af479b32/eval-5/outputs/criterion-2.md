# Criterion 2: Response PURLs do not contain `?` query parameters (no qualifiers present)

## Verdict: PASS

## Reasoning

### Code Change Analysis

The `without_qualifiers()` method is called on every PURL in the response mapping in `modules/fundamental/src/purl/service/mod.rs`. The task description notes that `PackageUrl` builder in `common/src/purl.rs` supports the `without_qualifiers()` method, which strips all query parameters (qualifiers) from the PURL string representation. Since qualifiers are encoded as `?key=value&key=value` in PURL format, the absence of qualifiers means no `?` character will appear in the resulting PURL string.

### Test Verification

Multiple tests explicitly assert the absence of `?` in response PURLs:

**In `tests/api/purl_recommend.rs` (modified):**
```rust
assert!(!body.items[0].purl.contains('?'));
assert!(!body.items[1].purl.contains('?'));
```

These assertions are added to `test_recommend_purls_basic`, directly verifying that the response PURLs contain no query parameter separator.

**In `tests/api/purl_simplify.rs` (new):**
- `test_simplified_purl_no_version`: `assert!(!body.items[0].purl.contains('?'));`
- `test_simplified_purl_mixed_types`: `assert!(!body.items[0].purl.contains("vcs_url"));` (checks for specific qualifier key absence)
- `test_simplified_purl_ordering_preserved`: `assert!(!body.items[0].purl.contains('?'));` and `assert!(!body.items[1].purl.contains('?'));`

### Conclusion

The `without_qualifiers()` call in the service layer eliminates all qualifier parameters, and the tests explicitly assert that no `?` character appears in response PURLs. The criterion is satisfied.
