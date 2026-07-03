## Repository
trustify-backend

## Target Branch
main

## Parent Epic
TC-9006: trustify-backend

## Description
Add REST endpoints for the remediation aggregation service created in Task 1. Expose `GET /api/v2/remediation/summary` for aggregated counts by severity and status, and `GET /api/v2/remediation/by-product` for per-product remediation breakdowns. Register the routes in the Axum server.

## Files to Create
- `modules/fundamental/src/remediation/endpoints/mod.rs` -- route registration for /api/v2/remediation
- `modules/fundamental/src/remediation/endpoints/summary.rs` -- GET /api/v2/remediation/summary handler
- `modules/fundamental/src/remediation/endpoints/by_product.rs` -- GET /api/v2/remediation/by-product handler

## Files to Modify
- `modules/fundamental/src/remediation/mod.rs` -- add endpoints module declaration
- `server/src/main.rs` -- mount remediation routes alongside existing module routes

## API Changes
- `GET /api/v2/remediation/summary` -- NEW: returns aggregated remediation counts by severity (Critical/High/Medium/Low) and status (Open/In Progress/Resolved)
- `GET /api/v2/remediation/by-product` -- NEW: returns per-product remediation breakdown with total, open, and resolved counts per product

## Implementation Notes
- Follow the endpoint registration pattern in `modules/fundamental/src/sbom/endpoints/mod.rs` -- each endpoint module registers routes, and `server/src/main.rs` mounts all modules.
- Handler functions should follow the pattern in `modules/fundamental/src/sbom/endpoints/list.rs` and `modules/fundamental/src/sbom/endpoints/get.rs`: extract dependencies from Axum state, call the service, and return typed responses.
- All handlers must return `Result<T, AppError>` following the error handling convention in `common/src/error.rs`.
- The by-product endpoint should return `PaginatedResults<ProductRemediation>` using the wrapper from `common/src/model/paginated.rs` to support large product portfolios (>50 products).
- Support query parameter filtering via the shared helpers in `common/src/db/query.rs`.
- Mount routes in `server/src/main.rs` following the existing pattern where each module's endpoint `mod.rs` registers its routes.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/mod.rs` -- reference pattern for route registration
- `modules/fundamental/src/sbom/endpoints/list.rs` -- reference pattern for list endpoint handler
- `common/src/model/paginated.rs::PaginatedResults<T>` -- response wrapper for the by-product endpoint
- `common/src/db/query.rs` -- shared query builder for filtering and pagination parameters

## Acceptance Criteria
- [ ] GET /api/v2/remediation/summary returns JSON with aggregated counts grouped by severity and status
- [ ] GET /api/v2/remediation/by-product returns paginated JSON with per-product remediation breakdown
- [ ] Both endpoints return proper HTTP error responses for server errors
- [ ] Routes are registered and accessible when the server starts
- [ ] Summary endpoint response time meets p95 < 500ms target

## Test Requirements
- [ ] Handler unit test for summary endpoint verifying correct JSON response shape
- [ ] Handler unit test for by-product endpoint verifying paginated response
- [ ] Test that both endpoints return 200 OK with valid data
- [ ] Test error handling when service returns an error

## Verification Commands
- `cargo build -p trustify-server` -- verify server compiles with new routes
- `cargo test -p trustify-fundamental -- remediation::endpoints` -- run endpoint tests

## Dependencies
- Depends on: Task 1 -- Add remediation model types and aggregation service
