## Criterion 1: `GET /api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3` returns versioned PURLs without qualifiers

**Verdict: PASS**

### Reasoning

The PR modifies the service layer in `modules/fundamental/src/purl/service/mod.rs` to strip qualifiers from returned PURLs. The key change is:

```rust
.map(|p| {
    let simplified = p.without_qualifiers();
    PurlSummary {
        purl: simplified.to_string(),
    }
})
```

Previously, the code mapped each result directly with `p.to_string()`, which included qualifiers. Now it calls `p.without_qualifiers()` before serialization, which strips all qualifier parameters from the PURL string.

The test `test_recommend_purls_basic` in `tests/api/purl_recommend.rs` confirms this behavior. The test seeds PURLs with qualifiers (`?repository_url=...&type=jar`) but asserts the response contains only the versioned PURL:

```rust
assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
```

The endpoint signature and route remain unchanged (`GET /api/v2/purl/recommend` with `Query(params): Query<RecommendParams>`), so the endpoint path and query parameter interface are preserved.

This criterion is satisfied by both the implementation change and the test verification.
