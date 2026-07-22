## Repository
trustify-backend

## Target Branch
main

## Description
Implement relevance-ranked search results in the search service and endpoint. The current `SearchService` in `modules/search/src/service/mod.rs` returns results without ranking, meaning users see results in an arbitrary order regardless of how well they match the query. This task adds PostgreSQL `ts_rank` scoring to search queries and returns results ordered by relevance, directly addressing the "results should be more relevant" requirement.

**Assumption (pending clarification):** No definition of "relevance" has been provided. This task assumes relevance is defined as PostgreSQL `ts_rank` scoring over the `tsvector` columns created in Task 1, with results ordered by descending score. If stakeholders require a different ranking algorithm (e.g., BM25, recency weighting, popularity), the approach will need revision.

**Assumption (pending clarification):** The relevance score will be included as a numeric field in the search response model. The existing `PaginatedResults<T>` wrapper from `common/src/model/paginated.rs` will be composed with a search-specific result type that includes the score, rather than modifying the shared paginated type.

## Files to Modify
- `modules/search/src/service/mod.rs` — Update search queries to use `ts_rank` for scoring and order results by relevance score descending
- `modules/search/src/endpoints/mod.rs` — Update the `GET /api/v2/search` handler to return the new response type with relevance scores

## Files to Create
- `modules/search/src/model/mod.rs` — New model module for search-specific response types
- `modules/search/src/model/search_result.rs` — `SearchResult` struct containing entity data and a `relevance_score: f32` field

## Implementation Notes
- Follow the model pattern from sibling modules (e.g., `modules/fundamental/src/sbom/model/summary.rs` for struct definition patterns, derive macros, and serde attributes).
  Applies: task creates `modules/search/src/model/search_result.rs` matching the convention's model module scope.
- Use `ts_rank(tsvector_column, plainto_tsquery('english', $query))` in the SQL query within `SearchService`. Reference the existing query builder helpers in `common/src/db/query.rs` for pagination and sorting integration.
  Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's service module scope.
- Return `PaginatedResults<SearchResult>` from the endpoint, following the response type convention used by list endpoints (e.g., `modules/fundamental/src/sbom/endpoints/list.rs`).
  Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's endpoint scope.
- The `SearchResult` struct should wrap the entity-specific summary (e.g., `SbomSummary`, `AdvisorySummary`, `PackageSummary`) with an additional `relevance_score` field, using `#[serde(flatten)]` or an enum for the entity variant.
- Error handling must follow the `Result<T, AppError>` pattern with `.context()` wrapping, consistent with `common/src/error.rs`.
- Re-export the new model module from `modules/search/src/lib.rs`.

## Acceptance Criteria
- [ ] Search results are ordered by relevance score (highest first) by default
- [ ] Each search result includes a numeric `relevance_score` field in the API response
- [ ] The `GET /api/v2/search` endpoint returns `PaginatedResults<SearchResult>` with relevance scores
- [ ] A search for a term that exactly matches an entity name ranks that entity higher than partial matches
- [ ] Empty search queries return results without errors (graceful degradation)
- [ ] Existing search functionality is not broken — all previously returned results are still returned

## Test Requirements
- [ ] Integration test in `tests/api/search.rs` verifying that results are ordered by relevance score descending
- [ ] Integration test verifying that exact-match results rank higher than partial matches
- [ ] Integration test verifying the `relevance_score` field is present in the JSON response
- [ ] Integration test verifying pagination still works correctly with ranked results

## Dependencies
- Depends on: Task 1 — Add PostgreSQL full-text search indexes for search optimization (requires tsvector columns and GIN indexes to exist for ts_rank scoring)
