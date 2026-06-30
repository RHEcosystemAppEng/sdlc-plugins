## Criterion 3: Duplicate entries that were previously distinct due to different qualifiers are deduplicated in the response

**Result: PASS**

The PR adds a new test function `test_recommend_purls_dedup` in `tests/api/purl_recommend.rs` that explicitly verifies deduplication behavior:
```rust
// Given PURLs with different qualifiers for the same package version
ctx.seed_purl("pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org&type=jar").await;
ctx.seed_purl("pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo2.maven.org&type=jar").await;

// Then only one entry is returned (deduplicated after qualifier removal)
assert_eq!(body.items.len(), 1);
assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
```

This test seeds two PURLs for the same package version `@3.12` that differ only in their `repository_url` qualifier. After qualifier removal, both would produce the identical PURL string `pkg:maven/org.apache/commons-lang3@3.12`. The test asserts that only one entry is returned, confirming deduplication works.

The production code implements this via `.dedup_by(|a, b| a.purl == b.purl)` in the service layer, which removes consecutive duplicates after the `without_qualifiers()` transformation.
