## Repository
trustify-backend

## Target Branch
main

## Description
Create the REST endpoint handler for `GET /api/v2/sbom/{id}/advisory-summary` that calls `SbomService::get_advisory_severity_summary` and returns the severity counts as JSON. Configure a 5-minute cache TTL using the existing tower-http caching middleware. Register the route in the SBOM endpoints module.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — Axum handler function for the advisory-summary GET endpoint

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the `/api/v2/sbom/{id}/advisory-summary` route

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: returns `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }` with 5-minute cache TTL. Returns 404 if the SBOM ID does not exist.

## Implementation Notes
- Follow the existing endpoint handler pattern from `modules/fundamental/src/sbom/endpoints/get.rs` (the `GET /api/v2/sbom/{id}` handler): extract the `id` path parameter, call the corresponding service method, return `Json<AdvisorySeveritySummary>` on success.
- Handler signature: `async fn advisory_summary(Path(id): Path<Id>, State(service): State<SbomService>) -> Result<Json<AdvisorySeveritySummary>, AppError>`.
- Configure 5-minute cache TTL using tower-http caching middleware in the route builder, following the caching configuration pattern used by existing cached endpoints.
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` as `.route("/api/v2/sbom/:id/advisory-summary", get(advisory_summary))` adjacent to the existing SBOM routes.
- Add OpenAPI documentation attributes (`#[utoipa::path(...)]`) following the pattern in existing endpoint handlers.

Per CONVENTIONS.md §Endpoint Registration: register the route in `modules/fundamental/src/sbom/endpoints/mod.rs`; it will be mounted automatically by `server/src/main.rs`.
Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's endpoint registration scope.

Per CONVENTIONS.md §Error Handling: handler returns `Result<Json<AdvisorySeveritySummary>, AppError>` with `.context()` wrapping on errors.
Applies: task creates `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's `.rs` handler file scope.

Per CONVENTIONS.md §Caching: configure the 5-minute cache TTL using tower-http caching middleware in the route builder configuration.
Applies: task creates `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's endpoint file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — follow the same handler pattern for a single-resource GET endpoint (path extraction, service call, JSON response)
- `modules/fundamental/src/sbom/endpoints/mod.rs` — follow the existing route registration pattern for adding a new sub-resource route

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns HTTP 200 with JSON body `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`
- [ ] Response includes `Cache-Control` header with 5-minute max-age (300 seconds)
- [ ] Returns HTTP 404 when the SBOM ID does not exist
- [ ] Endpoint is registered and accessible via the Axum router
- [ ] OpenAPI schema is generated for the endpoint

## Test Requirements
- [ ] Integration test: endpoint returns correct severity counts for a known SBOM with linked advisories
- [ ] Integration test: endpoint returns 404 for a non-existent SBOM ID
- [ ] Integration test: response includes cache-related headers

## Documentation Updates
- `README.md` — add the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint to the API reference section with its path, parameters, and response shape

## Dependencies
- Depends on: Task 1 — Add AdvisorySeveritySummary model and severity aggregation service method

---

[sdlc-workflow] Description digest: sha256-md:e15fbf036505ececa0dc9a41c8021b5d35b891006539de273e6ab9e5db36572f
