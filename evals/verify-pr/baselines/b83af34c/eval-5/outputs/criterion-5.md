# Criterion 5: Response shape unchanged

## Acceptance Criterion

> Response shape is unchanged (still `PaginatedResults<PurlSummary>`)

## Verdict: PASS

## Analysis

### Implementation Evidence

The endpoint handler in `modules/fundamental/src/purl/endpoints/recommend.rs` retains the same return type signature:

```rust
pub async fn recommend_purls(
    db: DatabaseConnection,
    Query(params): Query<RecommendParams>,
) -> Result<Json<PaginatedResults<PurlSummary>>, AppError> {
```

The return type `Result<Json<PaginatedResults<PurlSummary>>, AppError>` is unchanged. The `PaginatedResults` wrapper (defined in `common/src/model/paginated.rs`) still contains `items` and `total` fields.

### Service Layer Evidence

The service method in `modules/fundamental/src/purl/service/mod.rs` still returns:

```rust
Ok(PaginatedResults { items, total })
```

The `PurlSummary` struct is still used for each item:

```rust
PurlSummary {
    purl: simplified.to_string(),
}
```

Only the value assigned to `purl` changed (from `p.to_string()` to `simplified.to_string()`); the struct and its fields remain identical.

### Test Evidence

All tests in both `tests/api/purl_recommend.rs` and `tests/api/purl_simplify.rs` deserialize the response as `PaginatedResults<PurlSummary>`:

```rust
let body: PaginatedResults<PurlSummary> = resp.json().await;
```

This deserialization would fail at runtime if the response shape had changed, confirming the JSON structure is identical.

### Conclusion

The response shape is unchanged. The endpoint still returns `PaginatedResults<PurlSummary>` with `items` (a list of `PurlSummary` objects each containing a `purl` string) and `total` (count of all matching results). Only the content of the `purl` field changed (qualifiers stripped); the structural contract is preserved.
