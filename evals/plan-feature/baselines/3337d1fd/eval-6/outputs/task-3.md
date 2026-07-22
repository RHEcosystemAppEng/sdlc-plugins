## Repository
trustify-backend

## Target Branch
main

## Description
Create the remediation API endpoints that expose the aggregation data via REST. Register two new routes: GET /api/v2/remediation/summary for the overall remediation summary and GET /api/v2/remediation/by-product for the per-product breakdown. Mount the routes in the server application.

## Files to Create
- `modules/fundamental/src/remediation/endpoints/mod.rs` — route registration for /api/v2/remediation, mounts summary and by-product sub-routes
- `modules/fundamental/src/remediation/endpoints/summary.rs` — GET /api/v2/remediation/summary handler
- `modules/fundamental/src/remediation/endpoints/by_product.rs` — GET /api/v2/remediation/by-product handler

## Files to Modify
- `modules/fundamental/src/remediation/mod.rs` — add `pub mod endpoints;` to expose the endpoints submodule
- `server/src/main.rs` — mount remediation module routes alongside existing sbom, advisory, and package modules

## API Changes
- `GET /api/v2/remediation/summary` — NEW: returns aggregated remediation counts by severity and status
- `GET /api/v2/remediation/by-product` — NEW: returns paginated per-product remediation breakdown with total, open, resolved counts

## Implementation Notes
Follow the endpoint pattern in `modules/fundamental/src/sbom/endpoints/mod.rs` for route registration and `modules/fundamental/src/sbom/endpoints/list.rs` for handler implementation. Each handler extracts query parameters, calls the corresponding RemediationService method, and returns the result as JSON. Use `common/src/model/paginated.rs::PaginatedResults<T>` for the by-product endpoint response. Mount the remediation routes in `server/src/main.rs` following the same pattern used for sbom and advisory modules. Handlers return `Result<Json<T>, AppError>` per the project convention.

Per CONVENTIONS.md §Endpoint registration: register routes in endpoints/mod.rs, mount in server/main.rs.
Applies: task creates `modules/fundamental/src/remediation/endpoints/mod.rs` matching the convention's `.rs` file scope.

Per CONVENTIONS.md §Response types: list endpoints return PaginatedResults<T>.
Applies: task creates `modules/fundamental/src/remediation/endpoints/by_product.rs` matching the convention's `.rs` file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration pattern reference
- `modules/fundamental/src/sbom/endpoints/list.rs` — handler implementation pattern with pagination
- `common/src/model/paginated.rs::PaginatedResults<T>` — paginated response wrapper

## Acceptance Criteria
- [ ] GET /api/v2/remediation/summary returns JSON with severity-by-status counts
- [ ] GET /api/v2/remediation/by-product returns paginated JSON with per-product breakdown
- [ ] Routes are mounted in server/src/main.rs
- [ ] Endpoints follow existing error handling patterns (Result<T, AppError>)

## Test Requirements
- [ ] Handler unit tests with mock service data for both endpoints
- [ ] Verify correct HTTP status codes (200 OK for valid requests)

## Dependencies
- Depends on: Task 2 — Implement remediation service with aggregation queries
