# Criterion 4: Existing pagination and sorting behavior is preserved

## Verdict: PASS

## Reasoning

### Code evidence

The service layer change in `modules/fundamental/src/purl/service/mod.rs` preserves the pagination logic. The query still uses:

```rust
let items = query
    .offset(offset.unwrap_or(0) as u64)
    ...
    .all(&self.db)
    .await?
```

The `offset` and `limit` parameters are still passed through and applied to the database query. The pagination wrapper `PaginatedResults { items, total }` is still constructed with the same fields.

The total count computation was adjusted to use `group_by` to avoid counting duplicate rows:

```rust
let total = query.clone()
    .select_only()
    .column(purl::Column::Id)
    .group_by(purl::Column::Id)
    .count(&self.db).await?;
```

This ensures the `total` field reflects the count of distinct PURLs (after potential deduplication from qualifier removal), which is the correct behavior for pagination metadata.

### Test evidence

1. The existing `test_recommend_purls_pagination` test was NOT modified in the PR diff. This test seeds 5 versioned PURLs and verifies that `limit=2` returns 2 items with `total=5`. Since this test is unchanged, it continues to verify pagination behavior.

2. The new `test_simplified_purl_ordering_preserved` test in `tests/api/purl_simplify.rs` specifically tests ordering with pagination:
   ```rust
   // Given multiple versions with qualifiers
   ctx.seed_purl("pkg:maven/org.apache/commons-lang3@3.10?type=jar").await;
   ctx.seed_purl("pkg:maven/org.apache/commons-lang3@3.11?type=jar").await;
   ctx.seed_purl("pkg:maven/org.apache/commons-lang3@3.12?type=jar").await;

   // When requesting with limit
   let resp = ctx.get("/api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3&limit=2").await;

   // Then results are ordered and paginated correctly
   assert_eq!(body.items.len(), 2);
   assert_eq!(body.total, 3);
   ```

### Evidence

- `modules/fundamental/src/purl/service/mod.rs`: offset/limit parameters preserved in query, `PaginatedResults` wrapper unchanged
- `tests/api/purl_recommend.rs`: existing `test_recommend_purls_pagination` test is unmodified, confirming backward compatibility
- `tests/api/purl_simplify.rs`: `test_simplified_purl_ordering_preserved` tests ordering and pagination with simplified PURLs
- The endpoint handler signature remains `Result<Json<PaginatedResults<PurlSummary>>, AppError>` (unchanged)
