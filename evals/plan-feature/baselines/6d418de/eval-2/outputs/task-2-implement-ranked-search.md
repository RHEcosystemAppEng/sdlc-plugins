# Task 2 — Implement ranked full-text search in SearchService

## Repository
trustify-backend

## Target Branch
main

## Description
Extend the `SearchService` in `modules/search/src/service/mod.rs` to use PostgreSQL's full-text search ranking functions (`ts_rank`, `to_tsquery`) instead of basic text matching. Search results should be scored and returned in descending relevance order, so users see the most relevant results first.

The current search implementation performs basic matching without ranking. This task converts it to leverage the tsvector columns and GIN indexes added in Task 1, producing ranked results that address the user complaint about irrelevant search results.

## Files to Modify
- `modules/search/src/service/mod.rs` — Refactor `SearchService` to use `ts_rank` and `to_tsquery` for ranked full-text search across sbom, advisory, and package entities
- `modules/search/src/endpoints/mod.rs` — Update the `GET /api/v2/search` handler to pass ranking parameters and return results sorted by relevance score

## Files to Create
- `modules/search/src/model/mod.rs` — Search result model with relevance score field
- `modules/search/src/model/search_result.rs` — `SearchResult` struct containing entity reference, entity type, and relevance score

## API Changes
- `GET /api/v2/search` — MODIFY: Response now includes a `score` field per result and results are ordered by descending relevance score by default. The `q` query parameter now uses PostgreSQL `to_tsquery` parsing.

## Implementation Notes
- Follow the existing module pattern (model/ + service/ + endpoints/) seen in `modules/fundamental/src/sbom/` and `modules/fundamental/src/advisory/`
- The `SearchResult` model should include: entity_id, entity_type (enum: Sbom, Advisory, Package), display_name, summary snippet, and relevance_score (f32)
- Use `ts_rank(tsvector_column, to_tsquery('english', query))` for scoring
- Use `to_tsquery` with the 'english' configuration for word stemming and normalization
- Handle malformed query strings gracefully — wrap `to_tsquery` parsing in error handling that falls back to `plainto_tsquery` for queries with invalid tsquery syntax
- Results must be sorted by `ts_rank` descending (most relevant first)
- Return type should use `PaginatedResults<SearchResult>` from `common/src/model/paginated.rs` for consistency with other endpoints
- All handlers must return `Result<T, AppError>` with `.context()` wrapping per the established error handling pattern (see `common/src/error.rs`)
- Per docs/constraints.md section 5.4: reuse existing utilities from `common/src/db/query.rs` for pagination and sorting
- Per docs/constraints.md section 5.2: inspect `modules/search/src/service/mod.rs` before modifying to understand the current search implementation

## Reuse Candidates
- `common/src/db/query.rs` — Shared query builder helpers for pagination and sorting; reuse for paginated search results
- `common/src/model/paginated.rs` — `PaginatedResults<T>` wrapper; use as the response type for search results
- `common/src/error.rs` — `AppError` enum with `IntoResponse`; follow the same error handling pattern
- `modules/fundamental/src/advisory/service/advisory.rs` — `AdvisoryService` includes a `search` method that may demonstrate existing search patterns to follow or extend

## Acceptance Criteria
- [ ] Search results include a relevance score and are ordered by descending score
- [ ] Search uses PostgreSQL full-text search functions (ts_rank, to_tsquery)
- [ ] Search queries are parsed with English stemming (e.g., "vulnerabilities" matches "vulnerability")
- [ ] Malformed query strings are handled gracefully without returning 500 errors
- [ ] Response format uses PaginatedResults wrapper consistent with other endpoints
- [ ] Existing search functionality is preserved (queries that worked before still work)

## Test Requirements
- [ ] Test that search results are returned in descending relevance order
- [ ] Test that a search for a known term returns the expected entity with a non-zero score
- [ ] Test that search across multiple entity types returns mixed results ranked by relevance
- [ ] Test that a malformed query string returns results (via plainto_tsquery fallback) rather than an error
- [ ] Test that empty search queries return an appropriate response (empty results or validation error)

## Verification Commands
- `cargo test -p search` — all search module tests pass
- `cargo test -p tests -- search` — integration tests in tests/api/search.rs pass

## Dependencies
- Depends on: Task 1 — Add full-text search indexes via database migration
