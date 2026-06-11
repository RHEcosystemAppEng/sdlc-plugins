# Criterion 3: Duplicate entries that were previously distinct due to different qualifiers are deduplicated

## Verdict: PASS

## Analysis

The PR adds deduplication logic in `modules/fundamental/src/purl/service/mod.rs` after qualifier stripping:

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

The `.dedup_by(|a, b| a.purl == b.purl)` call removes consecutive duplicate entries after qualifiers are stripped. This handles the case where two PURLs that were previously distinct (e.g., same package version with different `repository_url` qualifiers) become identical once qualifiers are removed.

The new `test_recommend_purls_dedup` test in `tests/api/purl_recommend.rs` directly verifies this behavior:

```rust
// Given PURLs with different qualifiers for the same package version
ctx.seed_purl("pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org&type=jar").await;
ctx.seed_purl("pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo2.maven.org&type=jar").await;

// Then only one entry is returned (deduplicated after qualifier removal)
assert_eq!(body.items.len(), 1);
assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
```

Note: The `dedup_by` method only removes consecutive duplicates. This works correctly here because the query orders results by the same columns, so identical PURLs (after qualifier removal) will be adjacent. If results were not sorted, non-adjacent duplicates could survive. However, since the existing query ordering groups by package name and version, this approach is sufficient.

The criterion is met.
