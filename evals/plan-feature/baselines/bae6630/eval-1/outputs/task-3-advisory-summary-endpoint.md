## Repository
trustify-backend

## Target Branch
main

## Description
Create the Axum HTTP handler for `GET /api/v2/sbom/{id}/advisory-summary`. The handler extracts the SBOM ID from the path, an optional `threshold` query parameter, calls the service method to get severity counts, applies threshold filtering if requested, sets cache-control headers for 5-minute caching, and returns the JSON response.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — Axum handler function for the advisory summary endpoint

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the new `advisory_summary` module and add the route to the SBOM router

## Implementation Notes
- Follow the handler pattern in `modules/fundamental/src/sbom/endpoints/get.rs` (GET /api/v2/sbom/{id}): extract path parameter with `axum::extract::Path`, inject service via Axum state, return `Result<Json<AdvisorySeveritySummary>, AppError>`.
- Define a query parameters struct (e.g., `AdvisorySummaryQuery`) with an `Option<SeverityThreshold>` field named `threshold`, deriving `Deserialize`. Extract it with `axum::extract::Query`.
- When `threshold` is provided, zero out severity counts below the threshold. For example, `threshold=high` keeps `critical` and `high` counts, sets `medium` and `low` to 0, and recalculates `total`.
- Add cache-control headers: set `Cache-Control: public, max-age=300` (5 minutes) on the response. Use `tower-http` caching middleware consistent with the existing cache infrastructure referenced in the Key Conventions.
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` following the pattern of existing route registrations (e.g., how `get.rs` and `list.rs` are registered). Add `.route("/api/v2/sbom/:id/advisory-summary", get(advisory_summary::handler))` to the existing router builder.
- Return `AppError` (from `common/src/error.rs`) for error cases — the service layer already returns 404-appropriate errors for missing SBOMs.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — Pattern for path parameter extraction, service injection, and JSON response
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Route registration pattern to follow
- `modules/fundamental/src/sbom/endpoints/list.rs` — Pattern for query parameter extraction with `axum::extract::Query`
- `common/src/error.rs::AppError` — Error type that implements `IntoResponse` for automatic HTTP error responses

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with JSON body `{ critical, high, medium, low, total }`
- [ ] Returns 404 when SBOM ID does not exist
- [ ] Optional `?threshold=critical|high|medium|low` filters counts to only include severities at or above the threshold
- [ ] Response includes `Cache-Control: public, max-age=300` header
- [ ] Route is registered in the SBOM endpoints module

## Test Requirements
- [ ] Handler returns 200 with correct JSON structure for a valid SBOM
- [ ] Handler returns 404 for non-existent SBOM
- [ ] Threshold parameter correctly filters severity counts
- [ ] Response headers include cache-control directive

## Dependencies
- Depends on: Task 1 — Advisory summary model (requires `AdvisorySeveritySummary` and `SeverityThreshold`)
- Depends on: Task 2 — Advisory summary service (requires `SbomService::advisory_severity_summary`)

## Digest
[sdlc-workflow] Description digest: sha256-md:6eea75d3c27f990ac1df70afa6f7ab188aa2ac670af06daa14a8be00a0c3f58a
