# Criterion 3: Duplicate entries deduplicated after qualifier removal

## Verdict: PASS

## Criterion

Duplicate entries that were previously distinct due to different qualifiers are deduplicated in the response.

## Evidence

The implementation in `modules/fundamental/src/purl/service/mod.rs` adds a `.dedup_by()` call after qualifier removal:

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

This ensures that PURLs which were previously distinct only because of different qualifiers (e.g., same package with `repository_url=repo1` vs `repository_url=repo2`) collapse into a single entry after qualifier stripping.

The new `test_recommend_purls_dedup` test explicitly verifies this behavior:

```rust
// Seeds two PURLs identical except for repository_url qualifier
ctx.seed_purl("pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org&type=jar").await;
ctx.seed_purl("pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo2.maven.org&type=jar").await;

// Asserts only one entry is returned after dedup
assert_eq!(body.items.len(), 1);
assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
```
