# Criterion 2: Response PURLs do not contain `?` query parameters

## Verdict: PASS

## Reasoning

The acceptance criterion requires that response PURLs do not contain `?` query parameters (no qualifiers present).

### Code Changes

The `without_qualifiers()` method is called on each PURL before serialization in `modules/fundamental/src/purl/service/mod.rs`. This method (part of the `PackageUrl` builder in `common/src/purl.rs`, per the Implementation Notes) constructs a PURL without any qualifier key-value pairs, which means the `?` separator that precedes qualifiers is absent from the output.

### Test Evidence

Multiple tests explicitly assert the absence of `?` in response PURLs:

1. In `test_recommend_purls_basic` (purl_recommend.rs):
   - `assert!(!body.items[0].purl.contains('?'))`
   - `assert!(!body.items[1].purl.contains('?'))`

2. In `test_simplified_purl_no_version` (purl_simplify.rs):
   - `assert!(!body.items[0].purl.contains('?'))`

3. In `test_simplified_purl_mixed_types` (purl_simplify.rs):
   - `assert!(!body.items[0].purl.contains("vcs_url"))` (checks specific qualifier absence)

4. In `test_simplified_purl_ordering_preserved` (purl_simplify.rs):
   - `assert!(!body.items[0].purl.contains('?'))`
   - `assert!(!body.items[1].purl.contains('?'))`

### Conclusion

The `contains('?')` negative assertions across multiple test functions confirm that no qualifier query parameters appear in the response PURLs. Criterion satisfied.
