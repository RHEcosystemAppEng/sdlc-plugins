# Task 2: Implement search result relevance ranking

## Repository
trustify-backend

## Target Branch
main

## Description
Add relevance scoring to search results using PostgreSQL's `ts_rank` function so that results matching the search query more closely appear first. Currently, search results have no relevance-based ordering, which means users see results in an arbitrary order. This task adds a relevance score to each result and sorts by relevance by default when a text search query is provided.

This addresses the MVP requirement "Results should be more relevant" from TC-9002. Note: the feature did not define specific relevance criteria. The implementation uses PostgreSQL `ts_rank` as the ranking signal; further tuning (field weighting, boosting) may be needed based on user feedback.

## Files to Modify
- `modules/search/src/service/mod.rs` -- add `ts_rank` computation to search queries and return results sorted by relevance score (descending) by default
- `modules/search/src/endpoints/mod.rs` -- add optional `sort` query parameter to allow overriding the default relevance-based sort order
- `tests/api/search.rs` -- add integration tests for relevance ranking behavior

## Implementation Notes
- Use PostgreSQL `ts_rank(tsvector_column, to_tsquery(query))` to compute a relevance score for each matching result.
- Add the relevance score as an `ORDER BY` clause (descending) in search queries when a text query is present.
- When no text query is provided (empty search / browse mode), preserve the existing sort order.
- Add an optional `sort` query parameter to the search endpoint (e.g., `sort=relevance`, `sort=name`, `sort=date`) so users can override the default. If omitted, default to relevance when a query is present.
- Per CONVENTIONS.md §Endpoint registration: routes are registered in each module's `endpoints/mod.rs`; `server/main.rs` mounts all modules. Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's endpoint registration scope.
- Per CONVENTIONS.md §Error handling: all handlers return `Result<T, AppError>` with `.context()` wrapping. Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's handler file scope.
- Per CONVENTIONS.md §Response types: list endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`. Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's endpoint file scope.
- Per CONVENTIONS.md §Query helpers: use shared sorting helpers from `common/src/db/query.rs` for adding relevance-based sort ordering. Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's service query file scope.
- Per CONVENTIONS.md §Caching: uses `tower-http` caching middleware; cache configuration in endpoint route builders. Consider cache implications of relevance-sorted results (same query returns same order, so caching is still effective). Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's endpoint route builder scope.
- Per CONVENTIONS.md §Testing: integration tests in `tests/api/` use a real PostgreSQL test database with `assert_eq!(resp.status(), StatusCode::OK)` pattern. Applies: task modifies `tests/api/search.rs` matching the convention's test file scope.

## Reuse Candidates
- `common/src/db/query.rs` -- shared query builder helpers for sorting; extend with relevance-based sort option
- `common/src/model/paginated.rs::PaginatedResults` -- existing response wrapper; maintain compatibility
- `modules/fundamental/src/sbom/endpoints/list.rs` -- example list endpoint with query parameters and sorting

## Acceptance Criteria
- [ ] Search results include a relevance score computed via `ts_rank` when a text query is provided
- [ ] Results are sorted by relevance score (descending) by default when a search query is present
- [ ] Users can override sort order via the `sort` query parameter
- [ ] Search without a text query (browse mode) preserves existing sort order
- [ ] Response shape remains `PaginatedResults<T>` (backward-compatible)

## Test Requirements
- [ ] Verify that results with exact keyword matches rank higher than partial matches
- [ ] Verify that default sort order is by relevance when a search query is present
- [ ] Verify that the `sort` parameter overrides default relevance sorting
- [ ] Verify that search without a query returns results in the pre-existing order
- [ ] Existing search integration tests continue to pass

## Verification Commands
- `cargo test --test api search` -- verify all search integration tests pass

## Dependencies
- Depends on: Task 1 -- Add full-text search indexes (GIN indexes and tsvector columns are required for ts_rank scoring)
