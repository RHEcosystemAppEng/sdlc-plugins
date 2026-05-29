## Criterion 3: Duplicate entries that were previously distinct due to different qualifiers are deduplicated in the response

**Result: PASS**

### Evidence

The PR adds deduplication logic in `modules/fundamental/src/purl/service/mod.rs`:

```rust
.dedup_by(|a, b| a.purl == b.purl)
```

This is applied after the `.map()` that strips qualifiers, so PURLs that were previously distinct (due to different qualifier values like `repository_url=https://repo1.maven.org` vs `repository_url=https://repo2.maven.org`) are now collapsed into a single entry because they share the same versioned PURL string after qualifier removal.

The test `test_recommend_purls_dedup` in `tests/api/purl_recommend.rs` explicitly verifies this behavior:

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

This test seeds two PURLs that differ only in their `repository_url` qualifier and asserts that only one entry is returned after deduplication.

### Conclusion

Deduplication is implemented via `.dedup_by()` in the service layer and is verified by the dedicated `test_recommend_purls_dedup` test function.
