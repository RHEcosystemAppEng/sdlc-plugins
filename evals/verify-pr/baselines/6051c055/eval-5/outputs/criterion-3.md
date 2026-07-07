# Criterion 3: Deduplication of entries

## Criterion Text
Duplicate entries that were previously distinct due to different qualifiers are deduplicated in the response

## What was checked
Examined the deduplication implementation in `modules/fundamental/src/purl/service/mod.rs` and the corresponding test `test_recommend_purls_dedup` in `tests/api/purl_recommend.rs`.

## Evidence

The diff adds `.dedup_by(|a, b| a.purl == b.purl)` to the iterator chain in the service:

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

The test `test_recommend_purls_dedup` seeds two PURLs with the same version but different qualifiers:
```rust
ctx.seed_purl("pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org&type=jar").await;
ctx.seed_purl("pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo2.maven.org&type=jar").await;
```

And asserts only one entry is returned:
```rust
assert_eq!(body.items.len(), 1);
assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
```

**Caveat:** `Iterator::dedup_by` only removes *consecutive* duplicates (analogous to Unix `uniq`). If the database returns rows with non-adjacent duplicates (e.g., same-version PURLs interleaved with other versions), those duplicates would not be caught. The query has no explicit `ORDER BY` clause, so row ordering is not guaranteed by the database. In practice, same-version rows are likely adjacent (e.g., inserted sequentially and returned in ID order), and the tests pass with CI green. However, a more robust approach would use `unique_by` from the `itertools` crate or collect into a `HashSet`/`BTreeSet`. This is a latent correctness risk rather than a manifest failure.

## Verdict
PASS -- the deduplication is implemented and CI-tested, though the use of `dedup_by` (consecutive-only) instead of a full deduplication method is a latent risk.
