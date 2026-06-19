## Repository
trustify-backend

## Target Branch
main

## Description
Add response caching to the search endpoint to reduce database load and improve response times for repeated or common queries. This complements the database indexing (Task 1) to further address the "search should be faster" requirement from TC-9002.

**Ambiguity note:** The feature specifies no caching requirements, TTL values, or invalidation strategy. This task assumes a short-lived HTTP-level cache (e.g., 30-60 seconds) using the existing `tower-http` caching middleware pattern already used in the codebase. Cache key includes query text and filter parameters. This assumption is pending clarification — a longer TTL may be appropriate if search data changes infrequently.

## Files to Modify
- `modules/search/src/endpoints/mod.rs` — Add `tower-http` caching middleware to the search route builder, following the pattern used by other endpoint modules in the codebase

## Implementation Notes
Inspect `modules/search/src/endpoints/mod.rs` to see the current route configuration. The repo convention notes that caching uses `tower-http` caching middleware with cache configuration in endpoint route builders. Inspect other endpoint modules (e.g., `modules/fundamental/src/sbom/endpoints/mod.rs` or `modules/fundamental/src/advisory/endpoints/mod.rs`) to find the existing caching pattern and replicate it for the search endpoint.

The cache should:
- Use `tower-http` `CacheLayer` or equivalent middleware
- Set a `Cache-Control` header with a short `max-age` (e.g., 60 seconds)
- Apply to the `GET /api/v2/search` route
- The cache key is automatically derived from the request URL (including query parameters) by HTTP caching semantics

Per CONVENTIONS.md §Caching: use `tower-http` caching middleware with cache configuration in endpoint route builders. Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's `.rs` scope.

Per CONVENTIONS.md §Endpoint registration: the caching middleware is added as part of the route builder in `modules/search/src/endpoints/mod.rs`. Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's `.rs` scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/mod.rs` — reference for existing `tower-http` cache middleware usage pattern on endpoint routes
- `modules/fundamental/src/advisory/endpoints/mod.rs` — another reference for caching middleware configuration

## Acceptance Criteria
- [ ] The search endpoint (`GET /api/v2/search`) has response caching enabled via `tower-http` middleware
- [ ] Cache-Control headers are set with an appropriate `max-age` value
- [ ] Different query/filter combinations are cached independently (URL-based cache key)
- [ ] The caching pattern is consistent with how other endpoints in the codebase configure caching

## Test Requirements
- [ ] Two identical search requests within the cache TTL return the same response (cache hit verified via response headers or timing)
- [ ] Different search queries produce independent cache entries
- [ ] Cache expires after the configured TTL (subsequent request reflects updated data)
