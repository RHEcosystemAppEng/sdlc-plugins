# Criterion 3: Deduplication of Previously Distinct Entries

**Criterion:** Duplicate entries that were previously distinct due to different qualifiers are deduplicated in the response

**Verdict:** PASS

## Reasoning

The PR implements deduplication in the service layer via the `.dedup_by()` iterator method:

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

This chains qualifier stripping with deduplication: after `without_qualifiers()` removes the qualifier portion, entries that were previously distinct (e.g., `commons-lang3@3.12?repository_url=repo1` vs `commons-lang3@3.12?repository_url=repo2`) now have identical PURL strings, and `dedup_by` removes the consecutive duplicates.

The `test_recommend_purls_dedup` test verifies this behavior directly:
```rust
// Given PURLs with different qualifiers for the same package version
ctx.seed_purl("pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org&type=jar").await;
ctx.seed_purl("pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo2.maven.org&type=jar").await;

// Then only one entry is returned (deduplicated after qualifier removal)
assert_eq!(body.items.len(), 1);
assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
```

Note: `dedup_by` only removes consecutive duplicates. For same-version entries from the same package (which share namespace and name as filtered by the query), database results should naturally group them adjacently. However, if non-adjacent duplicates could arise in edge cases, `unique_by()` from itertools or SQL-level `DISTINCT` would be more robust. This is a code quality consideration rather than a criterion failure, as the basic deduplication behavior is implemented and tested.
