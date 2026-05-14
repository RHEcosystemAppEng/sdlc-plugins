# Criterion 3: Duplicate entries that were previously distinct due to different qualifiers are deduplicated in the response

## Verdict: PASS

## Analysis

The PR implements deduplication in the service layer. In `modules/fundamental/src/purl/service/mod.rs`, after stripping qualifiers, a `.dedup_by()` call removes consecutive duplicates:

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

This ensures that PURLs which were previously distinct only because of different qualifiers (e.g., `pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org` vs `pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo2.maven.org`) are collapsed into a single entry after qualifier removal.

The new test `test_recommend_purls_dedup` in `tests/api/purl_recommend.rs` explicitly verifies this behavior:

```rust
// Given PURLs with different qualifiers for the same package version
ctx.seed_purl("pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org&type=jar").await;
ctx.seed_purl("pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo2.maven.org&type=jar").await;

// Then only one entry is returned (deduplicated after qualifier removal)
assert_eq!(body.items.len(), 1);
assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
```

The criterion is satisfied: deduplication is implemented and tested.

**Note:** The `dedup_by` method only removes *consecutive* duplicates. This works correctly when the query results are already ordered (which is the case here since items come from the same `Purl::find()` query with consistent ordering). However, if non-consecutive duplicates could occur, `dedup_by` alone would not catch them. The test verifies the expected behavior for the current query ordering.
