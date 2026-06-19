## Repository
trustify-backend

## Target Branch
main

## Description
Enhance the SearchService to use PostgreSQL full-text search ranking (`ts_rank`) for relevance-based result ordering. This addresses the "results should be more relevant" requirement from TC-9002 by replacing any existing naive text matching (e.g., `LIKE`/`ILIKE`) with ranked full-text search.

**Ambiguity note:** The feature does not define what "relevant" means. This task assumes relevance equals PostgreSQL `ts_rank` score based on text match quality against the search query. Results are ordered by rank descending (best match first). No user-configurable ranking weights or boosting is implemented. This assumption is pending clarification with stakeholders.

## Files to Modify
- `modules/search/src/service/mod.rs` — Replace existing text matching logic with `ts_rank`-based full-text search queries; order results by relevance score descending
- `common/src/db/query.rs` — Add shared full-text search query builder helpers (`to_tsquery`, `ts_rank` wrappers) that can be reused by other modules

## Implementation Notes
Inspect `modules/search/src/service/mod.rs` to understand the current search implementation. The SearchService likely performs text matching across multiple entity types (SBOMs, advisories, packages). Replace the current approach with:

1. Convert user search input to a `tsquery` using `plainto_tsquery` or `websearch_to_tsquery`
2. Match against the `tsvector` columns/indexes created in Task 1
3. Rank results using `ts_rank(search_vector, query)` and order by rank descending
4. Preserve the existing `PaginatedResults<T>` response format from `common/src/model/paginated.rs`

Add reusable full-text search helpers to `common/src/db/query.rs` alongside the existing filtering, pagination, and sorting utilities so that individual module services (SBOM, advisory, package) can also adopt full-text search in the future.

Per CONVENTIONS.md §Error handling: all service methods must return `Result<T, AppError>` with `.context()` wrapping on database errors. Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's `.rs` scope.

Per CONVENTIONS.md §Response types: search results must continue to use `PaginatedResults<T>` from `common/src/model/paginated.rs`. Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's `.rs` scope.

Per CONVENTIONS.md §Query helpers: new full-text search helpers belong in `common/src/db/query.rs` alongside existing shared query utilities. Applies: task modifies `common/src/db/query.rs` matching the convention's `.rs` scope.

## Reuse Candidates
- `common/src/db/query.rs` — existing filtering, pagination, and sorting helpers; extend with full-text search utilities rather than duplicating query builder patterns
- `common/src/model/paginated.rs::PaginatedResults<T>` — response wrapper that must be used for search results
- `common/src/error.rs::AppError` — error type for service method return types

## Acceptance Criteria
- [ ] SearchService uses PostgreSQL full-text search (`ts_rank`) for result ranking
- [ ] Results are ordered by relevance score descending (best match first)
- [ ] Empty or whitespace-only search queries return an appropriate error or empty result set
- [ ] Response format remains `PaginatedResults<T>` — backward compatible with existing consumers
- [ ] Full-text search query helpers are added to `common/src/db/query.rs` for reuse

## Test Requirements
- [ ] Search for a known term returns matching results ordered by relevance
- [ ] Search for a term that matches multiple entities ranks exact matches higher than partial matches
- [ ] Empty search query is handled gracefully (error response or empty result)
- [ ] Pagination continues to work correctly with ranked results

## Dependencies
- Depends on: Task 1 — Search indexes (full-text search indexes must exist for `ts_rank` to be effective)
