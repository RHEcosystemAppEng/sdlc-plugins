## Repository
trustify-backend

## Target Branch
main

## Description
Add 5-minute cache configuration to the `GET /api/v2/sbom/{id}/advisory-summary` endpoint using the existing `tower-http` caching middleware infrastructure. This ensures that repeated calls for the same SBOM advisory summary within a 5-minute window are served from cache, meeting the p95 < 200ms latency requirement.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — add cache middleware layer to the advisory summary route with a 5-minute TTL
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — add cache-related headers or middleware configuration if required by the existing cache pattern

## Implementation Notes
- The repository uses `tower-http` caching middleware with cache configuration in endpoint route builders (per Key Conventions in the repository structure).
- Inspect `modules/fundamental/src/sbom/endpoints/mod.rs` to determine the exact caching middleware pattern used for existing endpoints. Apply the same pattern to the advisory summary route with a 5-minute (300 second) TTL.
- If the caching is applied via `Cache-Control` headers (e.g., `max-age=300`), add the appropriate response header in the handler or route layer.
- If the caching uses a middleware layer (e.g., `tower_http::services::CacheLayer`), wrap the advisory summary route with the same layer configuration.
- Inspect `server/src/main.rs` for any global cache middleware setup that may already apply.
- Per docs/constraints.md §5.2: inspect existing cache configuration before implementing.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/mod.rs` — inspect for existing cache middleware patterns on other routes
- `server/src/main.rs` — inspect for global cache middleware configuration

## Acceptance Criteria
- [ ] Advisory summary endpoint responses include appropriate cache headers (e.g., `Cache-Control: max-age=300`)
- [ ] Subsequent requests within the 5-minute window are served from cache
- [ ] Cache TTL is 5 minutes (300 seconds)
- [ ] Project compiles successfully with `cargo check`

## Test Requirements
- [ ] Integration test verifying that the response includes cache-related headers with the correct TTL
- [ ] Test verifying that cached responses are returned within the TTL window (if testable with the existing test infrastructure)

## Dependencies
- Depends on: Task 3 — Advisory summary endpoint

[sdlc-workflow] Description digest: sha256-md:9bfe88a03fc3ce010f15e294ba521fc38f2f28eb52594b21d692f7b52c8f1c55
