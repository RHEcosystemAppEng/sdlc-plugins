## Repository
trustify-backend

## Target Branch
main

## Description
Add a 5-minute cache layer to the advisory-summary endpoint using the existing tower-http caching middleware. This avoids repeated database aggregation queries for the same SBOM, meeting the performance requirement of p95 < 200ms for subsequent requests.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — Add cache-control headers or caching middleware layer to the handler
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Apply tower-http caching middleware to the advisory-summary route

## Implementation Notes
Use the existing `tower-http` caching middleware pattern already established in the codebase. The cache configuration should be applied at the route level in `modules/fundamental/src/sbom/endpoints/mod.rs` when registering the advisory-summary route.

Set the cache TTL to 300 seconds (5 minutes) using `Cache-Control: max-age=300` response headers. Follow whichever caching pattern is used by other endpoint route builders in the project — inspect how `tower-http` caching is configured for existing endpoints.

Consider using an in-memory cache keyed by SBOM ID if the project uses application-level caching rather than HTTP-level caching. The key should include the threshold parameter if present (e.g., `advisory-summary:{sbom_id}:{threshold}`).

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Check existing route builders for caching middleware configuration patterns

## Acceptance Criteria
- [ ] Advisory-summary endpoint responses are cached for 5 minutes
- [ ] Cache key includes SBOM ID and optional threshold parameter
- [ ] Subsequent requests within the 5-minute window are served from cache without database query
- [ ] Cache respects existing tower-http caching middleware patterns

## Verification Commands
- `cargo check -p trustify-fundamental` — compiles without errors

## Dependencies
- Depends on: Task 3 — Advisory summary endpoint

[sdlc-workflow] Description digest: sha256-md:d7f0a2c4e6b8391806b42d7e8a1c5e9f0d23f4a6b8c0312d4e6f8a0b2c3d5e7
