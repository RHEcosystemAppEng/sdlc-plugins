## Repository
trustify-backend

## Target Branch
main

## Description
Implement relevance ranking in the SearchService so that search results are ordered by relevance to the query rather than an arbitrary order (e.g., insertion order or ID). This addresses the requirement that "results should be more relevant" by applying PostgreSQL full-text search ranking functions (`ts_rank` or `ts_rank_cd`) to score results based on how well they match the search query.

**Assumptions pending clarification:**
- "Relevant" means text-match quality as scored by PostgreSQL's `ts_rank` function (no ranking criteria were specified in the feature description)
- The ranking applies across all searchable entity types (SBOMs, advisories, packages) returned by the search endpoint
- No examples of "irrelevant results" were provided, so it is assumed that the current implementation returns results without text-relevance ordering
- Relevance score may optionally be included in the response to help users understand result ordering

## Files to Modify
- `modules/search/src/service/mod.rs` — Add relevance scoring logic to SearchService queries using `ts_rank` or equivalent PostgreSQL functions; order results by relevance score descending
- `modules/search/src/endpoints/mod.rs` — Update the search endpoint to pass ranking parameters and optionally expose the relevance score in the response
- `tests/api/search.rs` — Add integration tests verifying that results are returned in relevance order

## Implementation Notes
- Use PostgreSQL's `ts_rank(tsvector_column, plainto_tsquery(query))` to compute relevance scores for each result row.
- Apply `ORDER BY rank DESC` to the search query to return most relevant results first.
- Integrate the ranking into the existing SearchService query building logic in `modules/search/src/service/mod.rs`.
- The search endpoint at `GET /api/v2/search` should continue to return `PaginatedResults<T>` — the ranking changes the order within the page, not the response shape.
- Per CONVENTIONS.md "Error handling" convention: ensure any new query logic returns `Result<T, AppError>` with `.context()` wrapping on database errors.
  Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's endpoint handler scope.
- Per CONVENTIONS.md "Response types" convention: continue using `PaginatedResults<T>` from `common/src/model/paginated.rs` for the search response.
  Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's list endpoint scope.
- Per CONVENTIONS.md "Query helpers" convention: use shared query builder helpers from `common/src/db/query.rs` for pagination and sorting integration with the new ranking.
  Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's query-related scope.
- Per CONVENTIONS.md "Testing" convention: add integration tests in `tests/api/` following the `assert_eq!(resp.status(), StatusCode::OK)` pattern against a real PostgreSQL test database.
  Applies: task modifies `tests/api/search.rs` matching the convention's `tests/api/` scope.

## Reuse Candidates
- `common/src/db/query.rs` — Shared query builder helpers for filtering, pagination, and sorting; extend or reuse for integrating relevance ranking with existing pagination logic
- `common/src/model/paginated.rs` — `PaginatedResults<T>` response wrapper; reuse as-is for ranked results
- `modules/fundamental/src/sbom/service/sbom.rs` — SbomService demonstrates the established pattern for service-level query building with SeaORM

## Acceptance Criteria
- [ ] Search results are ordered by text relevance (most relevant first) when a search query is provided
- [ ] Relevance ordering integrates with existing pagination (PaginatedResults)
- [ ] Search with an empty or wildcard query falls back to a sensible default ordering (e.g., most recently created)
- [ ] Existing search endpoint contract is preserved (additive changes only; no breaking changes to request/response shape)
- [ ] Error handling follows the `Result<T, AppError>` pattern with `.context()` wrapping

## Test Requirements
- [ ] Integration test: search for a known term returns the most relevant entity first
- [ ] Integration test: search results ordering changes based on query relevance (e.g., exact match ranks higher than partial match)
- [ ] Integration test: pagination works correctly with relevance-ordered results
- [ ] Integration test: empty search query returns results in default order without error
- [ ] Existing search integration tests in `tests/api/search.rs` continue to pass

## Dependencies
- Depends on: Task 1 — Add database indexes for search performance (relevance ranking requires full-text search indexes to function efficiently)
