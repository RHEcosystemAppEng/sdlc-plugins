## Repository
trustify-backend

## Target Branch
main

## Description
Optimize search query performance in the SearchService to reduce search response latency. The current full-text search implementation in `modules/search/src/service/mod.rs` needs query-level optimizations to improve execution time. This may include optimizing the query structure, adding appropriate database indexes, and leveraging the connection pool limiter in `common/src/db/limiter.rs` to prevent query contention.

**Assumption pending clarification:** No specific latency target or baseline measurement has been provided. This task targets demonstrable query execution time reduction through structural optimizations, without a specific SLA. The team should define performance benchmarks before and after implementation.

**Assumption pending clarification:** The scope of "search" is assumed to be the dedicated search module (`modules/search/`) and its endpoint (`GET /api/v2/search`), not the per-entity list endpoints.

## Files to Modify
- `modules/search/src/service/mod.rs` — optimize query construction and execution in SearchService
- `common/src/db/query.rs` — review and optimize shared query builder helpers used by search
- `tests/api/search.rs` — add performance-oriented integration tests

## Files to Create
- `migration/src/m0002_search_indexes/mod.rs` — add database indexes to improve search query performance (if profiling confirms index-based optimization is needed)

## API Changes
- `GET /api/v2/search` — MODIFY: no contract change, but response latency should decrease

## Implementation Notes
- Inspect the current `SearchService` implementation in `modules/search/src/service/mod.rs` to identify query patterns that can be optimized (e.g., unnecessary joins, missing indexes, unoptimized full-text search queries).
- Review `common/src/db/query.rs` for shared query builder patterns — any optimization here benefits all modules that use shared filtering and pagination.
- Check `common/src/db/limiter.rs` for connection pool configuration that may affect query concurrency under load.
- If database indexes are added, follow the migration pattern established in `migration/src/m0001_initial/mod.rs`.
- Use SeaORM query profiling or `EXPLAIN ANALYZE` to identify slow query patterns before and after optimization.

Per CONVENTIONS.md (Key Conventions) - Error handling: all handlers must return `Result<T, AppError>` with `.context()` wrapping. Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's Rust handler file scope.

Per CONVENTIONS.md (Key Conventions) - Query helpers: use shared filtering, pagination, and sorting via `common/src/db/query.rs`. Applies: task modifies `common/src/db/query.rs` matching the convention's query helper scope.

Per CONVENTIONS.md (Key Conventions) - Testing: integration tests in `tests/api/` hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern. Applies: task modifies `tests/api/search.rs` matching the convention's test file scope.

## Reuse Candidates
- `common/src/db/query.rs::query builder helpers` — shared filtering, pagination, and sorting logic that the search service should leverage rather than implementing custom query construction
- `common/src/db/limiter.rs::connection pool limiter` — existing connection management that may be tuned for search workload

## Acceptance Criteria
- [ ] Search query execution time is measurably reduced (demonstrate with before/after query profiling)
- [ ] Existing search functionality is not broken (all existing search integration tests pass)
- [ ] Any new database indexes are added via a proper migration
- [ ] Error handling follows the `Result<T, AppError>` pattern with `.context()` wrapping

## Test Requirements
- [ ] Existing search integration tests in `tests/api/search.rs` continue to pass
- [ ] New integration test verifying that search returns results within an acceptable time frame for a representative dataset
- [ ] If indexes are added, verify the migration applies and rolls back cleanly

## Verification Commands
- `cargo test --test search` — run search integration tests, expected: all pass
- `cargo build` — verify compilation, expected: success with no errors

## Dependencies
- None
