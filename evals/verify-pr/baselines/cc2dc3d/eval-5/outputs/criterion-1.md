# Criterion 1: GET /api/v2/purl/recommend returns versioned PURLs without qualifiers

## Verdict: PASS

## Analysis

The PR modifies the PURL recommendation service in `modules/fundamental/src/purl/service/mod.rs` to strip qualifiers from returned PURLs. The key change is:

```rust
.map(|p| {
    let simplified = p.without_qualifiers();
    PurlSummary {
        purl: simplified.to_string(),
    }
})
```

Previously, PURLs were returned via `p.to_string()` which included all qualifiers. Now the code calls `p.without_qualifiers()` before serialization, which strips the `?key=value` query parameters from the PURL string.

The endpoint handler in `modules/fundamental/src/purl/endpoints/recommend.rs` also removes the `use sea_orm::JoinType;` import since the qualifier join is no longer needed, and the service layer removes the `.join(JoinType::LeftJoin, purl::Relation::PurlQualifier.def())` call.

The test `test_recommend_purls_basic` in `tests/api/purl_recommend.rs` confirms this behavior by seeding PURLs with qualifiers and then asserting that the response contains only versioned PURLs without them:

```rust
assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
```

This demonstrates the endpoint now returns `pkg:maven/org.apache/commons-lang3@3.12` instead of the previous `pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org&type=jar`.

The implementation correctly fulfills this criterion.
