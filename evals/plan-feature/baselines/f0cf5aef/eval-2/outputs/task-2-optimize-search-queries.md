# Task 2 — Optimize SearchService query execution

## Repository
trustify-backend

## Target Branch
main

## Description
Optimize the SearchService query execution to improve search response time. The current SearchService (`modules/search/src/service/mod.rs`) performs full-text search across multiple entity types (SBOMs, advisories, packages), but the query structure may not be optimal for PostgreSQL's full-text search capabilities. This task focuses on query-level optimizations: using PostgreSQL `tsvector`/`tsquery` for full-text search instead of LIKE/ILIKE patterns, adding result-count limiting before joins, and leveraging connection pool settings.

This addresses the "Search should be faster" requirement from TC-9002. Note: the feature does not specify quantified performance targets, so this task focuses on standard query optimization patterns.

## Files to Modify
- `modules/search/src/service/mod.rs` — Optimize search query construction: use `tsvector`/`tsquery` for full-text matching, add early result limiting, optimize join order
- `common/src/db/limiter.rs` — Review and adjust connection pool limiter settings for search-heavy workloads if needed

## Implementation Notes
- Replace any LIKE/ILIKE-based text matching with PostgreSQL full-text search operators (`@@`, `to_tsvector`, `to_tsquery`)
- Apply result limiting early in the query pipeline (before joins) to reduce intermediate result set sizes
- Use `EXPLAIN ANALYZE` during development to verify query plan improvements
- Ensure the query builder uses the shared helpers in `common/src/db/query.rs` for pagination
- Per CONVENTIONS.md §Error handling: all service methods must return `Result<T, AppError>` with `.context()` wrapping for error messages.
  Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's Rust source file scope.
- Per CONVENTIONS.md §Response types: search results must be returned via `PaginatedResults<T>` from `common/src/model/paginated.rs`.
  Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's Rust source file scope.
- Per CONVENTIONS.md §Query helpers: use shared filtering, pagination, and sorting from `common/src/db/query.rs` rather than implementing custom query logic.
  Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's Rust source file scope.

## Reuse Candidates
- `common/src/db/query.rs` — Shared query builder helpers for filtering, pagination, and sorting; extend these for full-text search rather than implementing standalone query logic in the search service
- `common/src/model/paginated.rs` — PaginatedResults<T> response wrapper; search results must use this type
- `common/src/db/limiter.rs` — Connection pool limiter; review settings for compatibility with optimized queries
- `modules/fundamental/src/advisory/service/advisory.rs` — AdvisoryService implements search functionality; reference for query patterns used elsewhere in the codebase

## Acceptance Criteria
- [ ] SearchService uses PostgreSQL full-text search operators (`tsvector`/`tsquery`) instead of LIKE/ILIKE patterns (if applicable)
- [ ] Search queries apply result limiting before expensive joins
- [ ] Search results remain correct — same results returned for the same query inputs (ordering may change)
- [ ] Error handling follows `Result<T, AppError>` with `.context()` pattern
- [ ] Search endpoint response time is improved for representative queries (measured via manual testing)

## Test Requirements
- [ ] Existing search integration tests in `tests/api/search.rs` continue to pass
- [ ] Search returns correct results for single-word queries
- [ ] Search returns correct results for multi-word queries
- [ ] Search returns empty results for queries with no matches (no errors)
- [ ] Pagination works correctly with optimized queries

## Verification Commands
- `cargo test --test search` — All existing search tests pass
- `cargo run` followed by `curl http://localhost:8080/api/v2/search?q=test` — Search endpoint returns valid results

## Dependencies
- Depends on: Task 1 — Add database indexes for search-relevant columns (indexes should be in place for optimized queries to benefit from them)
