## Repository
trustify-backend

## Target Branch
main

## Description
Implement relevance scoring in the SearchService so that search results are ranked by relevance to the query rather than returned in an arbitrary or insertion order. This addresses the "results should be more relevant" requirement by introducing a scoring mechanism that ranks results based on how closely they match the search query.

**Assumptions pending clarification:**
- Assumes relevance scoring uses PostgreSQL `ts_rank()` or `ts_rank_cd()` functions against the full-text search indexes created in Task 1
- Assumes all entity types (SBOMs, advisories, packages) use the same ranking algorithm, with no per-entity weighting specified
- Assumes the search response should include a relevance score field so consumers can understand result ordering
- Assumes exact matches should rank higher than partial matches, but no specific boosting rules are defined

## Files to Modify
- `modules/search/src/service/mod.rs` — Update `SearchService` to compute and sort by relevance scores using `ts_rank()` against full-text indexes
- `modules/search/src/endpoints/mod.rs` — Update search endpoint response to include relevance score and default sort order by score descending

## Implementation Notes
Modify the `SearchService` in `modules/search/src/service/mod.rs` to:
1. Convert the user query into a `tsquery` for PostgreSQL full-text search
2. Compute relevance scores using `ts_rank()` against the indexed `tsvector` columns
3. Order results by relevance score descending by default

Use the existing `PaginatedResults<T>` wrapper from `common/src/model/paginated.rs` for the response format. The relevance score can be added as an additional field in the search result items.

Follow the error handling pattern with `Result<T, AppError>` and `.context()` wrapping as used throughout the codebase (see `common/src/error.rs`).

Reference the query builder helpers in `common/src/db/query.rs` for existing sorting and pagination patterns that should be extended to support relevance-based ordering.

## Reuse Candidates
- `common/src/db/query.rs::query builder helpers` — Extend existing sorting logic to support relevance score ordering
- `common/src/model/paginated.rs::PaginatedResults<T>` — Use existing pagination wrapper for scored results

## Dependencies
- Depends on: Task 1 — Add full-text search indexes (requires GIN indexes to compute ts_rank)

## Acceptance Criteria
- [ ] Search results are ordered by relevance score (highest first) by default
- [ ] Relevance score is computed using PostgreSQL full-text ranking functions
- [ ] Results matching the query more closely appear before less relevant results
- [ ] Existing search functionality continues to work for all entity types (SBOMs, advisories, packages)

## Test Requirements
- [ ] Integration test in `tests/api/search.rs` verifying that a specific query returns results ordered by relevance
- [ ] Integration test confirming that an exact-match result ranks higher than a partial match
- [ ] Existing search tests continue to pass with relevance-ordered results
