## Repository
trustify-backend

## Target Branch
main

## Description
Implement relevance-ranked full-text search in the SearchService by leveraging the tsvector indexes added in Task 1. Replace the current search query logic with PostgreSQL ts_rank-based scoring so that results are ordered by relevance to the search query. This addresses the "results should be more relevant" requirement.

**Assumption pending clarification:** The relevance ranking weights are assumed to use default PostgreSQL ts_rank weights. The product owner should validate whether certain entity types or fields should receive higher weight (e.g., advisory title matches ranked above package name matches).

**Assumption pending clarification:** It is unclear whether search should return a unified result list across entity types or separate result sets per type. This task assumes a unified ranked list, matching the apparent current behavior of the single `/api/v2/search` endpoint.

## Files to Modify
- `modules/search/src/service/mod.rs` — Rewrite search query to use PostgreSQL full-text search with ts_query and ts_rank for relevance scoring
- `modules/search/src/endpoints/mod.rs` — Update endpoint to pass search terms as ts_query input; ensure response includes relevance score if applicable
- `common/src/db/query.rs` — Add full-text search query builder helpers (ts_query construction, ts_rank ordering)

## Implementation Notes
- In `common/src/db/query.rs`, add a helper function that constructs a `plainto_tsquery('english', $1)` expression and a `ts_rank(search_vector, query)` ordering clause. This helper should be reusable by any module that needs full-text search.
- In `modules/search/src/service/mod.rs`, update the `SearchService` to use the new query helpers. The search query should:
  1. Convert user input to a tsquery using `plainto_tsquery`
  2. Filter results where `search_vector @@ tsquery`
  3. Order results by `ts_rank(search_vector, tsquery) DESC`
- In `modules/search/src/endpoints/mod.rs`, the existing `GET /api/v2/search` endpoint contract should be preserved — the `q` query parameter (or equivalent) remains the search input. Add an optional `rank` field to the response items if not already present.
- All handlers must return `Result<T, AppError>` with `.context()` wrapping per project conventions.
- List endpoints should continue to return `PaginatedResults<T>` from `common/src/model/paginated.rs`.

Per CONVENTIONS.md §Error handling: all handlers return Result<T, AppError> with .context() wrapping.
Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's `.rs` endpoint file scope.

Per CONVENTIONS.md §Response types: list endpoints return PaginatedResults<T>.
Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's endpoint file scope.

Per CONVENTIONS.md §Query helpers: shared filtering, pagination, and sorting via common/src/db/query.rs.
Applies: task modifies `common/src/db/query.rs` matching the convention's query helper scope.

## Reuse Candidates
- `common/src/db/query.rs` — Existing query builder helpers for filtering, pagination, and sorting. The full-text search helpers should follow the same patterns and integrate with the existing query builder chain.
- `common/src/model/paginated.rs::PaginatedResults<T>` — Response wrapper for paginated results. Search results must use this wrapper.
- `common/src/error.rs::AppError` — Error type for endpoint handlers. All new error paths must use this.

## Acceptance Criteria
- [ ] Search queries use PostgreSQL full-text search (tsquery/tsvector) instead of previous approach
- [ ] Results are ordered by relevance score (ts_rank) descending
- [ ] The existing GET /api/v2/search endpoint contract is preserved (backward compatible)
- [ ] Empty search queries return an appropriate response (not an error)
- [ ] Search results continue to be returned as PaginatedResults
- [ ] Query helpers in common/src/db/query.rs are generic enough for reuse by other modules

## Test Requirements
- [ ] Search for a known term returns matching results ordered by relevance
- [ ] Search for a term that matches multiple entity types returns a unified ranked list
- [ ] Search for a non-existent term returns an empty result set (not an error)
- [ ] Pagination works correctly with relevance-ranked results

## Dependencies
- Depends on: Task 1 — Add full-text search indexes via database migration

[sdlc-workflow] Description digest: sha256-md:0c8a5e73770b6f95581ae83370360034ff39d6ee63033512d2c930c42f8be383
