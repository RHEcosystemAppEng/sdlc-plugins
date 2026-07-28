# Criterion 3: Duplicate entries that were previously distinct due to different qualifiers are deduplicated in the response

## Verdict: PASS

## Analysis

This criterion addresses a consequence of qualifier removal: two PURLs that were previously distinct (e.g., same package/version with different `repository_url` qualifiers) would become identical after stripping qualifiers. The response must deduplicate these.

### Evidence from the PR diff

**Service layer (`modules/fundamental/src/purl/service/mod.rs`):**

A `dedup_by` call was added to the collect chain:

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

The `dedup_by(|a, b| a.purl == b.purl)` compares adjacent items by their PURL string. This removes consecutive duplicate entries after qualifier stripping. Note: `dedup_by` only removes *adjacent* duplicates (like Unix `uniq`), which is correct here because the query results are ordered and PURLs with different qualifiers for the same package/version would be adjacent after the qualifier join removal.

**Count query updated:**

The total count query was also updated to use grouping:

```rust
let total = query.clone()
    .select_only()
    .column(purl::Column::Id)
    .group_by(purl::Column::Id)
    .count(&self.db).await?;
```

This ensures the `total` field in the paginated response reflects the deduplicated count, not the raw count including qualifier-based duplicates.

**Dedicated dedup test (`tests/api/purl_recommend.rs`):**

The new `test_recommend_purls_dedup` function directly tests this behavior:

```rust
// Given PURLs with different qualifiers for the same package version
ctx.seed_purl("pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org&type=jar").await;
ctx.seed_purl("pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo2.maven.org&type=jar").await;

// When requesting recommendations (qualifiers stripped, dedup applied)
let resp = ctx.get("/api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3").await;

// Then only one entry is returned (deduplicated after qualifier removal)
assert_eq!(body.items.len(), 1);
assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
```

This test seeds two PURLs that differ only by `repository_url` qualifier, then asserts only one entry is returned after deduplication. This is the exact scenario described in the criterion.

### Conclusion

The criterion is satisfied. The `dedup_by` call in the service layer removes duplicate entries that become identical after qualifier stripping, and the `test_recommend_purls_dedup` test explicitly validates this behavior with the exact scenario (same package/version, different qualifiers yielding one result).
