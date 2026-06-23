## Repository
trustify-backend

## Target Branch
main

## Description
Add full-text search ranking to the search service so that results are ordered by relevance instead of insertion order. The current SearchService in `modules/search/src/service/mod.rs` performs basic text matching. This task adds PostgreSQL ts_rank-based scoring to improve result relevance.

**Assumption pending clarification**: "Results should be more relevant" is interpreted as adding ts_rank-based full-text search scoring. The feature description does not define what "relevant" means, so we assume ordering by PostgreSQL full-text match quality is the intended improvement.

## Files to Modify
- `modules/search/src/service/mod.rs` -- Refactor SearchService to use PostgreSQL ts_vector/ts_query with ts_rank for relevance scoring; integrate SearchFilter for filtering; return SearchResultItem with relevance_score populated
- `common/src/db/query.rs` -- Add full-text search query builder helper function that constructs ts_vector queries with ts_rank ordering

## Implementation Notes
The existing `SearchService` in `modules/search/src/service/mod.rs` currently performs full-text search across entities. Modify it to use PostgreSQL's `to_tsvector` and `to_tsquery` functions with `ts_rank` for relevance scoring.

Add a new helper function in `common/src/db/query.rs` alongside the existing shared query builder helpers (filtering, pagination, sorting) to construct full-text search queries. This follows the pattern of keeping shared query logic in the common crate.

Per CONVENTIONS.md §Query helpers: use shared filtering, pagination, and sorting via `common/src/db/query.rs`.
Applies: task modifies `common/src/db/query.rs` matching the convention's `.rs` file scope.

Per CONVENTIONS.md §Error handling: all handlers return `Result<T, AppError>` with `.context()` wrapping.
Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's `.rs` file scope.

Per CONVENTIONS.md §Framework: use SeaORM for database queries.
Applies: convention has no file-type restriction (broadly applicable).

Reference the existing query patterns in `common/src/db/query.rs` for building filtered/sorted queries. The `AppError` enum in `common/src/error.rs` should be used for error wrapping.

## Reuse Candidates
- `common/src/db/query.rs` -- existing query builder helpers for filtering, pagination, sorting; extend with full-text search helper
- `common/src/error.rs::AppError` -- error type for `.context()` wrapping in service methods

## Dependencies
- Depends on: Task 1 -- Define search filter model types (requires SearchFilter and SearchResultItem types)

## Acceptance Criteria
- [ ] SearchService uses PostgreSQL ts_rank for relevance scoring
- [ ] Search results are ordered by relevance score (highest first)
- [ ] SearchFilter is applied to narrow results when filter fields are provided
- [ ] A reusable full-text search query helper is added to `common/src/db/query.rs`
- [ ] All optional filter fields are handled (None means no filter applied)
- [ ] **Assumption pending clarification**: ts_rank-based ordering satisfies the "more relevant results" requirement

## Test Requirements
- [ ] Integration test that search results with a specific term rank higher than partial matches
- [ ] Integration test that search with no filters returns all results ordered by relevance
- [ ] Integration test that search with entity_type filter returns only matching entity types

[sdlc-workflow] Description digest: sha256-md:e06d157e5c134d9c41c123f160082b90b18a04708e7be5338eb87443f36a3401
