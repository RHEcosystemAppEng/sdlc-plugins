## Repository
trustify-backend

## Target Branch
main

## Description
Add the REST endpoint `GET /api/v2/sbom/{id}/advisory-summary` that returns aggregated advisory severity counts for a given SBOM. The handler calls `SbomService::advisory_summary()` (created in Task 1) and returns the result as a JSON response. Apply 5-minute response caching using the existing `tower-http` caching middleware. Support an optional `?threshold` query parameter that filters severity counts to only include levels at or above the specified threshold (e.g., `?threshold=critical` returns only the critical count).

This endpoint enables the frontend dashboard severity widget (UC-1) and alerting integrations (UC-2) described in Feature TC-9001.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — endpoint handler for `GET /api/v2/sbom/{id}/advisory-summary` with optional `?threshold` query parameter and 5-minute cache configuration

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the `advisory-summary` route under `/api/v2/sbom/{id}/advisory-summary`
- `server/src/main.rs` — ensure the new route is mounted (verify existing module mounting covers it; add explicit mount if needed)

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: returns `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }` with 200 OK; returns 404 if SBOM does not exist
- `GET /api/v2/sbom/{id}/advisory-summary?threshold=critical` — NEW: returns filtered counts above specified severity level

## Implementation Notes
- Follow the endpoint handler pattern in `modules/fundamental/src/sbom/endpoints/get.rs` for handler signature, path parameter extraction, and JSON response serialization.
- Follow the route registration pattern in `modules/fundamental/src/sbom/endpoints/mod.rs` for adding the new route alongside existing SBOM routes.
- The `?threshold` query parameter should accept values: `critical`, `high`, `medium`, `low`. When provided, zero out counts below the threshold severity level. When absent, return all counts.
- Apply 5-minute (300s) cache using `tower-http` caching layer, consistent with the project's existing cache configuration in endpoint route builders.
- Return the standard 404 error response from `AppError` when `SbomService::advisory_summary()` returns a not-found error, maintaining consistency with `GET /api/v2/sbom/{id}`.
- Per CONVENTIONS.md §Error Handling: all handlers return `Result<T, AppError>` with `.context()` wrapping. Applies: task creates `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's handler file scope.
- Per CONVENTIONS.md §Endpoint Registration: register route in `endpoints/mod.rs`; `server/main.rs` mounts all modules. Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's endpoint registration scope.
- Per CONVENTIONS.md §Caching: use `tower-http` caching middleware for response caching. Applies: task creates `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's endpoint file scope.
- Per docs/constraints.md §5 (Code Change Rules): follow patterns referenced in Implementation Notes; do not duplicate existing functionality.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — GET endpoint handler pattern with path parameter extraction and JSON response
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration pattern for SBOM endpoints
- `common/src/error.rs::AppError` — error response type for 404 and other errors
- `modules/fundamental/src/sbom/endpoints/list.rs` — reference for query parameter extraction pattern

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with JSON body `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`
- [ ] Endpoint returns 404 with standard error response when SBOM ID does not exist
- [ ] Response is cached for 5 minutes (300 seconds)
- [ ] `?threshold=critical` returns only counts at or above critical severity
- [ ] `?threshold=high` returns counts at or above high severity (critical + high)
- [ ] Route is registered in `modules/fundamental/src/sbom/endpoints/mod.rs`
- [ ] Handler follows the existing `Result<T, AppError>` return pattern

## Test Requirements
- [ ] Integration test: `GET /api/v2/sbom/{id}/advisory-summary` returns correct JSON structure with valid SBOM
- [ ] Integration test: endpoint returns 404 for non-existent SBOM
- [ ] Integration test: `?threshold=critical` filters response to critical-only counts
- [ ] Integration test: response includes `Cache-Control` header with appropriate max-age

## Verification Commands
- `cargo test --test api advisory_summary` — all advisory-summary integration tests pass
- `curl -s http://localhost:8080/api/v2/sbom/{id}/advisory-summary | jq .` — returns severity counts JSON

## Dependencies
- Depends on: Task 1 — Create AdvisorySeveritySummary model and aggregation service
