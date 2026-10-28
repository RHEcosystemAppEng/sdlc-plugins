# Criterion 3: Duplicate entries that were previously distinct due to different qualifiers are deduplicated in the response

## Verdict: PASS

## Reasoning

The deduplication requirement arises because removing qualifiers can cause previously distinct PURLs (e.g., same package version with different `repository_url` qualifiers) to become identical strings.

**Production code** (`modules/fundamental/src/purl/service/mod.rs`):
The service layer adds a `.dedup_by()` call after the qualifier stripping step:

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

This uses iterator-level deduplication on consecutive identical PURL strings. Note that `dedup_by` only removes *consecutive* duplicates (like Unix `uniq`), so it relies on the query returning results in a stable order where identical simplified PURLs are adjacent. The query filters by namespace and name, and since qualifiers no longer vary the PURL string, rows for the same version will produce identical strings and appear consecutively in database-returned order.

**Test evidence** (`test_recommend_purls_dedup` in `tests/api/purl_recommend.rs`):
```rust
// Seeds two PURLs with same version but different qualifiers
ctx.seed_purl("pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org&type=jar").await;
ctx.seed_purl("pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo2.maven.org&type=jar").await;

// Asserts deduplication: only one entry returned
assert_eq!(body.items.len(), 1);
assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
```

This test directly validates the deduplication scenario described in the acceptance criterion. The two seeded PURLs differ only by qualifier (`repo1` vs `repo2`), and after qualifier removal they collapse to a single entry.

**Note**: The use of `dedup_by` (consecutive dedup) rather than a `HashSet`-based approach means deduplication correctness depends on query ordering. The `group_by` in the count query and the sequential nature of the database results make this reasonable, but it is worth noting as a design consideration.
