# Criterion 5

**Criterion:** Response shape is unchanged (still `PaginatedResults<PurlSummary>`)

**Verdict:** PASS

## What was checked

- `modules/fundamental/src/purl/endpoints/recommend.rs`: the handler signature
  `-> Result<Json<PaginatedResults<PurlSummary>>, AppError>` is unchanged; it appears as context lines in the diff.
- `modules/fundamental/src/purl/service/mod.rs`: `recommend` still returns `Result<PaginatedResults<PurlSummary>>` and builds `PaginatedResults { items, total }`. `PurlSummary` is still built with just its `purl: String` field. The struct definition is not modified.
- Tests in both `tests/api/purl_recommend.rs` and `tests/api/purl_simplify.rs` deserialize the response as `PaginatedResults<PurlSummary>` and read `.items[..].purl` and `.total`. This confirms the wire shape. CI passes.

Only the content of the `purl` string changes (no qualifiers). The response structure is identical.
