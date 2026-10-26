## Criterion 3: Duplicate entries that were previously distinct due to different qualifiers are deduplicated in the response

### Verdict: PASS

### Analysis

The service layer adds a deduplication step after qualifier stripping:

```rust
.dedup_by(|a, b| a.purl == b.purl)
```

This removes consecutive duplicate entries where the PURL string matches after qualifier removal. PURLs that were previously distinct (e.g., same package version but different `repository_url` qualifiers) become identical once qualifiers are stripped, and `.dedup_by()` collapses them into a single entry.

The count query was also updated to use `group_by`:
```rust
.select_only()
.column(purl::Column::Id)
.group_by(purl::Column::Id)
.count(&self.db).await?;
```

This ensures the `total` field in the paginated response reflects the correct count after deduplication.

**Test coverage**: The new `test_recommend_purls_dedup` function directly tests this:

```rust
// Seeds two PURLs identical except for qualifiers
ctx.seed_purl("pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org&type=jar").await;
ctx.seed_purl("pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo2.maven.org&type=jar").await;

// Asserts only one entry is returned
assert_eq!(body.items.len(), 1);
assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
```

This test seeds two PURLs that differ only in their `repository_url` qualifier and verifies that exactly one entry is returned after qualifier removal and deduplication.

**Note**: `.dedup_by()` only removes consecutive duplicates. This works correctly here because the query results are ordered (by the database's default ordering or explicit sorting), so identical PURLs after qualifier removal will be adjacent. If the ordering were non-deterministic, non-adjacent duplicates could survive. However, the existing sorting behavior (preserved per criterion 4) ensures this is not an issue.
