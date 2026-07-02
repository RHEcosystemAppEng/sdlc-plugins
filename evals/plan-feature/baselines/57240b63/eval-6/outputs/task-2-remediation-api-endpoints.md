## Repository
trustify-backend

## Target Branch
main

## Parent Epic
TC-9006: trustify-backend

## Description
Create the REST API endpoints for the remediation tracking dashboard. This task adds two new endpoints under `/api/v2/remediation/`: a summary endpoint that returns aggregated vulnerability counts by severity and status, and a by-product endpoint that returns per-product remediation breakdowns. Both endpoints are registered in the server route tree following the established endpoint registration pattern.

## Files to Create
- `modules/fundamental/src/remediation/endpoints/mod.rs` -- route registration for /api/v2/remediation, mounts summary and by-product handlers
- `modules/fundamental/src/remediation/endpoints/summary.rs` -- GET /api/v2/remediation/summary handler
- `modules/fundamental/src/remediation/endpoints/by_product.rs` -- GET /api/v2/remediation/by-product handler

## Files to Modify
- `server/src/main.rs` -- mount remediation module routes alongside existing module routes (sbom, advisory, package, search)

## API Changes
- `GET /api/v2/remediation/summary` -- NEW: returns RemediationSummary with aggregated counts grouped by severity (Critical/High/Medium/Low) x status (Open/In Progress/Resolved), plus totals
- `GET /api/v2/remediation/by-product` -- NEW: returns PaginatedResults<ProductRemediation> with per-product breakdown (total, open, in_progress, resolved counts); supports offset/limit query parameters for pagination

## Implementation Notes
- Follow the endpoint registration pattern from `modules/fundamental/src/sbom/endpoints/mod.rs`: define a function that returns an Axum Router, register individual route handlers, and export the router for mounting in `server/src/main.rs`.
  - Applies: task creates `modules/fundamental/src/remediation/endpoints/mod.rs` matching the convention's endpoint registration scope.
- All handlers must return `Result<Json<T>, AppError>` with `.context()` error wrapping, consistent with handlers in `modules/fundamental/src/sbom/endpoints/list.rs` and `modules/fundamental/src/sbom/endpoints/get.rs`.
  - Applies: task creates `modules/fundamental/src/remediation/endpoints/summary.rs` matching the convention's error handling scope.
- The by-product endpoint should accept pagination query parameters (offset, limit) and return `PaginatedResults<ProductRemediation>` using the pattern from `common/src/model/paginated.rs`.
  - Applies: task creates `modules/fundamental/src/remediation/endpoints/by_product.rs` matching the convention's response type scope.
- Use shared query helpers from `common/src/db/query.rs` for pagination parameter extraction and validation.
- Configure `tower-http` caching middleware on the remediation routes. The summary endpoint benefits from short-lived caching (e.g., 60s TTL) since aggregation queries may be expensive. Follow the caching configuration pattern used in existing endpoint route builders.
  - Applies: task creates `modules/fundamental/src/remediation/endpoints/mod.rs` matching the convention's caching scope.
- In `server/src/main.rs`, mount the remediation router using the same pattern as existing modules (e.g., `.merge(remediation::endpoints::router(state.clone()))`).

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/mod.rs` -- reference for route registration pattern and router construction
- `modules/fundamental/src/sbom/endpoints/list.rs` -- reference for list endpoint handler with pagination
- `common/src/db/query.rs` -- shared query parameter extraction and validation
- `common/src/model/paginated.rs::PaginatedResults<T>` -- standard paginated response wrapper
- `common/src/error.rs::AppError` -- standard error type for all handlers

## Acceptance Criteria
- [ ] GET /api/v2/remediation/summary returns 200 with RemediationSummary JSON body
- [ ] GET /api/v2/remediation/by-product returns 200 with PaginatedResults<ProductRemediation> JSON body
- [ ] by-product endpoint supports offset and limit query parameters
- [ ] Both endpoints return appropriate error responses (500 with AppError) on service failures
- [ ] Routes are registered and accessible when the server starts
- [ ] Caching middleware is configured on remediation routes

## Test Requirements
- [ ] Verify both endpoints return 200 status codes with valid response shapes
- [ ] Verify by-product endpoint respects pagination parameters
- [ ] Verify error handling returns proper AppError responses

## Verification Commands
- `cargo build` -- compiles without errors
- `cargo run` -- server starts and remediation routes are mounted

## Dependencies
- Depends on: Task 1 -- Create remediation domain models and aggregation service

---
Description digest: sha256-md:4461feaf63dd8da2c8067ad678b2dc17631d8588aaed6441018c06683f207bc7
