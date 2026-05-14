# Criterion 1: `GET /api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3` returns versioned PURLs without qualifiers

## Verdict: PASS

## Analysis

The PR modifies the PURL recommendation endpoint to strip qualifiers from returned PURLs. The key change is in `modules/fundamental/src/purl/service/mod.rs`, where the `recommend` method now calls `p.without_qualifiers()` before converting to string:

```rust
.map(|p| {
    let simplified = p.without_qualifiers();
    PurlSummary {
        purl: simplified.to_string(),
    }
})
```

This ensures the response contains versioned PURLs like `pkg:maven/org.apache/commons-lang3@3.12` instead of fully qualified PURLs with query parameters.

The test `test_recommend_purls_basic` in `tests/api/purl_recommend.rs` is updated to assert the simplified format:

```rust
assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
```

Additionally, the endpoint handler in `modules/fundamental/src/purl/endpoints/recommend.rs` removes the `JoinType` import since qualifier joins are no longer needed.

The criterion is satisfied: the endpoint returns versioned PURLs without qualifiers.
