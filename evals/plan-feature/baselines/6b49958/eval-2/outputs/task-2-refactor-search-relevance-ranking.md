## Repository
trustify-backend

## Target Branch
main

## Description
Refactor `SearchService` to use PostgreSQL full-text search (`to_tsquery` / `ts_rank`) instead of any existing naive text matching (LIKE/ILIKE), so that search results are ranked by relevance score. This directly addresses the "Results should be more relevant" requirement.

**Assumption (pending clarification):** The feature description does not define what "relevant" means. This task implements PostgreSQL `ts_rank` scoring as the relevance signal, which ranks results by how well they match the search query terms. Additional ranking signals (recency, popularity, entity type priority) are not included and should be specified by the product owner if needed.

**Assumption (pending clarification):** The search query syntax is assumed to be plain text that gets converted to a tsquery via `plainto_tsquery('english', ...)`. Advanced query syntax (boolean operators, phrase matching) is not in scope unless explicitly requested.

## Files to Modify
- `modules/search/src/service/mod.rs` — refactor `SearchService` to use `to_tsquery` and `ts_rank` for full-text search queries against tsvector columns, replacing any LIKE/ILIKE patterns
- `modules/search/src/endpoints/mod.rs` — update the `GET /api/v2/search` endpoint handler to pass search parameters to the refactored service and return results ordered by relevance score

## API Changes
- `GET /api/v2/search` — MODIFY: response results are now ordered by relevance score (descending) instead of default ordering. No breaking changes to request or response shape.

## Implementation Notes
- Inspect `modules/search/src/service/mod.rs` (`SearchService`) to understand the current search implementation before modifying it
- Use `to_tsquery('english', ...)` or `plainto_tsquery('english', ...)` to convert user input to a tsquery
- Use `ts_rank(tsvector_column, tsquery)` to compute relevance scores
- Order results by `ts_rank` descending to surface the most relevant matches first
- The tsvector columns and GIN indexes from Task 1 must be present for this to function efficiently
- Follow the error handling pattern from `common/src/error.rs` — all handlers return `Result<T, AppError>` with `.context()` wrapping
- Return results using `PaginatedResults<T>` from `common/src/model/paginated.rs`, consistent with all other list endpoints
- The existing endpoint at `modules/search/src/endpoints/mod.rs` (`GET /api/v2/search`) already exists — this task modifies its internal implementation, not its route registration

## Reuse Candidates
- `common/src/db/query.rs` — existing query builder helpers for filtering, pagination, and sorting that should be extended or composed with the new full-text search logic
- `common/src/model/paginated.rs::PaginatedResults<T>` — standard response wrapper used by all list endpoints
- `common/src/error.rs::AppError` — error handling enum for consistent error responses
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — example of service pattern (fetch, list methods) to follow for the refactored SearchService

## Acceptance Criteria
- [ ] `SearchService` uses PostgreSQL full-text search (tsquery/tsvector) for all search queries
- [ ] Search results are returned ordered by `ts_rank` relevance score (descending)
- [ ] The `GET /api/v2/search` endpoint response shape remains backward-compatible (no breaking changes)
- [ ] Queries with no matching results return an empty `PaginatedResults` response (not an error)
- [ ] Existing integration tests in `tests/api/search.rs` pass (or are updated to reflect relevance ordering)

## Test Requirements
- [ ] Integration test: search for a known term returns matching entities ranked by relevance (most relevant first)
- [ ] Integration test: search for a term that matches multiple entity types returns all matching types with correct relevance ordering
- [ ] Integration test: search for a non-existent term returns an empty result set with HTTP 200
- [ ] Integration test: verify that partial word matches work as expected with the chosen tsquery conversion
- [ ] Regression: all existing tests in `tests/api/search.rs` continue to pass

## Dependencies
- Depends on: Task 1 — Add full-text search indexes (tsvector columns and GIN indexes must exist)

[sdlc-workflow] Description digest: sha256:8bd12c745f5a946242377542b12766afe3739534404df10eef7c6a8d8fee9e16
