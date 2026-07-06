# Criterion 5: Response shape is unchanged

## Acceptance Criterion

> Response shape is unchanged (still `PaginatedResults<PurlSummary>`)

## Verdict: PASS

## Reasoning

### Endpoint return type

The endpoint handler in `modules/fundamental/src/purl/endpoints/recommend.rs` retains the same return type:

```rust
pub async fn recommend_purls(
    db: DatabaseConnection,
    Query(params): Query<RecommendParams>,
) -> Result<Json<PaginatedResults<PurlSummary>>, AppError> {
```

The PR diff shows no change to the function signature or return type -- only the removal of the unused `JoinType` import and a whitespace adjustment.

### Service return type

The service method in `modules/fundamental/src/purl/service/mod.rs` continues to return `Result<PaginatedResults<PurlSummary>>` and constructs the result as:

```rust
Ok(PaginatedResults { items, total })
```

The `items` field is still a `Vec<PurlSummary>` (each item constructed as `PurlSummary { purl: simplified.to_string() }`), and `total` is still a count value.

### Test evidence

All tests in the PR deserialize the response as `PaginatedResults<PurlSummary>`:

```rust
let body: PaginatedResults<PurlSummary> = resp.json().await;
```

This appears in `test_recommend_purls_basic`, `test_recommend_purls_dedup`, `test_recommend_purls_unknown_returns_empty` (unchanged), `test_recommend_purls_pagination` (unchanged), and all three tests in `purl_simplify.rs`. The deserialization would fail at runtime if the response shape had changed.

### Model types

The `PaginatedResults<T>` wrapper is defined in `common/src/model/paginated.rs` and is not modified by this PR. The `PurlSummary` type is also not modified -- only the content of its `purl` field changes (from fully qualified to versioned without qualifiers).

This criterion is satisfied.
