## Criterion 1: GET /api/v2/purl/recommend returns versioned PURLs without qualifiers

**Criterion:** `GET /api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3` returns versioned PURLs without qualifiers

**Verdict:** PASS

### Reasoning

The PR modifies the PURL recommendation service layer in `modules/fundamental/src/purl/service/mod.rs` to strip qualifiers from returned PURLs. The key change is:

```rust
.map(|p| {
    let simplified = p.without_qualifiers();
    PurlSummary {
        purl: simplified.to_string(),
    }
})
```

Previously, the code mapped each result directly to `PurlSummary { purl: p.to_string() }`, which included qualifiers. The new code calls `p.without_qualifiers()` before converting to string, which produces versioned PURLs like `pkg:maven/org.apache/commons-lang3@3.12` instead of `pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org&type=jar`.

The endpoint handler in `modules/fundamental/src/purl/endpoints/recommend.rs` still returns `Result<Json<PaginatedResults<PurlSummary>>, AppError>`, so the endpoint path and parameters are unchanged -- only the PURL content in the response body is simplified.

### Test Coverage

The updated `test_recommend_purls_basic` test in `tests/api/purl_recommend.rs` explicitly asserts on a versioned PURL without qualifiers:

```rust
assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
```

This confirms the endpoint returns versioned PURLs without qualifiers for the specified base PURL.
