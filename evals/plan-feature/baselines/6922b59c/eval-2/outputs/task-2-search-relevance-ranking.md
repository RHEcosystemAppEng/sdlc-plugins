## Repository
trustify-backend

## Target Branch
main

## Description
Add relevance scoring to search results so that results matching the search query more closely appear higher in the list. Currently the GET /api/v2/search endpoint returns results without any ranking by match quality.

**Assumption (pending clarification):** Relevance will be determined by PostgreSQL full-text search ranking functions (`ts_rank` or `ts_rank_cd`). The feature description TC-9002 does not specify a ranking algorithm, weighting scheme, or definition of what constitutes a "relevant" result. This approach should be validated with stakeholders before implementation.

## Files to Modify
- `modules/search/src/service/mod.rs` -- Add relevance scoring logic using `ts_rank` to SearchService queries
- `modules/search/src/endpoints/mod.rs` -- Update search endpoint to support `sort_by=relevance` parameter and return scores in response
- `common/src/model/paginated.rs` -- Extend `PaginatedResults<T>` to support optional relevance score per item (or add a `ScoredResult<T>` wrapper)

## API Changes
- `GET /api/v2/search` -- MODIFY: Response items include an optional `relevance_score` field (f64). Add optional `sort_by` query parameter accepting `relevance` (default for text queries) or `date`

## Implementation Notes
- Use PostgreSQL `ts_rank()` or `ts_rank_cd()` functions to compute per-result relevance scores based on the full-text search query match quality.
- Default sort order for search results should be by relevance score (descending) when a text query is provided. When no query is provided (listing all), fall back to the existing sort order.
- Per CONVENTIONS.md §Response Types: list endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`. Extend this wrapper to include an optional `score` field or introduce a `ScoredPaginatedResults<T>` type. See existing usage in `modules/fundamental/src/sbom/endpoints/list.rs`.
  Applies: task modifies `common/src/model/paginated.rs` matching the convention's `.rs` response type scope.
- Per CONVENTIONS.md §Error Handling: wrap ranking computation and sort parameter validation with `.context()` for descriptive error messages.
  Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's `.rs` error handling scope.
- Per CONVENTIONS.md §Endpoint Registration: follow existing route registration and query parameter extraction patterns in `modules/search/src/endpoints/mod.rs`. See `modules/fundamental/src/sbom/endpoints/mod.rs` for the established pattern.
  Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's `.rs` endpoint registration scope.
- Reference existing sort parameter handling in `common/src/db/query.rs` for implementing the `sort_by` parameter.

## Reuse Candidates
- `common/src/db/query.rs` -- Existing sorting utilities that can be extended for relevance-based sorting
- `common/src/model/paginated.rs::PaginatedResults` -- Response wrapper to extend with scoring capability
- `modules/fundamental/src/sbom/endpoints/list.rs` -- Example of list endpoint with sorting; reference for sort parameter handling pattern

## Acceptance Criteria
- [ ] Search results include a `relevance_score` field for each result when a text query is provided
- [ ] Results are sorted by relevance score by default when a text query is present (highest relevance first)
- [ ] API response includes the relevance score per item in the response body
- [ ] A `sort_by` query parameter is accepted with values `relevance` and `date`
- [ ] Existing search behavior is preserved when no search query text is provided (returns all results in existing order)
- [ ] Existing search tests continue to pass

## Test Requirements
- [ ] Integration test verifying search results are sorted by relevance score (descending) for a text query
- [ ] Integration test verifying `relevance_score` field is present in the response for each result
- [ ] Integration test with multiple entities where one has a stronger text match to verify correct ranking order
- [ ] Integration test verifying `sort_by=date` overrides relevance sorting
- [ ] Existing tests in `tests/api/search.rs` continue to pass

## Verification Commands
- `cargo test --test search` -- search tests pass including new relevance tests

## Dependencies
- Depends on: Task 1 -- Add database indexes and optimize search queries for performance (full-text indexes are needed for ts_rank scoring)
