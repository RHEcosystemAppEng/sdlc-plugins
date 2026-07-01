# Task 5 — Update search endpoint response to use PaginatedResults with ranked results

## Repository
trustify-backend

## Target Branch
main

## Description
Update the search endpoint (`GET /api/v2/search`) to return `PaginatedResults<SearchResultSummary>` with proper pagination support, consistent with all other list endpoints in the codebase. This ensures the search endpoint follows the same response format convention as SBOM, advisory, and package list endpoints, and enables consumers to paginate through large result sets efficiently.

## Files to Modify
- `modules/search/src/endpoints/mod.rs` — update the endpoint handler to accept pagination query parameters (`offset`, `limit`) and return `PaginatedResults<SearchResultSummary>` instead of the current response type
- `modules/search/src/service/mod.rs` — update `SearchService` methods to accept pagination parameters and return total count alongside results for `PaginatedResults` construction

## Implementation Notes
- Follow the pagination pattern established in `modules/fundamental/src/sbom/endpoints/list.rs` — the `GET /api/v2/sbom` endpoint demonstrates the standard approach for accepting `offset`/`limit` parameters and returning `PaginatedResults<T>`.
- Use `PaginatedResults<T>` from `common/src/model/paginated.rs` as the response wrapper. This ensures consistency with all other list endpoints.
- The pagination should compose with the full-text search ranking from Task 3 — results are first ranked by relevance, then paginated. The `total` count in `PaginatedResults` should reflect the total number of matches before pagination, so consumers know how many results exist.
- The pagination should also compose with filters from Task 4 — filtered results are counted and paginated correctly.
- Default pagination values should follow the existing conventions (check `common/src/db/query.rs` for default offset/limit values).
- Apply `tower-http` caching middleware configuration to the updated endpoint, following the pattern in other endpoint route builders.

## Reuse Candidates
- `common/src/model/paginated.rs::PaginatedResults<T>` — the shared pagination response wrapper used by all list endpoints
- `common/src/db/query.rs` — pagination query helpers (offset, limit)
- `modules/fundamental/src/sbom/endpoints/list.rs` — reference implementation for paginated list endpoint

## Acceptance Criteria
- [ ] `GET /api/v2/search` returns `PaginatedResults<SearchResultSummary>` with `items`, `total`, `offset`, and `limit` fields
- [ ] Pagination parameters `offset` and `limit` are accepted as query parameters
- [ ] Default pagination values are applied when parameters are omitted
- [ ] Total count reflects all matching results (before pagination, after filtering)
- [ ] Results within a page are ordered by relevance score (descending)

## Test Requirements
- [ ] Integration test: search with `limit=2` returns at most 2 results with correct total count
- [ ] Integration test: search with `offset=2&limit=2` returns the correct page of results
- [ ] Integration test: pagination combined with filters returns correct total and page

## Verification Commands
- `cargo test -p tests -- search --test-threads=1` — integration tests pass

## Dependencies
- Depends on: Task 2 — Add search result model types with relevance scoring (requires SearchResultSummary type)
- Depends on: Task 3 — Implement weighted full-text search ranking (requires ranked results)
- Depends on: Task 4 — Add filter query parameters to the search endpoint (pagination must compose with filters)
