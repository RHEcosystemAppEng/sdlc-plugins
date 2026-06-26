# Criterion 2: Response PURLs do not contain `?` query parameters (no qualifiers present)

## Verdict: PASS

## Reasoning

This criterion requires that the response PURLs have no query parameters (the `?` character that introduces qualifiers in a PURL string).

1. **Service layer enforcement:** The `without_qualifiers()` method is called on every PURL entity before serialization in `modules/fundamental/src/purl/service/mod.rs`. This method, as documented in the task's Implementation Notes, constructs PURLs without qualifiers, meaning no `?` character will appear in the output string.

2. **Explicit test assertions:** Multiple tests explicitly assert the absence of `?`:
   - `test_recommend_purls_basic`: `assert!(!body.items[0].purl.contains('?'))` and `assert!(!body.items[1].purl.contains('?'))`
   - `test_simplified_purl_no_version`: `assert!(!body.items[0].purl.contains('?'))`
   - `test_simplified_purl_mixed_types`: `assert!(!body.items[0].purl.contains("vcs_url"))` (checks specific qualifier key absence)
   - `test_simplified_purl_ordering_preserved`: `assert!(!body.items[0].purl.contains('?'))` and `assert!(!body.items[1].purl.contains('?'))`

3. **Negative assertions are thorough:** The tests use `contains('?')` which catches ANY qualifier, not just specific ones. This is a comprehensive check rather than asserting against a specific expected string.

4. **Test data includes qualifiers:** The seed data in tests explicitly includes qualifiers (e.g., `?repository_url=https://repo1.maven.org&type=jar`, `?vcs_url=...`, `?type=jar`), proving that the stripping works even when qualifiers are present in the database.

5. **CI passes:** All tests pass, confirming the `?` absence assertions hold at runtime.

The criterion is fully satisfied by both the implementation (service-layer qualifier stripping) and comprehensive test coverage with explicit `?` absence assertions.
