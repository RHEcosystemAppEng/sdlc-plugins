# Criterion 3: Deduplication of entries

**Criterion:** Duplicate entries that were previously distinct due to different qualifiers are deduplicated in the response

**Verdict:** PASS

**Reasoning:**

The diff in `modules/fundamental/src/purl/service/mod.rs` shows a `.dedup_by()` call added to the iterator chain after qualifier stripping:

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

This deduplicates consecutive entries with the same PURL string, which handles the case where two entries that were previously distinct (different qualifiers) now have the same versioned PURL.

The new test `test_recommend_purls_dedup` in `tests/api/purl_recommend.rs` explicitly verifies this:
```rust
// Given PURLs with different qualifiers for the same package version
ctx.seed_purl("pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org&type=jar").await;
ctx.seed_purl("pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo2.maven.org&type=jar").await;

// Then only one entry is returned (deduplicated after qualifier removal)
assert_eq!(body.items.len(), 1);
assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
```

The test seeds two PURLs that differ only in qualifiers (`repo1` vs `repo2`), requests recommendations, and asserts only one result is returned.
