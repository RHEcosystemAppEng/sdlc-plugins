## Criterion 2: Response PURLs do not contain `?` query parameters (no qualifiers present)

**Result: PASS**

### Analysis

The PR ensures that no `?` query parameters appear in response PURLs through two mechanisms:

1. **Service layer change**: In `modules/fundamental/src/purl/service/mod.rs`, the `without_qualifiers()` method is called on each PURL before serialization, which strips all qualifier key-value pairs (everything after `?` in a PURL string).

2. **Test assertions**: Multiple tests explicitly verify the absence of `?`:
   - `test_recommend_purls_basic`: `assert!(!body.items[0].purl.contains('?'))` and `assert!(!body.items[1].purl.contains('?'))`
   - `test_simplified_purl_no_version`: `assert!(!body.items[0].purl.contains('?'))`
   - `test_simplified_purl_mixed_types`: `assert!(!body.items[0].purl.contains("vcs_url"))` (verifies specific qualifier is absent)
   - `test_simplified_purl_ordering_preserved`: `assert!(!body.items[0].purl.contains('?'))` and `assert!(!body.items[1].purl.contains('?'))`

The removal of the `JoinType::LeftJoin` on `PurlQualifier` in the query layer also means qualifier data is no longer fetched from the database for this endpoint, reinforcing that qualifiers cannot leak into the response.
