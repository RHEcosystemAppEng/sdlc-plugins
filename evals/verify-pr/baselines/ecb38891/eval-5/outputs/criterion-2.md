# Criterion 2: Response PURLs do not contain ? query parameters (no qualifiers present)

## Verdict: PASS

## Reasoning

The PR ensures that response PURLs contain no qualifier query parameters by:

1. **Service layer change:** In `modules/fundamental/src/purl/service/mod.rs`, the `without_qualifiers()` method is called on each PURL before serialization. This method strips all qualifier key-value pairs, which are represented as `?key=value` in the PURL string format.

2. **Explicit test assertions:** Multiple tests now assert the absence of `?` in returned PURLs:
   - `test_recommend_purls_basic` includes:
     ```rust
     assert!(!body.items[0].purl.contains('?'));
     assert!(!body.items[1].purl.contains('?'));
     ```
   - `test_simplified_purl_no_version` includes:
     ```rust
     assert!(!body.items[0].purl.contains('?'));
     ```
   - `test_simplified_purl_mixed_types` includes:
     ```rust
     assert!(!body.items[0].purl.contains("vcs_url"));
     ```
   - `test_simplified_purl_ordering_preserved` includes:
     ```rust
     assert!(!body.items[0].purl.contains('?'));
     assert!(!body.items[1].purl.contains('?'));
     ```

3. **Qualifier join removal:** The `JoinType::LeftJoin` on `PurlQualifier` was removed from the database query, and the `use sea_orm::JoinType;` import was removed from `recommend.rs`, confirming qualifiers are no longer fetched.

The combination of the service-layer stripping and explicit `contains('?')` assertions in tests confirms this criterion is satisfied.
