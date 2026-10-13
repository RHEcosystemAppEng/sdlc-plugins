# Criterion 4: Existing pagination and sorting behavior is preserved

## Criterion Text

Existing pagination and sorting behavior is preserved

## Verdict: PASS

## Reasoning

### Code Changes -- Pagination Preserved

The pagination mechanism in `modules/fundamental/src/purl/service/mod.rs` is unchanged:

```rust
let items = query
    .offset(offset.unwrap_or(0) as u64)
    // .limit(...) continues on next line in the diff
    .all(&self.db)
    .await?
```

The `offset` and `limit` parameters are still applied to the database query. The query parameter handling in the endpoint (`modules/fundamental/src/purl/endpoints/recommend.rs`) is also unchanged -- the `RecommendParams` struct still accepts `offset` and `limit` query parameters.

### Code Changes -- Sorting Preserved

The diff does not modify any ordering or sorting logic. The query builder does not add or remove any `ORDER BY` clause. Whatever ordering behavior existed before (either explicit ordering in the query builder or database-default ordering) remains the same.

### Code Changes -- Response Shape Preserved

The handler signature is unchanged:

```rust
pub async fn recommend_purls(
    db: DatabaseConnection,
    Query(params): Query<RecommendParams>,
) -> Result<Json<PaginatedResults<PurlSummary>>, AppError>
```

The `PaginatedResults` wrapper with `items` and `total` fields is still used.

### Existing Test Coverage

The base-branch `test_recommend_purls_pagination` test (visible in `test-base-purl-recommend.md`) is NOT modified in the diff, meaning it remains in the PR branch unchanged. This test:

```rust
// Seeds 5 versioned PURLs
for i in 1..=5 {
    ctx.seed_purl(&format!(
        "pkg:maven/org.apache/commons-lang3@3.{}?repository_url=https://repo1.maven.org&type=jar",
        i
    )).await;
}

// Requests with limit=2
let resp = ctx.get("/api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3&limit=2").await;

// Asserts pagination
assert_eq!(body.items.len(), 2);
assert_eq!(body.total, 5);
```

This test continues to pass after the changes because:
- Each seeded PURL has a unique version (3.1 through 3.5), so after qualifier stripping they remain 5 distinct PURLs
- `dedup_by` does not collapse any entries since all versions differ
- The `total` count correctly reports 5
- The `limit=2` correctly returns only 2 items

### New Test Coverage

The `test_simplified_purl_ordering_preserved` test in the new `purl_simplify.rs` explicitly validates pagination with the simplified format:

```rust
ctx.seed_purl("pkg:maven/org.apache/commons-lang3@3.10?type=jar").await;
ctx.seed_purl("pkg:maven/org.apache/commons-lang3@3.11?type=jar").await;
ctx.seed_purl("pkg:maven/org.apache/commons-lang3@3.12?type=jar").await;

let resp = ctx.get("/api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3&limit=2").await;

assert_eq!(body.items.len(), 2);
assert_eq!(body.total, 3);
```

This confirms that pagination (limit) works correctly with the new qualifier-free responses and that `total` reflects the full count.

### CI Confirmation

All CI checks pass, including both the existing pagination test and the new ordering test.

## Conclusion

The pagination mechanism (offset/limit) is untouched. The existing pagination test continues to pass. A new test further validates pagination behavior with the simplified format. This criterion is satisfied.
