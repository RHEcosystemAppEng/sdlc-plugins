## Repository
trustify-backend

## Target Branch
main

## Description
Refactor the SearchService to use PostgreSQL full-text search queries (`tsquery`/`tsvector`) instead of LIKE/ILIKE patterns for improved search relevance and performance. This task changes the search query construction to leverage the GIN-indexed tsvector columns added in Task 1.

**Assumption (pending clarification):** "More relevant results" means using PostgreSQL `ts_rank` for ranking and `plainto_tsquery` or `websearch_to_tsquery` for query parsing. Exact ranking weights and query parsing strategy need stakeholder validation.

## Files to Modify
- `modules/search/src/service/mod.rs` — refactor `SearchService` query methods to use `tsvector` matching and `ts_rank` ordering instead of LIKE/ILIKE
- `modules/search/src/endpoints/mod.rs` — update the `GET /api/v2/search` handler to pass the query string to the refactored service

## Implementation Notes
- The existing `SearchService` in `modules/search/src/service/mod.rs` currently performs search across entities. Refactor its query construction to use `to_tsquery` or `websearch_to_tsquery` against the `search_vector` column.
- Use `ts_rank(search_vector, query)` to order results by relevance score. Include the rank score in the response so consumers can assess match quality.
- Reuse the shared query builder helpers in `common/src/db/query.rs` for pagination and sorting — extend them if needed to support `ts_rank`-based ordering.
- Wrap results in `PaginatedResults<T>` from `common/src/model/paginated.rs` as per the existing response pattern.
- All handlers should return `Result<T, AppError>` with `.context()` wrapping, consistent with the error handling pattern in `common/src/error.rs`.
- **Assumption (pending clarification):** Use `websearch_to_tsquery` to support natural language queries (AND/OR/NOT operators). If exact phrase matching is required, this may need `phraseto_tsquery`.
- Per CONVENTIONS.md §Error Handling: use `Result<T, AppError>` with `.context()` wrapping for all service methods.
  Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's Rust source file scope.

## Reuse Candidates
- `common/src/db/query.rs::QueryBuilder` — shared query builder with filtering, pagination, and sorting helpers that can be extended for full-text search ranking
- `common/src/model/paginated.rs::PaginatedResults` — response wrapper used by all list endpoints

## Acceptance Criteria
- [ ] SearchService uses `tsvector`/`tsquery` matching instead of LIKE/ILIKE
- [ ] Search results are ordered by relevance score (`ts_rank`)
- [ ] Existing search endpoint contract is preserved (same path, compatible response shape)
- [ ] Search queries that previously returned results continue to return results (no regression)

## Test Requirements
- [ ] Full-text search returns results matching title/name fields
- [ ] Full-text search returns results matching description fields
- [ ] Results are ordered by relevance (exact title matches ranked higher than description matches)
- [ ] Empty search query returns an appropriate response (not an error)
- [ ] Special characters in search query do not cause errors

## Dependencies
- Depends on: Task 1 — Add full-text search indexes (requires tsvector columns to exist)
