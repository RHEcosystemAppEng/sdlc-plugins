## Repository
trustify-backend

## Target Branch
main

## Parent Epic
TC-9006: trustify-backend

## Description
Add REST API endpoints for remediation data. Create `GET /api/v2/remediation/summary` returning aggregated severity × status counts, and `GET /api/v2/remediation/by-product` returning per-product remediation breakdowns. Register both routes in the server's route mounting configuration.

## Files to Create
- `modules/fundamental/src/remediation/endpoints/mod.rs` — route registration and handler functions for both remediation endpoints

## Files to Modify
- `modules/fundamental/src/remediation/mod.rs` — add `pub mod endpoints;` declaration
- `server/src/main.rs` — mount remediation routes alongside existing module routes

## API Changes
- `GET /api/v2/remediation/summary` — NEW: returns RemediationSummary with severity × status aggregated counts
- `GET /api/v2/remediation/by-product` — NEW: returns RemediationByProduct with per-product total/open/resolved counts

## Implementation Notes
Follow the endpoint pattern in `modules/fundamental/src/sbom/endpoints/mod.rs` and `modules/fundamental/src/sbom/endpoints/list.rs`:

- Define handler functions as `async fn` taking Axum extractors
- Return `Result<Json<T>, AppError>` per `common/src/error.rs` pattern
- Register routes using Axum's Router::new().route() pattern (see `modules/fundamental/src/sbom/endpoints/mod.rs` for route registration)
- Mount in `server/src/main.rs` following the same `.merge()` or `.nest()` pattern used for sbom and advisory modules
- Both endpoints return the model types from Task 1 — `RemediationSummary` and `RemediationByProduct`
- Non-functional requirement: p95 < 500ms — ensure queries are efficient; consider adding `tower-http` caching middleware (see SBOM endpoint caching pattern in `modules/fundamental/src/sbom/endpoints/mod.rs`)

Per docs/constraints.md §5 (Code Change Rules): endpoint handlers delegate to service layer — no direct database queries in handler functions.

## Acceptance Criteria
- [ ] GET /api/v2/remediation/summary returns 200 with RemediationSummary JSON
- [ ] GET /api/v2/remediation/by-product returns 200 with RemediationByProduct JSON
- [ ] Routes are registered and reachable from the server
- [ ] Handlers delegate to RemediationService methods
- [ ] Response Content-Type is application/json

## Test Requirements
- [ ] Verify GET /api/v2/remediation/summary returns 200 with expected JSON structure
- [ ] Verify GET /api/v2/remediation/by-product returns 200 with expected JSON structure
- [ ] Verify 404/error responses for malformed requests
- [ ] Verify caching headers are set if caching middleware is applied

## Dependencies
- Depends on: Task 1 — Remediation models
- Depends on: Task 2 — Remediation service
