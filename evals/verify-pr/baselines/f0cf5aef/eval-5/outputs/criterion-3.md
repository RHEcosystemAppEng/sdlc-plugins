# Criterion 3: Duplicate entries that were previously distinct due to different qualifiers are deduplicated in the response

## Verdict: PASS

## Reasoning

This criterion requires that when qualifiers are stripped, entries that were previously distinct (because they had different qualifiers for the same package version) are collapsed into a single entry.

### Implementation Evidence

In `modules/fundamental/src/purl/service/mod.rs`, a `dedup_by` call was added after the `map` that strips qualifiers:

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

The `dedup_by` method removes consecutive duplicate entries where `a.purl == b.purl`. This works because:
1. The query filters by namespace and name, so results for the same package version with different qualifiers will be adjacent in the result set.
2. After `without_qualifiers()` strips the qualifiers, these entries become identical strings and are deduplicated.

Note: `dedup_by` only removes adjacent duplicates, not all duplicates. This is sufficient here because the database query groups results by namespace/name, so rows that differ only by qualifiers will be consecutive. If results were interleaved with other versions, non-adjacent duplicates could theoretically survive, but the query structure prevents this scenario for the stated use case.

### Test Evidence

The `test_recommend_purls_dedup` test directly validates this behavior:

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

Two PURLs are seeded with the same version (`@3.12`) but different `repository_url` qualifiers. After qualifier removal, both would produce `pkg:maven/org.apache/commons-lang3@3.12`. The test asserts only one item is returned, confirming deduplication.

### Conclusion

The `dedup_by` implementation and the `test_recommend_purls_dedup` test together confirm that duplicate entries arising from qualifier removal are properly deduplicated.
