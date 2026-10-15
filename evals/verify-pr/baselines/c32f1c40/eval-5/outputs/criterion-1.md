# Criterion 1: GET /api/v2/purl/recommend returns versioned PURLs without qualifiers

## Verdict: PASS

## Reasoning

The acceptance criterion requires that `GET /api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3` returns versioned PURLs without qualifiers.

### Code Changes

In `modules/fundamental/src/purl/service/mod.rs`, the implementation makes two key changes:

1. **Removed the qualifier join:** The line `.join(JoinType::LeftJoin, purl::Relation::PurlQualifier.def())` was removed from the query builder, so qualifier data is no longer fetched from the database.

2. **Added qualifier stripping:** The map closure now calls `p.without_qualifiers()` before converting to string:
   ```rust
   .map(|p| {
       let simplified = p.without_qualifiers();
       PurlSummary {
           purl: simplified.to_string(),
       }
   })
   ```

### Test Evidence

The `test_recommend_purls_basic` test in `tests/api/purl_recommend.rs` verifies this behavior:
- Seeds PURLs with qualifiers (e.g., `pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org&type=jar`)
- Asserts the response contains the versioned form without qualifiers: `assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12")`

The new `tests/api/purl_simplify.rs` file provides additional coverage with tests for no-version PURLs, mixed types, and ordering preservation, all asserting qualifier-free responses.

### Conclusion

The endpoint code strips qualifiers via `without_qualifiers()` and tests confirm the response contains versioned PURLs without qualifier parameters. Criterion satisfied.
