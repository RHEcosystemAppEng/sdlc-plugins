## Repository
trustify-backend

## Target Branch
main

## Description
Implement PostgreSQL full-text search with relevance ranking in the SearchService to replace or enhance the current search implementation. This task upgrades the search query logic to use PostgreSQL's `tsvector`/`tsquery` with `ts_rank` scoring so that results are ordered by relevance to the search terms. This addresses the requirement that "results should be more relevant."

**Assumption (pending clarification):** The feature states results should be "more relevant" but provides no definition of relevance, no ranking criteria, and no examples of good vs. bad results. This task assumes that PostgreSQL full-text search ranking via `ts_rank` is an acceptable relevance strategy. The ranking weights (e.g., title matches weighted higher than description matches) should be confirmed with the product owner.

**Assumption (pending clarification):** The current SearchService in `modules/search/src/service/mod.rs` uses basic string matching or LIKE queries. This task assumes replacing that with tsvector/tsquery-based full-text search is the correct approach. Alternative search backends (e.g., Elasticsearch) are not considered without explicit direction.

## Files to Modify
- `modules/search/src/service/mod.rs` — Rewrite search queries to use PostgreSQL full-text search with `tsvector`/`tsquery` and `ts_rank` for relevance-based ordering
- `modules/search/src/endpoints/mod.rs` — Update the GET /api/v2/search endpoint response to include a relevance score field in results

## Implementation Notes
Modify `SearchService` in `modules/search/src/service/mod.rs` to construct queries using `to_tsvector('english', column) @@ to_tsquery('english', :query)` with `ts_rank` for ordering. The search should span SBOM, advisory, and package entities, matching the cross-entity search pattern already in the service. Use the query builder helpers from `common/src/db/query.rs` for pagination and sorting integration. Wrap search results in `PaginatedResults<T>` from `common/src/model/paginated.rs` to maintain the established response pattern. All handler return types should use `Result<T, AppError>` with `.context()` wrapping per the error handling convention.

Per CONVENTIONS.md §Error Handling: return `Result<T, AppError>` with `.context()` wrapping in service methods. Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's Rust file scope.

Per CONVENTIONS.md §Response Types: wrap list results in `PaginatedResults<T>`. Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's Rust file scope.

Per CONVENTIONS.md §Query Helpers: use shared query builder for pagination and sorting. Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's Rust file scope.

## Reuse Candidates
- `common/src/db/query.rs::Query` — Shared query builder with filtering, pagination, and sorting helpers; reuse for integrating full-text search with existing pagination
- `common/src/model/paginated.rs::PaginatedResults` — Response wrapper for paginated list endpoints; reuse for search result responses

## Acceptance Criteria
- [ ] SearchService uses PostgreSQL full-text search with `tsvector`/`tsquery` instead of basic string matching
- [ ] Search results are ordered by relevance score using `ts_rank`
- [ ] Search spans SBOM, advisory, and package entities as before
- [ ] Search response includes a relevance score for each result
- [ ] Results for exact matches rank higher than partial matches
- [ ] Existing search API contract (GET /api/v2/search) is preserved (backward compatible)

## Test Requirements
- [ ] Integration test verifying that exact title matches rank higher than partial description matches
- [ ] Integration test verifying that multi-word queries return correctly ranked results
- [ ] Integration test verifying that search across entity types (SBOM, advisory, package) returns combined ranked results
- [ ] Existing search tests in `tests/api/search.rs` continue to pass
- [ ] Edge case: empty query returns no results or all results (define expected behavior)

## Dependencies
- Depends on: Task 1 — Add database indexes for search performance (GIN indexes must exist for full-text search to perform well)
