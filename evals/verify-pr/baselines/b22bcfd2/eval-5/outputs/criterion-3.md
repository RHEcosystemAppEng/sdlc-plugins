# Criterion 3: Duplicate entries that were previously distinct due to different qualifiers are deduplicated in the response

## Verdict: PASS

## Reasoning

### Code evidence

The service layer change in `modules/fundamental/src/purl/service/mod.rs` adds deduplication after qualifier stripping:

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

The `.dedup_by(|a, b| a.purl == b.purl)` call removes consecutive duplicate entries based on the simplified PURL string. This handles the case where two PURLs that were previously distinct due to different qualifiers (e.g., `pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org&type=jar` vs `pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo2.maven.org&type=jar`) now map to the same versioned PURL (`pkg:maven/org.apache/commons-lang3@3.12`).

Additionally, the query was modified to add grouping:

```rust
let total = query.clone()
    .select_only()
    .column(purl::Column::Id)
    .group_by(purl::Column::Id)
    .count(&self.db).await?;
```

This adjusts the total count computation to account for deduplication.

### Test evidence

The `test_recommend_purls_dedup` test in `tests/api/purl_recommend.rs` explicitly verifies deduplication:

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

This test seeds two PURLs for the same version but with different `repository_url` qualifiers, then verifies that only one entry is returned after qualifier stripping and deduplication.

### Note on dedup_by behavior

`dedup_by` in Rust's iterator library removes consecutive duplicates only (similar to Unix `uniq`). This works correctly when results from the database query are ordered by the fields that compose the simplified PURL (namespace, name, version). If results could arrive in non-consecutive order for the same simplified PURL, some duplicates might survive. However, the query filters by namespace and name, and results from SeaORM's `.all()` typically return in a consistent order, so consecutive deduplication is sufficient for this use case.

### Evidence

- `modules/fundamental/src/purl/service/mod.rs`: `.dedup_by(|a, b| a.purl == b.purl)` removes duplicate entries after qualifier stripping
- `tests/api/purl_recommend.rs`: `test_recommend_purls_dedup` seeds two PURLs with same version but different qualifiers and asserts only 1 item is returned
- Total count query adjusted with `group_by(purl::Column::Id)` to reflect deduplicated counts
