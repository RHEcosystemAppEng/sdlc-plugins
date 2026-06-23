## Repository
trustify-backend

## Target Branch
main

## Description
Add 5-minute response caching to the `GET /api/v2/sbom/{id}/advisory-summary` endpoint using the existing `tower-http` caching middleware infrastructure. The cache key must incorporate both the SBOM ID and the optional `threshold` query parameter so that different threshold values produce separate cache entries.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Apply caching middleware layer to the advisory-summary route with a 5-minute (300 second) TTL
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — Add appropriate `Cache-Control` response headers (`max-age=300, public`) to enable `tower-http` caching

## Implementation Notes
The repository uses `tower-http` caching middleware as noted in the Key Conventions section of the repo structure. Check how existing endpoints configure caching by examining the route builder in `modules/fundamental/src/sbom/endpoints/mod.rs` and `server/src/main.rs`.

The caching approach should follow one of these patterns (depending on what the existing codebase uses):
1. **Middleware layer on the route** — wrap the advisory-summary route with a `tower_http::services::SetResponseHeader` or cache middleware layer configured with `max-age=300`
2. **Response header in the handler** — set `Cache-Control: public, max-age=300` on the response within the handler function, and let a global caching middleware respect it

The cache key must differentiate between requests with different query parameters. If `tower-http` caching uses the full request URI (including query string) as the cache key, this is handled automatically. Verify this assumption by checking the middleware configuration in `server/src/main.rs`.

## Reuse Candidates
- `server/src/main.rs` — global middleware configuration, may show existing cache middleware setup patterns
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route builder where per-route middleware layers are applied

## Acceptance Criteria
- [ ] Response includes `Cache-Control: public, max-age=300` header
- [ ] Repeated requests within 5 minutes return cached response (no database query)
- [ ] Different `threshold` query parameter values produce separate cache entries
- [ ] Cache entry expires after 5 minutes, subsequent request queries the database

## Test Requirements
- [ ] Integration test: verify `Cache-Control` header is present on response with correct `max-age=300` value
- [ ] Integration test: two rapid requests return identical responses (cache hit verification, if testable)

## Dependencies
- Depends on: Task 3 — Advisory summary endpoint (needs the endpoint to exist before adding caching)

[sdlc-workflow] Description digest: sha256-md:11ba8faba4e9ffa52a7a38160a7ae9b79bd8f7494041e12bdfa453428997be03
