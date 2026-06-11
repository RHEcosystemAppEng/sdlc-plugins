# Task 4 — Add caching to the search endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Add HTTP caching headers to the `GET /api/v2/search` endpoint using the existing `tower-http` caching middleware infrastructure. This addresses the "search should be faster" requirement by reducing redundant database queries for repeated or similar search requests.

The codebase already uses `tower-http` caching middleware configured via endpoint route builders (per the Key Conventions). This task applies the same caching pattern to the search endpoint, ensuring that identical search queries within a short time window are served from cache rather than hitting the database.

## Files to Modify
- `modules/search/src/endpoints/mod.rs` — Add `tower-http` caching middleware to the search route configuration, following the caching patterns used by other endpoint modules

## Implementation Notes
- The project already uses `tower-http` caching middleware with cache configuration in endpoint route builders (per the repository's Key Conventions). Inspect existing endpoint modules (e.g., `modules/fundamental/src/sbom/endpoints/mod.rs`, `modules/fundamental/src/advisory/endpoints/mod.rs`) to find the established caching pattern
- Apply a short cache TTL appropriate for search results (e.g., 30-60 seconds) — search data changes with ingestion events, so aggressive caching would serve stale results
- Cache should vary by the full query string (including all filter parameters) to ensure filtered and unfiltered searches are cached independently
- Set appropriate `Cache-Control` headers: `public, max-age=<ttl>`, with `Vary: Accept, Accept-Encoding` to handle content negotiation
- Do not cache error responses (4xx, 5xx)
- Per docs/constraints.md section 5.2: inspect the existing caching middleware configuration in other endpoint modules before implementing

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Route registration with caching middleware configuration; primary pattern to follow
- `modules/fundamental/src/advisory/endpoints/mod.rs` — Another endpoint with caching middleware; cross-reference for consistent TTL and configuration
- `server/src/main.rs` — Axum server setup and route mounting; verify how caching middleware is applied at the server level

## Acceptance Criteria
- [ ] Search endpoint responses include appropriate Cache-Control headers
- [ ] Identical search requests within the cache TTL are served from cache (faster response)
- [ ] Different query parameters produce different cache entries (correct Vary behavior)
- [ ] Cache TTL is reasonable for search data freshness (not too aggressive)
- [ ] Error responses are not cached

## Test Requirements
- [ ] Test that search responses include Cache-Control headers
- [ ] Test that repeated identical requests are served faster (cache hit)
- [ ] Test that different query parameters produce independent cache entries

## Verification Commands
- `cargo test -p search` — all search module tests pass
- `curl -v "http://localhost:8080/api/v2/search?q=test" 2>&1 | grep -i cache-control` — Cache-Control header is present in response

## Dependencies
- Depends on: Task 3 — Add filtering parameters to the search endpoint
