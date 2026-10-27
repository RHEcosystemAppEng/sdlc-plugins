# Criterion 5: Response shape unchanged

**Criterion:** Response shape is unchanged (still `PaginatedResults<PurlSummary>`)

**Result:** PASS

## Analysis

The endpoint handler in `modules/fundamental/src/purl/endpoints/recommend.rs` maintains the same return type signature:

```rust
pub async fn recommend_purls(
    db: DatabaseConnection,
    Query(params): Query<RecommendParams>,
) -> Result<Json<PaginatedResults<PurlSummary>>, AppError> {
```

This return type is unchanged between the base branch and the PR branch. The diff shows only whitespace/formatting changes in the endpoint file — the `use sea_orm::JoinType;` import was removed (no longer needed), but the handler signature and return type are identical.

In the service layer (`modules/fundamental/src/purl/service/mod.rs`), the `recommend` method still returns `Result<PaginatedResults<PurlSummary>>` and constructs the response as:
```rust
Ok(PaginatedResults { items, total })
```

The `PurlSummary` struct itself is not modified — only the value assigned to its `purl` field changes (from fully qualified to versioned-only). The struct shape, the pagination wrapper, and the JSON serialization format remain identical, ensuring backward compatibility for API consumers.

All test files use `let body: PaginatedResults<PurlSummary> = resp.json().await;` to deserialize responses, confirming the response shape is consistent.
