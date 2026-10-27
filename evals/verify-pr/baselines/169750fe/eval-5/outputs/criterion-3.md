# Criterion 3: Deduplication after qualifier removal

**Criterion:** Duplicate entries that were previously distinct due to different qualifiers are deduplicated in the response

**Result:** PASS

## Analysis

The diff in `modules/fundamental/src/purl/service/mod.rs` adds deduplication logic after qualifier stripping:

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

The `.dedup_by(|a, b| a.purl == b.purl)` call removes consecutive duplicate entries based on the PURL string. Since qualifiers have already been stripped, PURLs that were previously distinct only due to different qualifiers (e.g., same package/version but different `repository_url`) now have identical string representations and are deduplicated.

The test `test_recommend_purls_dedup` in `tests/api/purl_recommend.rs` specifically verifies this behavior:
- Seeds two PURLs with the same package and version but different qualifiers (`repository_url=https://repo1.maven.org` vs `repository_url=https://repo2.maven.org`)
- Asserts only 1 item is returned: `assert_eq!(body.items.len(), 1);`
- Asserts the returned PURL is the versioned form without qualifiers: `assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");`

Note: `.dedup_by()` removes consecutive duplicates, which works correctly here because the query results are ordered before deduplication. For non-consecutive duplicates, a `HashSet`-based approach would be more robust, but the current query ordering ensures consecutive positioning of same-version PURLs.
