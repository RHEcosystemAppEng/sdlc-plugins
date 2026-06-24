# Criterion 2: Response PURLs do not contain `?` query parameters

## Acceptance Criterion
Response PURLs do not contain `?` query parameters (no qualifiers present).

## Analysis

### Implementation Changes

The `without_qualifiers()` method is called on each PURL entity before serialization in the service layer (`modules/fundamental/src/purl/service/mod.rs`). This method constructs a PURL string that omits the `?key=value` qualifier suffix. The qualifier join (`JoinType::LeftJoin, purl::Relation::PurlQualifier.def()`) was also removed from the query in the service layer, meaning qualifier data is no longer even fetched from the database.

### Test Coverage

Multiple tests explicitly assert the absence of the `?` character in response PURLs:

1. `test_recommend_purls_basic` (modified):
   - `assert!(!body.items[0].purl.contains('?'))`
   - `assert!(!body.items[1].purl.contains('?'))`

2. `test_simplified_purl_no_version` (new):
   - `assert!(!body.items[0].purl.contains('?'))`

3. `test_simplified_purl_mixed_types` (new):
   - `assert!(!body.items[0].purl.contains("vcs_url"))` -- checks that specific qualifier keys are absent

4. `test_simplified_purl_ordering_preserved` (new):
   - `assert!(!body.items[0].purl.contains('?'))`
   - `assert!(!body.items[1].purl.contains('?'))`

### Verdict

**PASS** -- The implementation removes qualifiers at the service layer, and multiple tests explicitly assert the absence of `?` query parameters in response PURLs.
