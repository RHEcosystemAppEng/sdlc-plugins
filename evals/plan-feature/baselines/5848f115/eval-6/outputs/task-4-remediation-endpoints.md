# Task 4 — Add remediation summary and by-product endpoints

## Repository
trustify-backend

## Target Branch
TC-9006

## Description
Add the two REST API endpoints for remediation aggregation: `GET /api/v2/remediation/summary` returns the overall severity-by-status breakdown, and `GET /api/v2/remediation/by-product` returns per-product remediation counts. Both endpoints invoke the RemediationService created in Task 3 and follow the existing endpoint registration pattern.

## Files to Create
- `modules/fundamental/src/remediation/endpoints/mod.rs` — Route registration for `/api/v2/remediation` mounting the summary and by-product handlers
- `modules/fundamental/src/remediation/endpoints/summary.rs` — `GET /api/v2/remediation/summary` handler returning `RemediationSummary` as JSON
- `modules/fundamental/src/remediation/endpoints/by_product.rs` — `GET /api/v2/remediation/by-product` handler returning `Vec<ProductRemediation>` as JSON, with optional pagination

## Files to Modify
- `modules/fundamental/src/remediation/mod.rs` — Add `pub mod endpoints;` to expose the endpoints module
- `server/src/main.rs` — Mount the remediation module routes alongside existing module routes

## API Changes
- `GET /api/v2/remediation/summary` — NEW: Returns `RemediationSummary` with aggregate counts by severity and status
- `GET /api/v2/remediation/by-product` — NEW: Returns `Vec<ProductRemediation>` with per-product breakdown, supports pagination via query parameters

## Implementation Notes
- Follow the endpoint registration pattern in `modules/fundamental/src/sbom/endpoints/mod.rs` for route definition and in `modules/fundamental/src/sbom/endpoints/list.rs` and `modules/fundamental/src/sbom/endpoints/get.rs` for handler implementation.
- Mount routes in `server/src/main.rs` following the same pattern used for sbom, advisory, and search modules.
- The summary handler calls `RemediationService::get_summary()` and returns the result as JSON.
- The by-product handler calls `RemediationService::get_by_product()` and wraps the result in `PaginatedResults<ProductRemediation>` from `common/src/model/paginated.rs` to support large portfolios (>50 products) per customer considerations.
- Both handlers return `Result<Json<T>, AppError>` per the error handling convention.
- Consider adding `tower-http` caching middleware configuration for these endpoints, following the caching pattern used by existing endpoints.
- Per Key Conventions (Endpoint registration): each module's `endpoints/mod.rs` registers routes; `server/main.rs` mounts all modules.
  Applies: task creates `modules/fundamental/src/remediation/endpoints/mod.rs` matching the convention's `.rs` endpoint file scope.
- Per Key Conventions (Response types): list endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`.
  Applies: task creates `modules/fundamental/src/remediation/endpoints/by_product.rs` matching the convention's `.rs` file scope.
- Per Key Conventions (Caching): uses `tower-http` caching middleware; cache configuration in endpoint route builders.
  Applies: task creates `modules/fundamental/src/remediation/endpoints/mod.rs` matching the convention's `.rs` endpoint file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Route registration pattern for module endpoints
- `modules/fundamental/src/sbom/endpoints/list.rs` — List endpoint handler pattern with pagination
- `modules/fundamental/src/sbom/endpoints/get.rs` — Single-item endpoint handler pattern
- `common/src/model/paginated.rs::PaginatedResults` — Pagination response wrapper for the by-product endpoint
- `common/src/error.rs::AppError` — Error type implementing IntoResponse for Axum handlers

## Acceptance Criteria
- [ ] `GET /api/v2/remediation/summary` returns a JSON response with severity-by-status aggregation
- [ ] `GET /api/v2/remediation/by-product` returns a JSON response with per-product breakdown
- [ ] By-product endpoint supports pagination (offset/limit query parameters)
- [ ] Both endpoints return appropriate error responses (500) when the service layer fails
- [ ] Routes are mounted in `server/src/main.rs` and accessible at the correct paths

## Test Requirements
- [ ] Verify `GET /api/v2/remediation/summary` returns 200 with valid JSON matching `RemediationSummary` shape
- [ ] Verify `GET /api/v2/remediation/by-product` returns 200 with valid JSON matching paginated `ProductRemediation` shape
- [ ] Verify both endpoints return appropriate error codes for internal errors

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9006 from main
- Depends on: Task 3 — Add remediation aggregation service

## Parent Epic
TC-9006: trustify-backend
