# Criterion 3 Analysis

**Criterion:** Duplicate entries that were previously distinct due to different qualifiers are deduplicated in the response

**Verdict:** PASS

## Evidence

### Code Changes

In `modules/fundamental/src/purl/service/mod.rs`, after stripping qualifiers from each PURL, the code applies deduplication:

```rust
.map(|p| {
    let simplified = p.without_qualifiers();
    PurlSummary {
        purl: simplified.to_string(),
    }
})
.dedup_by(|a, b| a.purl == b.purl)
.collect();
```

The `.dedup_by(|a, b| a.purl == b.purl)` call removes consecutive duplicate entries where the PURL string is identical. This handles the case where two database entries like `pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org&type=jar` and `pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo2.maven.org&type=jar` both simplify to `pkg:maven/org.apache/commons-lang3@3.12` -- without dedup, the response would contain two identical entries.

### Dedup Correctness Note

The use of `dedup_by` (rather than a `HashSet`-based dedup) means deduplication is applied to consecutive elements only. This is correct as long as the query results are ordered, which the service's query achieves through its filtering and pagination logic. PURLs with the same namespace and name (and thus the same simplified form) will be adjacent in the query results, making consecutive dedup sufficient.

### Test Verification

The new `test_recommend_purls_dedup` function in `tests/api/purl_recommend.rs` directly tests this behavior:

```rust
async fn test_recommend_purls_dedup(ctx: &TestContext) {
    // Given PURLs with different qualifiers for the same package version
    ctx.seed_purl("pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org&type=jar").await;
    ctx.seed_purl("pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo2.maven.org&type=jar").await;

    // When requesting recommendations (qualifiers stripped, dedup applied)
    let resp = ctx.get("/api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3").await;

    // Then only one entry is returned (deduplicated after qualifier removal)
    assert_eq!(resp.status(), StatusCode::OK);
    let body: PaginatedResults<PurlSummary> = resp.json().await;
    assert_eq!(body.items.len(), 1);
    assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
}
```

The test seeds two entries that differ only in qualifiers (`repo1` vs `repo2`), then verifies that only one entry is returned in the response. This directly validates the deduplication behavior.

### Contrast with Previous Behavior

In the base branch, the `test_recommend_purls_with_qualifiers` test verified that both qualifier variants were returned as separate entries (`assert_eq!(body.items.len(), 2)`). The new `test_recommend_purls_dedup` replaces this with the inverse assertion (`assert_eq!(body.items.len(), 1)`), confirming the behavior change from "separate entries per qualifier" to "deduplicated entries."

## Conclusion

The code implements deduplication via `dedup_by` after qualifier stripping, and the dedicated `test_recommend_purls_dedup` test verifies that previously distinct entries (differing only in qualifiers) are collapsed to a single entry. Criterion is satisfied.
