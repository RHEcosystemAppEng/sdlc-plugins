# Task 2 — Add relevance scoring to SearchService

## Repository
trustify-backend

## Target Branch
main

## Description
Refactor the `SearchService` in `modules/search/src/service/mod.rs` to use PostgreSQL's full-text search ranking functions (`ts_rank` or `ts_rank_cd`) against the tsvector columns created in Task 1. Currently, search returns results without relevance ordering. This task adds a relevance score to each result and enables sorting by relevance, directly addressing the requirement that "results should be more relevant."

## Files to Modify
- `modules/search/src/service/mod.rs` — refactor SearchService to use `ts_rank()` for relevance-scored full-text search queries
- `modules/search/src/endpoints/mod.rs` — update the GET /api/v2/search endpoint to accept an optional `sort=relevance` query parameter and return the relevance score in results

## API Changes
- `GET /api/v2/search` — MODIFY: response items now include a `relevance_score: f32` field; accepts optional `sort` query parameter with value `relevance` (default sort order when a search query is provided)

## Implementation Notes
- Use PostgreSQL's `ts_rank(tsvector, tsquery)` function via SeaORM's raw expression or `SimpleExpr` API to compute relevance scores.
- Convert the user's search query into a `tsquery` using `plainto_tsquery()` or `websearch_to_tsquery()` for natural language search support.
- The relevance score should be returned as a float field alongside each result item.
- Default sort order when a query string is present should be by relevance (descending). When no query string is provided, fall back to the existing sort order.
- Follow the existing error handling pattern: all handlers return `Result<T, AppError>` with `.context()` wrapping (see `common/src/error.rs`).
- Follow the existing query builder patterns in `common/src/db/query.rs` for filtering, pagination, and sorting integration.
- Per CONVENTIONS.md: follow the established module pattern (model/ + service/ + endpoints/) for any structural changes.
  Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's Rust module scope.

## Reuse Candidates
- `common/src/db/query.rs` — shared query builder helpers for filtering, pagination, and sorting; extend rather than duplicate for relevance sort support
- `common/src/model/paginated.rs` — `PaginatedResults<T>` response wrapper; the relevance score may need to be added to the result item type or as a wrapper
- `common/src/error.rs` — `AppError` enum for consistent error handling

## Acceptance Criteria
- [ ] Search results include a `relevance_score` field when a text query is provided
- [ ] Results are sorted by relevance score (descending) by default when a search query is present
- [ ] An optional `sort` query parameter allows switching between relevance and other sort orders
- [ ] Search queries without a text query (e.g., filter-only) continue to work with the existing sort order
- [ ] The search endpoint remains backward compatible — existing API consumers are not broken

## Test Requirements
- [ ] Integration test: search with a text query returns results ordered by relevance (most relevant first)
- [ ] Integration test: search results include a non-zero relevance score for matching items
- [ ] Integration test: search without a text query returns results without relevance scoring (backward compatibility)
- [ ] Integration test: `sort=relevance` query parameter works correctly
- [ ] Tests added in `tests/api/search.rs` following the existing `assert_eq!(resp.status(), StatusCode::OK)` pattern

## Verification Commands
- `cargo test -p search` — search module unit tests pass
- `cargo test --test search` — search integration tests pass

## Dependencies
- Depends on: Task 1 — Add full-text search indexes via database migration
