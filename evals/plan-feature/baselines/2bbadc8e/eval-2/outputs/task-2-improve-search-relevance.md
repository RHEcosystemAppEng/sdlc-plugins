## Repository
trustify-backend

## Target Branch
main

## Description
Implement full-text search with relevance ranking using PostgreSQL's `ts_rank` scoring to improve search result ordering. Currently, search results are returned without meaningful relevance ordering, making it difficult for users to find the most pertinent results. This task integrates PostgreSQL full-text search ranking into the SearchService so results are ordered by text match quality.

**Assumption pending clarification:** The Feature description states results should be "more relevant" but does not define relevance criteria (text match quality vs. recency vs. severity vs. combined scoring). This task assumes relevance means text match quality using PostgreSQL `ts_rank` scoring. If a different ranking strategy is needed (e.g., weighted by entity type, boosted by recency, or combined multi-factor scoring), the ranking algorithm should be revisited after clarification.

## Files to Modify
- `modules/search/src/service/mod.rs` — Add ts_rank-based result scoring and ordering to search queries
- `modules/search/src/endpoints/mod.rs` — Update the search endpoint handler to return results ordered by relevance score
- `common/src/model/paginated.rs` — Extend PaginatedResults<T> to optionally include a relevance score field in search result items

## Implementation Notes
- Use PostgreSQL `ts_rank(tsvector_column, to_tsquery(search_term))` to compute relevance scores for each matching row. Order results by descending rank score.
- The `tsvector` columns and GIN indexes from Task 1 are prerequisites — this task builds on that infrastructure. If Task 1 is not yet merged, the ts_rank queries can still be developed against the planned column structure.
- Follow the existing `PaginatedResults<T>` pattern in `common/src/model/paginated.rs` for response wrapping. Consider adding an optional `score` or `relevance` field to search result items so consumers can display or use the ranking value.
- The `SearchService` in `modules/search/src/service/mod.rs` is the central search logic — modify its query method to include `ts_rank` in the SELECT clause and ORDER BY clause.
- Per Key Conventions: list endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs` — maintain this pattern when adding relevance-scored results.
  Applies: task modifies `common/src/model/paginated.rs` matching the convention's Rust model file scope.
- Per Key Conventions: all handlers return `Result<T, AppError>` with `.context()` wrapping — ensure relevance ranking errors are wrapped properly.
  Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's Rust endpoint file scope.

## Reuse Candidates
- `common/src/model/paginated.rs::PaginatedResults<T>` — Existing response wrapper used by all list endpoints; extend this for search results with relevance scoring rather than creating a separate response type
- `common/src/db/query.rs::query builder helpers` — Shared query construction utilities; extend for ORDER BY ts_rank integration
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — Reference service implementation showing how search and list operations are structured in this codebase

## Acceptance Criteria
- [ ] Search results are ordered by relevance score (best text matches appear first)
- [ ] The relevance score is computed using PostgreSQL ts_rank
- [ ] Search results for specific, unambiguous terms return the most relevant entity as the first result
- [ ] Existing pagination behavior is preserved — relevance ordering works correctly with offset/limit pagination
- [ ] The search API response shape remains backward-compatible (relevance score is an additive field, not a breaking change)

## Test Requirements
- [ ] Integration test verifying search results are ordered by relevance (a query matching one entity more closely than another returns the closer match first)
- [ ] Integration test verifying pagination works correctly with relevance-ordered results
- [ ] Integration test verifying that empty search queries return results in a stable default order

## Dependencies
- Depends on: Task 1 — Optimize search query performance (requires tsvector columns and GIN indexes)
