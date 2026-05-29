# Task 3 -- Add GET /api/v2/sbom/{id}/advisory-summary endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Add the `GET /api/v2/sbom/{id}/advisory-summary` endpoint handler that calls `SbomService::get_advisory_summary`, returns the severity counts as JSON, and applies 5-minute caching using the existing `tower-http` cache infrastructure. This is the primary deliverable of feature TC-9001, providing a single-call alternative to multi-page client-side advisory counting.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` -- endpoint handler for `GET /api/v2/sbom/{id}/advisory-summary`

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` -- register the new `advisory-summary` route alongside existing SBOM routes (`list.rs`, `get.rs`)

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` -- NEW: returns `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }` with 5-minute cache, 404 if SBOM not found

## Implementation Notes
- Follow the existing endpoint handler pattern in `modules/fundamental/src/sbom/endpoints/get.rs`. Handlers take Axum extractors (Path for `{id}`, State for service access) and return `Result<Json<T>, AppError>`.
- **Route registration**: Add the route in `modules/fundamental/src/sbom/endpoints/mod.rs` following the pattern used for `list.rs` and `get.rs`. The route path should be `/api/v2/sbom/{id}/advisory-summary`.
- **Caching**: Apply 5-minute cache using the existing `tower-http` caching middleware. Check the route builder configuration in `modules/fundamental/src/sbom/endpoints/mod.rs` for how caching is currently configured on other endpoints. Add `Cache-Control: max-age=300` or the equivalent `tower-http` layer configuration.
- **Error handling**: Return 404 when the SBOM does not exist, consistent with the existing `GET /api/v2/sbom/{id}` endpoint behavior. Use the same `AppError` variant that the existing `get.rs` handler uses for SBOM-not-found.
- **Response shape**: The response body must exactly match: `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }` where N is a non-negative integer.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` -- reference for handler signature, Path extractor for `{id}`, error handling for SBOM-not-found (404)
- `modules/fundamental/src/sbom/endpoints/mod.rs` -- reference for route registration pattern and cache middleware application
- `modules/fundamental/src/sbom/endpoints/list.rs` -- reference for Axum handler patterns used in this module

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with correct JSON response shape
- [ ] Endpoint returns 404 when SBOM ID does not exist
- [ ] Response is cached for 5 minutes using the existing cache infrastructure
- [ ] Route is registered in the SBOM module's route configuration

## Test Requirements
- [ ] Integration test: valid SBOM ID returns 200 with expected severity counts JSON
- [ ] Integration test: nonexistent SBOM ID returns 404
- [ ] Integration test: response includes appropriate cache headers (max-age=300)

## Verification Commands
- `cargo test --package fundamental -- sbom::endpoints::test_advisory_summary` -- endpoint tests pass
- `curl -s http://localhost:8080/api/v2/sbom/{id}/advisory-summary | jq .` -- returns expected JSON shape

## Documentation Updates
- `README.md` -- add the new endpoint to any API endpoint listing if present

## Dependencies
- Depends on: Task 2 -- Add severity aggregation service method
