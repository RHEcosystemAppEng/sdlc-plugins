## Repository
trustify-backend

## Target Branch
main

## Description
Optimize search query performance to address the "Search should be faster" requirement. This task focuses on query-level optimizations beyond the full-text search indexes added in Task 1: query plan analysis, connection pool tuning, and caching configuration for the search endpoint.

**Assumption (pending clarification):** The feature description provides no performance baseline or target. This task assumes P95 search latency should be under 500ms. Without production metrics, optimization focuses on common performance bottlenecks: missing indexes on frequently filtered columns, unoptimized query plans, and lack of HTTP-level caching for repeated queries.

**Assumption (pending clarification):** The scale of data is unknown. Optimizations target moderate scale (tens of thousands of entities). If the dataset is significantly larger, additional strategies (materialized views, dedicated search engine like Elasticsearch) may be needed — those are out of scope for this task.

## Files to Modify
- `modules/search/src/service/mod.rs` — optimize query construction to avoid N+1 queries, use eager joins, and ensure efficient query plans for filtered full-text search
- `modules/search/src/endpoints/mod.rs` — add HTTP caching headers (Cache-Control) for search results using the existing `tower-http` caching middleware pattern
- `common/src/db/limiter.rs` — review and tune connection pool limits if search queries are contending with other requests

## Implementation Notes
- The existing codebase uses `tower-http` caching middleware (per Key Conventions in the repo manifest) — configure appropriate cache TTL for search results in the endpoint route builder
- Use `EXPLAIN ANALYZE` during development to verify query plans use the GIN indexes from Task 1 rather than sequential scans
- In `SearchService`, ensure that multi-entity search (querying sbom + advisory + package tables) uses UNION ALL with individual index scans rather than joining all tables in a single query, to allow PostgreSQL to use indexes efficiently
- Review `common/src/db/limiter.rs` for connection pool configuration — search queries should not monopolize the pool
- Follow the error handling pattern from `common/src/error.rs` — all handlers return `Result<T, AppError>` with `.context()` wrapping
- Consider adding a query timeout to prevent long-running searches from blocking the connection pool — this can be done via PostgreSQL `statement_timeout` set on the search query connection

## Reuse Candidates
- `common/src/db/query.rs` — existing query builder helpers that should be used for constructing optimized queries
- `common/src/db/limiter.rs` — existing connection pool limiter that may need tuning for search workloads
- `modules/fundamental/src/sbom/endpoints/mod.rs` — example of route registration with `tower-http` caching middleware configuration

## Acceptance Criteria
- [ ] Search queries use GIN indexes (verified via EXPLAIN ANALYZE showing Index Scan, not Seq Scan)
- [ ] Multi-entity search does not produce N+1 query patterns
- [ ] HTTP caching headers are present on search responses (Cache-Control with appropriate TTL)
- [ ] Search endpoint responds within 500ms for typical queries against test data (P95 target)
- [ ] Connection pool is not exhausted under concurrent search requests
- [ ] All existing integration tests continue to pass

## Test Requirements
- [ ] Integration test: verify search response includes Cache-Control header
- [ ] Integration test: verify search responds within acceptable time for a dataset of representative size
- [ ] Integration test: concurrent search requests do not cause connection pool exhaustion or timeouts
- [ ] Regression: all existing tests in `tests/api/sbom.rs`, `tests/api/advisory.rs`, and `tests/api/search.rs` pass

## Verification Commands
- `EXPLAIN ANALYZE SELECT ... FROM sbom WHERE tsvector_column @@ to_tsquery('test')` — expected: Index Scan using GIN index, not Seq Scan
- `cargo test --test api` — expected: all integration tests pass

## Dependencies
- Depends on: Task 1 — Add full-text search indexes (indexes must be in place to verify query plans)
- Depends on: Task 2 — Refactor search relevance ranking (optimizations apply to the refactored search queries)

[sdlc-workflow] Description digest: sha256:a50376559312b97719fc7aceb54be98ac8a85d57b9bf1300f4f888fe2b821563
