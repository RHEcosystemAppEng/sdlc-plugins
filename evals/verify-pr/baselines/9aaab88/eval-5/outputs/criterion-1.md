# Criterion 1: GET /api/v2/purl/recommend returns versioned PURLs without qualifiers

## Verdict: PASS

## Reasoning

The PR modifies `modules/fundamental/src/purl/service/mod.rs` to strip qualifiers from PURLs before including them in the response. Specifically, the mapping logic changes from:

```rust
.map(|p| PurlSummary {
    purl: p.to_string(),
})
```

to:

```rust
.map(|p| {
    let simplified = p.without_qualifiers();
    PurlSummary {
        purl: simplified.to_string(),
    }
})
```

This uses the `without_qualifiers()` method on the `PackageUrl` builder (referenced in the task's Implementation Notes as being available in `common/src/purl.rs`).

The test `test_recommend_purls_basic` in `tests/api/purl_recommend.rs` confirms the behavior change:
- Seeds PURLs with qualifiers (`?repository_url=...&type=jar`)
- Asserts the response contains versioned PURLs without qualifiers: `assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12")`

Additionally, the endpoint handler in `recommend.rs` still routes to the same service method and returns `Result<Json<PaginatedResults<PurlSummary>>, AppError>`, so the endpoint path and response type are unchanged.

The criterion is satisfied: the endpoint returns versioned PURLs (e.g., `pkg:maven/org.apache/commons-lang3@3.12`) without qualifier query parameters.
