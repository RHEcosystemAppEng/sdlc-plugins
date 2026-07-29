## Repository
trustify-backend

## Target Branch
main

## Description
Optimize search query performance and add response caching to the search endpoint to reduce latency for repeated queries. Currently, the search endpoint is reported as slow by users. This task adds HTTP-level response caching using the existing tower-http caching middleware and optimizes the SearchService query patterns to reduce database round-trips.

This addresses the Feature TC-9002 MVP requirement "Search should be faster — currently too slow" and the NFR "Should be fast enough." The Feature description does not specify quantifiable performance targets; this task implements standard optimization techniques (caching, query optimization) as a baseline. The feature owner should define specific latency targets for validation.

## Files to Modify
- `modules/search/endpoints/mod.rs` — Configure tower-http caching middleware on the search route with appropriate cache-control headers (e.g., max-age for GET requests with identical query parameters); add ETag or Last-Modified support for conditional requests
- `modules/search/service/mod.rs` — Optimize search query construction to minimize database round-trips; use single-query JOINs instead of N+1 patterns if present; add query result limiting to prevent unbounded scans
- `common/src/db/limiter.rs` — Review and adjust connection pool limiter settings if search queries are contending with other operations
- `tests/api/search.rs` — Add integration tests verifying cache headers are present and that cached responses are returned for repeated identical queries

## Implementation Notes
- The codebase already uses tower-http caching middleware (per Key Conventions: "Uses tower-http caching middleware; cache configuration in endpoint route builders"). Add cache configuration to the search endpoint route builder, following the pattern used in other endpoints. Inspect existing endpoint route builders to determine the established caching pattern.
- For cache-control headers, use a short TTL (e.g., 30–60 seconds) since search data changes with ingestion. Consider using `private, max-age=30` to allow client-side caching without CDN caching.
- Add ETag support using a hash of the query parameters and the latest data modification timestamp. This enables conditional GET requests (`If-None-Match`) to return 304 Not Modified.
- In SearchService, inspect the existing query for N+1 patterns (e.g., fetching entity details in a loop after the initial search). If found, refactor to use JOINs or batch fetching.
- Add a configurable maximum result limit to prevent unbounded full-table scans. Use `common/src/db/limiter.rs` as a reference for limiting patterns.
- All handler functions must return `Result<T, AppError>` with `.context()` wrapping.
- Integration tests should verify that cache-control headers are present on search responses and that the response structure is unchanged.
- **Ambiguity note**: The Feature does not specify performance targets. This task applies standard caching and query optimization. Specific latency targets should be defined by the feature owner to enable proper validation.

## Reuse Candidates
- `common/src/db/limiter.rs` — Connection pool limiter. Review for search query pool allocation.
- `common/src/db/query.rs::query` — Shared query builder helpers. Reuse pagination and sorting helpers to ensure optimized queries use the same patterns.
- `modules/search/service/mod.rs::SearchService` — Existing search implementation. Inspect for N+1 patterns and optimization opportunities.

## Acceptance Criteria
- [ ] Search endpoint responses include appropriate cache-control headers (e.g., `Cache-Control: private, max-age=30`)
- [ ] Repeated identical search requests within the cache TTL return cached responses
- [ ] Search query execution does not exhibit N+1 query patterns (verified by query inspection or logging)
- [ ] Search queries include a maximum result limit to prevent unbounded scans
- [ ] Existing search functionality and response format are unchanged — backward compatible
- [ ] Cache is invalidated or bypassed when data is ingested (new SBOMs or advisories)

## Test Requirements
- [ ] Integration test: verify search response includes Cache-Control headers
- [ ] Integration test: verify search response format is unchanged (PaginatedResults<T> with correct structure)
- [ ] Integration test: verify search with a large dataset completes within a reasonable time (no timeout)
- [ ] Integration test: verify search results are correct after data ingestion (cache does not serve stale data indefinitely)

## Verification Commands
- `cargo test --test search -- --test-threads=1` — Run search integration tests; all tests should pass
- `cargo build` — Verify the project compiles without errors after changes

## Dependencies
- No dependencies on other tasks
