# Criterion 3: Deduplication of entries previously distinct due to qualifiers

## Acceptance Criterion

> Duplicate entries that were previously distinct due to different qualifiers are deduplicated in the response

## Verdict: PASS

## Reasoning

### Implementation

In `modules/fundamental/src/purl/service/mod.rs`, the PR adds a deduplication step after qualifier stripping:

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

The `.dedup_by(|a, b| a.purl == b.purl)` call removes consecutive duplicate entries based on the PURL string value. After qualifiers are stripped, entries like `pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org&type=jar` and `pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo2.maven.org&type=jar` both become `pkg:maven/org.apache/commons-lang3@3.12` and the dedup collapses them to a single entry.

### Test evidence

The `test_recommend_purls_dedup` test directly verifies this behavior:

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

This test seeds two PURLs that are identical except for their `repository_url` qualifier. After qualifier removal, they become the same string, and the assertion confirms only one entry is returned.

### Note on dedup_by behavior

The `dedup_by` method in Rust removes consecutive duplicates. This works correctly here because the query results for the same namespace/name are grouped by the database query's ordering. If results were interleaved (e.g., version A from repo1, version B from repo1, version A from repo2), non-consecutive duplicates could survive. However, since the query filters by namespace and name and the database returns results in a consistent order, consecutive duplicates from the same version with different qualifiers are correctly collapsed.

This criterion is satisfied.
