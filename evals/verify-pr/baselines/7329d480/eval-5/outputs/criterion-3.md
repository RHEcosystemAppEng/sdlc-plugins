# Criterion 3: Deduplication after qualifier removal

**Acceptance Criterion**: Duplicate entries that were previously distinct due to different qualifiers are deduplicated in the response

**Verdict**: PASS

## Evidence

### Product code -- dedup_by in service layer

In `modules/fundamental/src/purl/service/mod.rs`, a deduplication step was added to the iterator chain after qualifier stripping:

```rust
+            .dedup_by(|a, b| a.purl == b.purl)
             .collect();
```

This removes consecutive duplicate entries where the `purl` string is identical. Since qualifiers have been stripped by `without_qualifiers()` in the preceding `.map()`, entries that were previously distinct only due to different qualifiers (e.g., different `repository_url` values) will now have identical `purl` strings and be collapsed into a single entry.

### Test evidence -- dedicated dedup test

In `tests/api/purl_recommend.rs`, the new `test_recommend_purls_dedup` function directly tests this behavior:

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

The test seeds two PURLs with the same type/namespace/name/version but different `repository_url` qualifiers (`repo1` vs `repo2`). After qualifier removal, both map to `pkg:maven/org.apache/commons-lang3@3.12`. The assertion `body.items.len(), 1` confirms deduplication occurred -- the base-branch version of this scenario (in the now-removed `test_recommend_purls_with_qualifiers`) asserted `body.items.len(), 2`.
