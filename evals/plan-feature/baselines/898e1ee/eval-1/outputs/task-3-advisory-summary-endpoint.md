# Task 3 — Advisory Summary Endpoint and Route Registration

## Repository
trustify-backend

## Target Branch
main

## Description
Add the `GET /api/v2/sbom/{id}/advisory-summary` Axum handler and register it in the SBOM endpoint module's router. The handler extracts the SBOM ID from the path, an optional `threshold` query parameter, calls `SbomService::get_advisory_severity_summary`, and returns the result as JSON. The route is configured with a 5-minute `tower-http` cache layer per the caching convention.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — Define the Axum handler function `pub async fn get_advisory_summary(Path(id): Path<Uuid>, Query(params): Query<AdvisorySummaryParams>, State(service): State<SbomService>, State(db): State<DatabaseConnection>) -> Result<Json<AdvisorySeveritySummary>, AppError>`. Define `AdvisorySummaryParams` struct with `threshold: Option<SeverityThreshold>` for query parameter extraction.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Add `mod advisory_summary;` declaration. In the route registration function, add `.route("/api/v2/sbom/:id/advisory-summary", get(advisory_summary::get_advisory_summary))` with a `CacheControl` layer configured for `max-age=300` (5 minutes).

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: Returns JSON `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`. Optional query param `?threshold=critical|high|medium|low` filters to only severities at or above the threshold. Returns 404 if SBOM ID does not exist.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — Existing `GET /api/v2/sbom/{id}` handler; follow its pattern for path parameter extraction, service invocation, and error handling.
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Route registration pattern; follow how existing routes are added to the router.
- `common/src/error.rs::AppError` — `AppError` implements `IntoResponse`, so returning `Result<Json<T>, AppError>` from the handler automatically produces correct HTTP error responses.

## Implementation Notes
Follow the handler pattern in `modules/fundamental/src/sbom/endpoints/get.rs` which extracts `Path(id)` and calls a service method, returning `Json(result)`. The handler function signature should match the Axum extractor conventions used throughout the codebase.

For caching, follow the existing `tower-http` caching middleware pattern referenced in the Key Conventions. Configure the route with `CacheControl::new().with_max_age(Duration::from_secs(300))` or the equivalent `tower-http` cache layer builder used elsewhere in the route registration.

The `AdvisorySummaryParams` query struct should derive `Deserialize` so Axum's `Query` extractor can parse it from the URL query string.

Per CONVENTIONS.md §Framework: use Axum for HTTP handler. Applies: task creates `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's `.rs` file scope.

Per CONVENTIONS.md §Endpoint registration: register routes in `endpoints/mod.rs`. Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's `.rs` endpoint registration scope.

Per CONVENTIONS.md §Error handling: return `Result<T, AppError>` with `.context()` wrapping. Applies: task creates `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's `.rs` file scope.

Per CONVENTIONS.md §Caching: use `tower-http` caching middleware in endpoint route builders. Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's endpoint route builder scope.

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with JSON severity counts
- [ ] Response shape is `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`
- [ ] Returns 404 when SBOM ID does not exist
- [ ] Optional `?threshold` query param filters severity counts
- [ ] Response includes `Cache-Control: max-age=300` header
- [ ] Route is registered in the SBOM endpoint module router
- [ ] `cargo check` passes with no errors

## Test Requirements
- [ ] Handler returns 200 with correct JSON structure for a valid SBOM
- [ ] Handler returns 404 for a non-existent SBOM ID
- [ ] Cache-Control header is set to 300 seconds

## Dependencies
- Depends on: Task 2 — Advisory Severity Aggregation Service Method (provides `SbomService::get_advisory_severity_summary`)

[sdlc-workflow] Description digest: sha256-md:6c6ea2546d3b4b81219743f254535234ab2be280cea34491374d7819751bb46e
