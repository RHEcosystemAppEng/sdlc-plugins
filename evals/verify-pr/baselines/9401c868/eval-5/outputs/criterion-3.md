## Criterion 3: Deduplication of entries previously distinct due to different qualifiers

**Criterion**: Duplicate entries that were previously distinct due to different qualifiers are deduplicated in the response

**Verdict**: PASS

### Analysis

The service layer in `modules/fundamental/src/purl/service/mod.rs` adds a deduplication step after qualifier removal:

```rust
.dedup_by(|a, b| a.purl == b.purl)
```

This ensures that PURLs which were previously distinct only because of differing qualifiers (e.g., same package version but different `repository_url` values) are collapsed into a single entry after qualifiers are stripped.

The new test `test_recommend_purls_dedup` in `tests/api/purl_recommend.rs` directly validates this behavior:

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

Two PURLs that differ only in qualifiers are seeded, and the response correctly returns a single deduplicated entry. The criterion is satisfied.

**Note**: The `dedup_by` method only removes consecutive duplicates. This works correctly here because the query results are sorted by the database, so identical versioned PURLs (after qualifier removal) will be adjacent. If the sort order were not guaranteed, a `HashSet`-based approach would be more robust, but given the existing query ordering this is acceptable.
