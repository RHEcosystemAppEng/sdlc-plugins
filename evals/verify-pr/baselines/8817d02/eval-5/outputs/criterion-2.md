# Criterion 2: Response PURLs do not contain ? query parameters

**Criterion:** Response PURLs do not contain `?` query parameters (no qualifiers present)

**Verdict:** PASS

## Reasoning

The PR ensures that no `?` character appears in response PURLs through both implementation and test changes:

1. **Implementation (`modules/fundamental/src/purl/service/mod.rs`):** The `without_qualifiers()` method is called on each PURL before serialization. By definition, this method strips all query parameters (everything after `?`) from the PURL string representation. The resulting `simplified.to_string()` will never contain a `?` character.

2. **Test assertions in `test_recommend_purls_basic`:** Two new assertions explicitly verify the absence of `?`:
   ```rust
   assert!(!body.items[0].purl.contains('?'));
   assert!(!body.items[1].purl.contains('?'));
   ```
   These assertions directly validate the criterion.

3. **Test assertions in `tests/api/purl_simplify.rs`:** All three new test functions include `assert!(!body.items[0].purl.contains('?'))` or equivalent checks:
   - `test_simplified_purl_no_version`: `assert!(!body.items[0].purl.contains('?'))`
   - `test_simplified_purl_mixed_types`: `assert!(!body.items[0].purl.contains("vcs_url"))` -- checks that a specific qualifier key is absent
   - `test_simplified_purl_ordering_preserved`: `assert!(!body.items[0].purl.contains('?'))` and `assert!(!body.items[1].purl.contains('?'))`

4. **Qualifier join removed:** The removal of the `JoinType::LeftJoin` on `purl::Relation::PurlQualifier` means qualifier data is never fetched from the database, providing defense in depth -- even if `without_qualifiers()` had a bug, there would be no qualifier data to serialize.

The criterion is satisfied: response PURLs will not contain `?` query parameters.
