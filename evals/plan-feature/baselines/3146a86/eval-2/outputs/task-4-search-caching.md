# Task 4 — Add response caching to the search endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Implement HTTP response caching for the search endpoint using the project's existing
`tower-http` caching middleware. Repeated identical search queries should be served from
cache to reduce database load and improve response times. This addresses the "search should
be faster" requirement by avoiding redundant query execution for commonly repeated searches.

## Files to Modify
- `modules/search/src/endpoints/mod.rs` — add `tower-http` caching middleware configuration to the search route builder; set appropriate cache TTL and vary headers based on query parameters
- `server/src/main.rs` — verify the caching middleware is mounted for the search module routes (if not already configured globally)

## Implementation Notes
- The project already uses `tower-http` caching middleware — see the route builders in other endpoint modules for the established pattern (check `modules/fundamental/src/sbom/endpoints/mod.rs` or `modules/fundamental/src/advisory/endpoints/mod.rs` for cache configuration examples)
- Set `Cache-Control` with a short TTL (e.g., 60 seconds) since search indexes may change with new data ingestion
- Use `Vary` header to include query parameters (`q`, `type`, `severity`, `date_from`, `date_to`, `offset`, `limit`) so different search queries are cached separately
- Cache invalidation: the short TTL provides eventual consistency; explicit invalidation is out of scope for this task
- Do not cache error responses (4xx, 5xx)

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration with caching middleware pattern
- `modules/fundamental/src/advisory/endpoints/mod.rs` — another example of route-level cache configuration

## Acceptance Criteria
- [ ] Repeated identical search queries are served from cache (verified by checking response headers)
- [ ] Different query parameters produce separate cache entries (Vary header correctly configured)
- [ ] Cache TTL is set to a reasonable short duration (60s or similar)
- [ ] Error responses are not cached
- [ ] Cache does not break pagination — different offset/limit values return different cached results

## Test Requirements
- [ ] Integration test: verify `Cache-Control` header is present in search responses
- [ ] Integration test: verify repeated identical requests return consistent results
- [ ] Verify existing search tests in `tests/api/search.rs` still pass with caching enabled

## Verification Commands
- `cargo test -p tests --test search` — search integration tests pass

## Dependencies
- Depends on: Task 3 — Add filter support to the search endpoint
