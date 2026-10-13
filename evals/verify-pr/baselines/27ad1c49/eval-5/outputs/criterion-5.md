# Criterion 5: Response shape is unchanged

## Criterion Text

Response shape is unchanged (still `PaginatedResults<PurlSummary>`)

## Verdict: PASS

## Reasoning

### Code Changes

The handler return type in `modules/fundamental/src/purl/endpoints/recommend.rs` remains:

```rust
pub async fn recommend_purls(
    db: DatabaseConnection,
    Query(params): Query<RecommendParams>,
) -> Result<Json<PaginatedResults<PurlSummary>>, AppError>
```

The return type `Result<Json<PaginatedResults<PurlSummary>>, AppError>` is unchanged. The `PaginatedResults<PurlSummary>` wrapper continues to be the response envelope.

### Service Layer

In `modules/fundamental/src/purl/service/mod.rs`, the `recommend` method still returns `Result<PaginatedResults<PurlSummary>>`. The mapping still constructs `PurlSummary { purl: ... }` instances, and the results are still wrapped in `PaginatedResults { items, total }`.

The only change in the mapping is what string goes into the `purl` field:
- Before: `p.to_string()` (full PURL with qualifiers)
- After: `p.without_qualifiers().to_string()` (PURL without qualifiers)

The structure of the response object is identical -- only the content of the `purl` string field changes.

### Test Evidence

All tests deserialize the response into the same types:

```rust
let body: PaginatedResults<PurlSummary> = resp.json().await;
```

This deserialization would fail at runtime if the response shape changed. The fact that all tests pass (and CI is green) confirms the response shape remains `PaginatedResults<PurlSummary>`.

The tests access `body.items`, `body.items.len()`, `body.items[0].purl`, and `body.total` -- confirming both the outer `PaginatedResults` structure (with `items` and `total` fields) and the inner `PurlSummary` structure (with a `purl` field) are preserved.

### Import Evidence

The test files import the same types as before:

```rust
use common::model::paginated::PaginatedResults;
use common::purl::PurlSummary;
```

No changes to these imports in any test file.

### CI Confirmation

All CI checks pass, confirming the response shape deserialization works correctly.

## Conclusion

The return type, response structure (`PaginatedResults<PurlSummary>`), and field layout are all unchanged. Only the content of the `purl` string field within `PurlSummary` changes (qualifiers removed). This criterion is satisfied.
