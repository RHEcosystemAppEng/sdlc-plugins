## Criterion 3: Duplicate entries are deduplicated after qualifier removal

**Criterion:** Duplicate entries that were previously distinct due to different qualifiers are deduplicated in the response

**Verdict:** PASS

### Reasoning

The PR adds a deduplication step in `modules/fundamental/src/purl/service/mod.rs` after qualifier removal:

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

The `.dedup_by(|a, b| a.purl == b.purl)` call removes consecutive duplicate entries based on the PURL string after qualifiers have been stripped. This addresses the scenario where two database entries like `pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org&type=jar` and `pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo2.maven.org&type=jar` would both simplify to `pkg:maven/org.apache/commons-lang3@3.12` and should appear only once in the response.

The qualifier join was also removed from the query (`JoinType::LeftJoin, purl::Relation::PurlQualifier.def()` is deleted), which simplifies the query and aligns with not needing qualifier data in the response.

### Test Coverage

The new `test_recommend_purls_dedup` test in `tests/api/purl_recommend.rs` directly validates deduplication:

```rust
// Given PURLs with different qualifiers for the same package version
ctx.seed_purl("pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org&type=jar").await;
ctx.seed_purl("pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo2.maven.org&type=jar").await;

// Then only one entry is returned (deduplicated after qualifier removal)
assert_eq!(body.items.len(), 1);
assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
```

This seeds two PURLs that differ only in qualifiers and asserts that only one deduplicated entry is returned.
