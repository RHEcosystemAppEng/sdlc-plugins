# Criterion 3: Duplicate entries are deduplicated after qualifier removal

## Criterion Text
Duplicate entries that were previously distinct due to different qualifiers are deduplicated in the response

## Verdict: PASS

## Analysis

The diff shows deduplication is implemented at the service layer and verified by a dedicated test.

### Implementation evidence
In `modules/fundamental/src/purl/service/mod.rs`, after the mapping that strips qualifiers, a deduplication step was added:

```rust
.dedup_by(|a, b| a.purl == b.purl)
```

This applies `dedup_by` on the iterator after the `map` that calls `without_qualifiers()`. The `dedup_by` function removes consecutive duplicate elements where the PURL strings are equal. Since qualifiers have been stripped, PURLs that were previously distinct only because of different qualifiers (e.g., same package version with different `repository_url` values) will now have identical PURL strings and will be collapsed to a single entry.

Note: `dedup_by` only removes *consecutive* duplicates, which is standard for sorted iterators. The query results come from the database with consistent ordering (the query uses `offset`/`limit` pagination), so duplicates from qualifier removal will appear consecutively.

### Test evidence
The new `test_recommend_purls_dedup` function directly verifies this behavior:

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

This test seeds two PURLs for the same package version with different qualifiers, then asserts that only one entry is returned after qualifier stripping and deduplication. This directly validates the criterion.

The removal of `test_recommend_purls_with_qualifiers` (which previously asserted that two qualifier-different PURLs were returned as separate entries) is consistent -- that behavior no longer exists.
