## Criterion 1: GET /api/v2/purl/recommend returns versioned PURLs without qualifiers

**Criterion**: `GET /api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3` returns versioned PURLs without qualifiers

**Verdict**: PASS

### Analysis

The diff modifies the service layer in `modules/fundamental/src/purl/service/mod.rs` to strip qualifiers from PURLs before including them in the response. The key change is:

```rust
.map(|p| {
    let simplified = p.without_qualifiers();
    PurlSummary {
        purl: simplified.to_string(),
    }
})
```

Previously, the code returned `p.to_string()` which included the full PURL with qualifiers. Now it calls `p.without_qualifiers()` first, producing versioned PURLs like `pkg:maven/org.apache/commons-lang3@3.12` instead of `pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org&type=jar`.

The endpoint handler in `recommend.rs` still calls `PurlService::recommend()` with the same signature and returns `Json<PaginatedResults<PurlSummary>>`, so the change is confined to the service layer's serialization logic.

The test `test_recommend_purls_basic` in `tests/api/purl_recommend.rs` was updated to assert the new format:
```rust
assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
```

This directly validates the criterion.
