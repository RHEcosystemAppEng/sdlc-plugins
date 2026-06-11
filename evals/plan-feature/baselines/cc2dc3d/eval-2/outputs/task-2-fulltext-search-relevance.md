## Repository
trustify-backend

## Target Branch
main

## Description
Implement PostgreSQL full-text search with relevance ranking in the SearchService to replace naive text matching. The current search returns "irrelevant results" (TC-9002). This task upgrades the search service to use `tsvector`/`tsquery` with `ts_rank` scoring so results are ordered by relevance rather than insertion order.

**Assumption (pending clarification):** No domain-specific relevance model was specified. Using PostgreSQL `ts_rank` with default weights is a reasonable baseline. The ranking strategy can be refined once stakeholders define what "relevant" means for their use cases.

## Files to Modify
- `modules/search/src/service/mod.rs` — refactor `SearchService` to use PostgreSQL full-text search (`to_tsquery`, `ts_rank`) instead of LIKE/ILIKE pattern matching; order results by relevance score
- `modules/search/src/endpoints/mod.rs` — update the `GET /api/v2/search` handler to accept an optional `sort_by=relevance` parameter (default when a search query is provided) and pass it to the service layer
- `common/src/db/query.rs` — add a full-text search helper function that builds tsquery expressions from user input, handling multi-word queries and special characters

## API Changes
- `GET /api/v2/search` — MODIFY: add optional `sort_by` query parameter (values: `relevance`, `date`, `name`; default: `relevance` when `q` is provided). Response now includes a `score` field in each result item representing the relevance rank.

## Implementation Notes
- The existing `SearchService` in `modules/search/src/service/mod.rs` provides full-text search across entities. Refactor it to use PostgreSQL's `to_tsvector` and `to_tsquery` functions with `ts_rank` for scoring.
- Use `plainto_tsquery` for simple user input (handles whitespace-separated terms) and `websearch_to_tsquery` if available for more natural query syntax.
- The `common/src/db/query.rs` module already contains shared query builder helpers for filtering, pagination, and sorting. Add a new helper function (e.g., `build_fulltext_query`) that constructs the tsquery expression and rank ordering clause.
- Follow the existing module pattern: the service layer in `modules/search/src/service/mod.rs` handles business logic, the endpoint in `modules/search/src/endpoints/mod.rs` handles HTTP concerns.
- All handlers must return `Result<T, AppError>` with `.context()` wrapping per the repository's error handling convention.
- Results should continue to use `PaginatedResults<T>` from `common/src/model/paginated.rs` for consistency with other list endpoints.
- This task depends on the `search_vector` columns and GIN indexes created in Task 1 for optimal performance. However, the full-text search can be implemented using `to_tsvector()` on the fly if the indexes are not yet available — it will just be slower.

## Reuse Candidates
- `common/src/db/query.rs` — shared query builder helpers (filtering, pagination, sorting) to extend with full-text search support
- `common/src/model/paginated.rs` — `PaginatedResults<T>` response wrapper to reuse for search results
- `modules/search/src/service/mod.rs` — existing `SearchService` implementation to refactor rather than rewrite
- `common/src/error.rs` — `AppError` enum for consistent error handling

## Acceptance Criteria
- [ ] Search queries use PostgreSQL full-text search (`tsquery`/`tsvector`) instead of LIKE/ILIKE
- [ ] Results are ranked by relevance score using `ts_rank`
- [ ] The `GET /api/v2/search` endpoint accepts a `sort_by` parameter
- [ ] Multi-word search queries return results matching all terms
- [ ] Search results include a relevance score field
- [ ] Existing search functionality is not broken (backward compatible)

## Test Requirements
- [ ] Integration test: search for a known term returns the expected entity as the top result
- [ ] Integration test: multi-word query returns results matching all terms, ranked by relevance
- [ ] Integration test: `sort_by=relevance` orders results by ts_rank score descending
- [ ] Integration test: `sort_by=date` orders results by creation date descending
- [ ] Integration test: empty search query returns all results (no tsquery applied)
- [ ] Integration test: special characters in search query are handled gracefully (no SQL injection, no crash)
- [ ] Add tests in `tests/api/search.rs` following the existing `assert_eq!(resp.status(), StatusCode::OK)` pattern

## Verification Commands
- `cargo test --test search` — search-specific integration tests pass
- `cargo test` — all tests pass without regression

## Documentation Updates
- `README.md` — document the new `sort_by` query parameter for the search endpoint

## Dependencies
- Depends on: Task 1 — Add database indexes for search performance (for optimal performance, though functional without it)
