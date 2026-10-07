# Criterion 1: GET /api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3 returns versioned PURLs without qualifiers

## Verdict: PASS

## Analysis

The PR modifies the PURL recommendation service layer (`modules/fundamental/src/purl/service/mod.rs`) to strip qualifiers from returned PURLs. The key change is in the `.map()` closure that constructs `PurlSummary` items:

**Before (base branch):**
```rust
.map(|p| PurlSummary {
    purl: p.to_string(),
})
```

**After (PR branch):**
```rust
.map(|p| {
    let simplified = p.without_qualifiers();
    PurlSummary {
        purl: simplified.to_string(),
    }
})
```

The `without_qualifiers()` method (documented in the task as available on the `PackageUrl` builder in `common/src/purl.rs`) strips all qualifier key-value pairs, producing a versioned PURL like `pkg:maven/org.apache/commons-lang3@3.12` instead of `pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org&type=jar`.

The endpoint signature in `recommend.rs` is unchanged -- it still serves `GET /api/v2/purl/recommend` with `Query<RecommendParams>` and returns `Json<PaginatedResults<PurlSummary>>`.

**Test verification:** The updated `test_recommend_purls_basic` in `tests/api/purl_recommend.rs` explicitly asserts:
```rust
assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
```
This confirms the response contains a versioned PURL without qualifiers.

This criterion is satisfied by both the code change and corresponding test assertion.
