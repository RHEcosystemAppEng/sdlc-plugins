# Criterion 5: Response shape is unchanged (still `PaginatedResults<PurlSummary>`)

**Verdict: PASS**

## Evidence
- **Handler:** the signature in `modules/fundamental/src/purl/endpoints/recommend.rs` is unchanged: `Result<Json<PaginatedResults<PurlSummary>>, AppError>`. The only changes in that file are the removed `JoinType` import and one whitespace-only line.
- **Service:** `PurlService::recommend` still returns `Result<PaginatedResults<PurlSummary>>` and builds `Ok(PaginatedResults { items, total })`.
- **`PurlSummary`:** it still has only the `purl: String` field. Only the field's value changed.
- **Tests:** every test deserializes the response into `PaginatedResults<PurlSummary>`, and CI passes.

## Caveat
The shape is unchanged, but `total` no longer matches the deduplicated `items` (see criterion 4). That is a problem with what the field means, not with the shape.
