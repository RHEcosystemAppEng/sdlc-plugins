# Criterion 3: Duplicate entries that were previously distinct due to different qualifiers are deduplicated in the response

## Verdict: PASS

## Evidence

### Production code

In `modules/fundamental/src/purl/service/mod.rs`, after stripping qualifiers, a deduplication step is applied:

```rust
.dedup_by(|a, b| a.purl == b.purl)
```

This ensures that PURLs which were previously distinct only because of different qualifier values (e.g., `?repository_url=https://repo1.maven.org` vs `?repository_url=https://repo2.maven.org`) are collapsed into a single entry after qualifiers are removed.

### Test evidence

The new `test_recommend_purls_dedup` function in `tests/api/purl_recommend.rs` directly tests this behavior:

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

Two PURLs with different `repository_url` qualifiers but identical namespace/name/version are seeded. After qualifier removal and dedup, only one entry is returned.

### Conclusion

The production code includes an explicit dedup step, and the test verifies the exact scenario described in the criterion -- two previously-distinct entries collapsed to one.
