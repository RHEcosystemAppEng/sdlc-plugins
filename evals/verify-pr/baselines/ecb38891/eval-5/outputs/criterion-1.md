# Criterion 1: GET /api/v2/purl/recommend returns versioned PURLs without qualifiers

## Verdict: PASS

## Reasoning

The PR modifies the PURL recommendation service in `modules/fundamental/src/purl/service/mod.rs` to strip qualifiers from returned PURLs. Specifically:

1. **Qualifier join removed:** The `JoinType::LeftJoin` on `purl::Relation::PurlQualifier` has been removed from the query, so qualifier data is no longer fetched from the database.

2. **PURL simplification added:** The `.map()` closure now calls `p.without_qualifiers()` to produce a simplified PURL before converting to string:
   ```rust
   .map(|p| {
       let simplified = p.without_qualifiers();
       PurlSummary {
           purl: simplified.to_string(),
       }
   })
   ```

3. **Test verification:** The `test_recommend_purls_basic` test in `tests/api/purl_recommend.rs` now asserts that the returned PURL is `"pkg:maven/org.apache/commons-lang3@3.12"` (versioned, no qualifiers), confirming the endpoint returns the expected format.

4. **Additional test coverage:** The new file `tests/api/purl_simplify.rs` includes `test_simplified_purl_no_version` and `test_simplified_purl_mixed_types` which further verify that PURLs are returned without qualifiers across different package types.

The code changes and test assertions confirm that the endpoint now returns versioned PURLs without qualifiers.
