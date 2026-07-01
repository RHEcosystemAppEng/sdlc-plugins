# Task 4 — Optimize search query performance

## Repository
trustify-backend

## Target Branch
main

## Description
Optimize the search query execution path in `SearchService` to improve response times. This task addresses the "search should be faster" requirement by tuning the database queries, ensuring the GIN indexes from Task 1 are used effectively, and adding connection pool and caching considerations for the search endpoint.

**Ambiguity note:** The feature description does not provide current baseline latency or target performance goals ("Should be fast enough" is the only NFR). This task focuses on structural optimizations (index utilization, query plan efficiency, caching headers) that are universally beneficial. Quantified performance targets should be established by the product owner and validated via load testing after these changes land.

## Files to Modify
- `modules/search/src/service/mod.rs` — optimize query construction to ensure GIN index utilization; add query plan hints if needed
- `modules/search/src/endpoints/mod.rs` — add cache-control headers for search results using tower-http caching middleware; add request timeout for long-running search queries

## Implementation Notes
- Ensure search queries use the tsvector columns (from Task 1) with `@@` operator so PostgreSQL's query planner selects the GIN index. Avoid patterns that prevent index usage (e.g., wrapping the indexed column in a function call).
- Consider adding `LIMIT` pushdown to the database query rather than fetching all results and paginating in application code. The existing `PaginatedResults<T>` pattern in `common/src/model/paginated.rs` should already support this — verify and fix if needed.
- Add HTTP cache-control headers for search responses using `tower-http` caching middleware, following the pattern described in the Key Conventions section ("Uses tower-http caching middleware; cache configuration in endpoint route builders").
- Consider adding a query timeout via SeaORM's `DatabaseConnection::execute` timeout option or Axum middleware to prevent long-running queries from consuming connection pool slots (see `common/src/db/limiter.rs` for the connection pool limiter).
- Use `EXPLAIN ANALYZE` during development to verify that search queries hit the GIN index and not sequential scans.
- Per CONVENTIONS.md: follow the established error handling pattern with `Result<T, AppError>` and `.context()` wrapping for any new error paths.
  Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's Rust module scope.

## Reuse Candidates
- `common/src/db/limiter.rs` — connection pool limiter; understand its configuration to ensure search queries do not exhaust the pool
- `common/src/db/query.rs` — shared query builder; check for existing pagination pushdown patterns
- `common/src/model/paginated.rs` — `PaginatedResults<T>` may already implement efficient pagination

## Acceptance Criteria
- [ ] Search queries utilize the GIN indexes (verified via EXPLAIN ANALYZE showing index scan, not sequential scan)
- [ ] Pagination is pushed down to the database query (LIMIT/OFFSET in SQL) rather than fetching all results
- [ ] Search endpoint responses include appropriate cache-control headers
- [ ] Long-running search queries are bounded by a timeout to prevent connection pool exhaustion
- [ ] Existing search functionality is not broken by optimizations

## Test Requirements
- [ ] Integration test: search queries return correct results after optimization (no regression)
- [ ] Integration test: paginated search returns the correct subset of results
- [ ] Integration test: search responses include cache-control headers
- [ ] Tests added in `tests/api/search.rs` following the existing test pattern

## Verification Commands
- `cargo test -p search` — search module tests pass
- `cargo test --test search` — search integration tests pass

## Dependencies
- Depends on: Task 1 — Add full-text search indexes via database migration
- Depends on: Task 2 — Add relevance scoring to SearchService
