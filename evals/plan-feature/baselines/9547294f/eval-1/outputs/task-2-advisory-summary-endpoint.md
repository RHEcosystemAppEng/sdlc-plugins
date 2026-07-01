## Repository
trustify-backend

## Target Branch
main

## Description
Add the `GET /api/v2/sbom/{id}/advisory-summary` endpoint handler in the SBOM endpoints module. The endpoint calls `SbomService::advisory_severity_summary` and returns the `AdvisorySeveritySummary` response. Configure 5-minute response caching using the existing tower-http caching middleware. Return 404 when the SBOM ID does not exist, consistent with existing SBOM endpoints.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the new `/api/v2/sbom/{id}/advisory-summary` route with 5-minute cache configuration

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — handler function for `GET /api/v2/sbom/{id}/advisory-summary`

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: returns `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }` with 5-minute cache headers. Returns 404 if SBOM ID does not exist.

## Implementation Notes
- Follow the endpoint registration pattern in `modules/fundamental/src/sbom/endpoints/mod.rs` — existing routes for `list.rs` (GET /api/v2/sbom) and `get.rs` (GET /api/v2/sbom/{id}) show how routes are registered and mounted.
- The handler should extract the SBOM ID from the path parameter, call `SbomService::advisory_severity_summary`, and return the result as JSON.
- For 404 handling, follow the same pattern used by `GET /api/v2/sbom/{id}` in `modules/fundamental/src/sbom/endpoints/get.rs` — the handler returns `Result<T, AppError>` and the service method returns an `AppError` for missing SBOMs.
- Configure caching using tower-http caching middleware as described in the Key Conventions. Set `Cache-Control: max-age=300` (5 minutes) on the route builder. See existing endpoint route builders for the caching configuration pattern.
- The handler should return `Result<Json<AdvisorySeveritySummary>, AppError>` following the Axum handler pattern used throughout the codebase.
- Per CONVENTIONS.md: each module's `endpoints/mod.rs` registers routes; `server/main.rs` mounts all modules. The new route is registered in the existing SBOM endpoints module.
  Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's Rust endpoint file scope.
- Per CONVENTIONS.md: all handlers return `Result<T, AppError>` with `.context()` wrapping.
  Applies: task creates `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's Rust endpoint file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — existing GET handler for SBOM details; follow the same pattern for path parameter extraction, service invocation, and error handling
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration pattern; add the new route alongside existing SBOM routes
- `common/src/error.rs::AppError` — error type implementing `IntoResponse`; reuse for 404 and server error responses

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`
- [ ] Endpoint returns 404 when SBOM ID does not exist
- [ ] Response includes `Cache-Control: max-age=300` header (5-minute cache)
- [ ] Response time p95 < 200ms for SBOMs with up to 500 advisories

## Test Requirements
- [ ] Integration test: GET request to `/api/v2/sbom/{id}/advisory-summary` returns 200 with correct severity counts
- [ ] Integration test: GET request with non-existent SBOM ID returns 404
- [ ] Integration test: verify response contains cache control headers

## Verification Commands
- `cargo test --test api` — run integration tests and verify new endpoint tests pass

## Documentation Updates
- `README.md` — add the new endpoint to any API endpoint listing if present

## Dependencies
- Depends on: Task 1 — Add AdvisorySeveritySummary model and SbomService aggregation method

---

> [sdlc-workflow] Description digest: (simulated) The digest would be posted as a Jira comment after task creation per the description-digest-protocol. Format: `[sdlc-workflow] Description digest: sha256-md:<64-hex-chars>`
