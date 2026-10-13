## Repository
trustify-backend

## Target Branch
main

## Description
Add response caching to the search endpoint to reduce database load and improve response times for repeated queries. This contributes to the "search should be faster" requirement by avoiding redundant database queries for identical search requests within a short time window.

**Assumptions pending clarification:**
- Assumes cache TTL of 60 seconds as a reasonable default, since no caching requirements were specified
- Assumes caching is applied at the HTTP response level using tower-http caching middleware, consistent with the existing caching pattern in the codebase
- Assumes cache should be invalidated on query parameter changes (different search terms or filters produce different cache entries)
- Assumes an in-memory cache is acceptable for MVP (no external cache store like Redis required)

## Files to Modify
- `modules/search/src/endpoints/mod.rs` — Add tower-http `CacheControl` and caching middleware to the search route configuration

## Implementation Notes
The codebase already uses `tower-http` caching middleware (referenced in repo conventions). Apply the same caching pattern to the search endpoint routes in `modules/search/src/endpoints/mod.rs`.

Configure cache headers on the search endpoint route builder:
1. Add `Cache-Control` headers with a short `max-age` (e.g., 60 seconds) to search responses
2. Use the `tower-http` `SetResponseHeader` layer or Axum middleware to attach cache directives
3. Ensure the cache key varies by query parameters (search term, filters, pagination) so different queries are cached independently

Reference the existing route registration pattern in `modules/search/src/endpoints/mod.rs` and the `server/src/main.rs` route mounting pattern for where to attach middleware.

## Reuse Candidates
- `modules/search/src/endpoints/mod.rs` — Existing route builder where cache middleware should be added, following the same caching pattern used by other endpoints

## Acceptance Criteria
- [ ] Search endpoint responses include `Cache-Control` headers with appropriate `max-age` directive
- [ ] Repeated identical search requests within the cache window are served from cache
- [ ] Different query parameters (search terms, filters, page) produce separate cache entries
- [ ] Cache does not interfere with search correctness — new data is reflected after cache expiry

## Test Requirements
- [ ] Integration test in `tests/api/search.rs` verifying search responses include `Cache-Control` headers
- [ ] Integration test verifying that different query parameters are not served stale cached results from a different query
