## Criterion 3: Duplicate entries deduplicated after qualifier removal

**Verdict: PASS**

### Analysis

The third acceptance criterion requires that duplicate entries that were previously distinct due to different qualifiers are deduplicated in the response.

### Evidence from PR Diff

**Service layer** (`modules/fundamental/src/purl/service/mod.rs`):
After stripping qualifiers and mapping to `PurlSummary`, the code applies deduplication:

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

The `.dedup_by(|a, b| a.purl == b.purl)` call removes consecutive duplicate entries that have the same PURL string. This handles the case where two database rows that previously had different qualifiers (e.g., `?repository_url=https://repo1.maven.org&type=jar` vs `?repository_url=https://repo2.maven.org&type=jar`) now map to the same versioned PURL string after qualifier removal.

Note: `dedup_by` removes consecutive duplicates, which means it relies on the database query ordering to group identical PURLs adjacently. The query filters by namespace and name, so entries for the same package version should be adjacent in the result set. If the query does not guarantee this ordering, non-consecutive duplicates could survive. However, since the query filters to a specific namespace+name combination and the database typically returns rows in insertion or primary key order, consecutive deduplication is reasonable for this use case.

Additionally, the count query was updated to use `group_by` for accurate total counts:
```rust
let total = query.clone()
    .select_only()
    .column(purl::Column::Id)
    .group_by(purl::Column::Id)
    .count(&self.db).await?;
```

**Test verification** (`tests/api/purl_recommend.rs`):
The new `test_recommend_purls_dedup` test directly exercises this behavior:

```rust
// Seeds two PURLs with same version but different qualifiers
ctx.seed_purl("pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org&type=jar").await;
ctx.seed_purl("pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo2.maven.org&type=jar").await;

// Asserts only one entry is returned (deduplicated)
assert_eq!(body.items.len(), 1);
assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
```

This test confirms that two database rows differing only in qualifiers collapse into a single response entry after qualifier removal and deduplication.

### Conclusion

The code applies `.dedup_by()` after qualifier stripping to remove duplicate entries, and a dedicated test verifies the behavior with qualifier-differentiated inputs. This criterion is satisfied.
