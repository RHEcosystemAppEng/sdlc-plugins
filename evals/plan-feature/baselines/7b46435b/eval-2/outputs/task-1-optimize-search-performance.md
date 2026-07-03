## Repository
trustify-backend

## Target Branch
main

## Description
Optimize the search query execution in SearchService to improve response times for GET /api/v2/search. The current full-text search implementation has been reported as slow. Investigate and optimize the search queries, add database indexes if needed, and consider implementing query result caching using the existing tower-http caching middleware.

Note: The Feature description does not specify a performance baseline or target. Implementers should measure current p95 latency before optimization and document the improvement achieved.

## Files to Modify
- `modules/search/src/service/mod.rs` — optimize SearchService full-text search query execution, add index hints or query restructuring
- `common/src/db/query.rs` — add or optimize shared query builder helpers for search performance (e.g., query plan hints, batch fetching)

## Implementation Notes
- Follow existing service patterns in `modules/fundamental/src/sbom/service/sbom.rs` for query structure and error handling
- Use the existing tower-http caching middleware configuration for endpoint-level response caching where appropriate
- Consider PostgreSQL full-text search optimizations: GIN/GiST indexes on text columns, `ts_rank` for pre-computed ranking, materialized views for frequently queried data
- Reuse shared query builder helpers from `common/src/db/query.rs` for pagination and sorting — do not duplicate existing helpers
- Per CONVENTIONS.md §Error Handling: use `Result<T, AppError>` with `.context()` wrapping for all service methods. Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's .rs file scope.
- Per CONVENTIONS.md §Query Helpers: use shared filtering, pagination, and sorting via `common/src/db/query.rs`. Applies: task modifies `common/src/db/query.rs` matching the convention's query builder scope.
- Per CONVENTIONS.md §Testing: add integration tests in `tests/api/` following the existing `assert_eq!(resp.status(), StatusCode::OK)` pattern. Applies: task modifies `tests/api/search.rs` matching the convention's test file scope.

## Reuse Candidates
- `common/src/db/query.rs::query` — shared query builder helpers for filtering, pagination, and sorting; extend rather than duplicate
- `common/src/db/limiter.rs::limiter` — connection pool limiter; relevant if connection pooling is a performance bottleneck
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — example of optimized service query patterns to follow

## Acceptance Criteria
- [ ] Search endpoint (GET /api/v2/search) response times are measurably improved over the pre-optimization baseline
- [ ] Existing search functionality returns the same results as before optimization
- [ ] All existing integration tests in `tests/api/search.rs` pass without modification
- [ ] No regressions in other endpoints that share `common/src/db/query.rs`

## Test Requirements
- [ ] Add performance-focused integration test to `tests/api/search.rs` verifying search completes within acceptable time bounds
- [ ] Verify existing search test cases continue to pass with identical results
- [ ] If database indexes are added, verify they are created by the migration and used by the query planner

## Verification Commands
- `cargo test --test search` — run search integration tests and verify all pass

## Dependencies
- None
