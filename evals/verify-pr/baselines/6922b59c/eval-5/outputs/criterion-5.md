## Criterion 5: Response shape is unchanged (still `PaginatedResults<PurlSummary>`)

### Verdict: PASS

### Analysis

The endpoint handler signature and return type are unchanged:

```rust
pub async fn recommend_purls(
    db: DatabaseConnection,
    Query(params): Query<RecommendParams>,
) -> Result<Json<PaginatedResults<PurlSummary>>, AppError> {
```

The return type remains `Result<Json<PaginatedResults<PurlSummary>>, AppError>`. The `PaginatedResults<T>` wrapper (defined in `common/src/model/paginated.rs` per the repository structure) still contains `items: Vec<T>` and `total: i64` fields.

The `PurlSummary` struct itself was not modified -- the PR only changes what value is assigned to its `purl` field (now a simplified PURL without qualifiers). The struct's shape and serialization remain the same.

**Test coverage**: All test functions in both `purl_recommend.rs` and `purl_simplify.rs` deserialize the response as `PaginatedResults<PurlSummary>`:

```rust
let body: PaginatedResults<PurlSummary> = resp.json().await;
```

If the response shape had changed, this deserialization would fail and the tests would not pass. Since all CI checks pass, the response shape is confirmed to be unchanged.
