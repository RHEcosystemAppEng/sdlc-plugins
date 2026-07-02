# Task 2: Add remediation REST endpoints

Parent Epic: TC-9006: trustify-backend

## Repository
trustify-backend

## Target Branch
main

## Description
Add two REST endpoints for the remediation module: `GET /api/v2/remediation/summary` returns portfolio-wide remediation counts grouped by severity and status, and `GET /api/v2/remediation/by-product` returns a paginated per-product remediation breakdown. Register the remediation routes in the server's main router.

## Files to Create
- `modules/fundamental/src/remediation/endpoints/mod.rs` — route registration function that configures both remediation endpoints under `/api/v2/remediation`
- `modules/fundamental/src/remediation/endpoints/summary.rs` — handler for `GET /api/v2/remediation/summary`
- `modules/fundamental/src/remediation/endpoints/by_product.rs` — handler for `GET /api/v2/remediation/by-product`, accepts optional query parameters for filtering and pagination

## Files to Modify
- `server/src/main.rs` — mount the remediation module routes alongside existing module routes (sbom, advisory, package, search)

## API Changes
- `GET /api/v2/remediation/summary` — NEW: returns `RemediationSummary` with aggregated counts by severity and status
- `GET /api/v2/remediation/by-product` — NEW: returns `PaginatedResults<ProductRemediation>` with per-product remediation breakdown; accepts query params for pagination (`offset`, `limit`) and optional filtering (`product_name`)

## Implementation Notes
- Per CONVENTIONS.md §Endpoint Registration: create an `endpoints/mod.rs` that registers routes and mount them in `server/src/main.rs`. Follow the pattern in `modules/fundamental/src/sbom/endpoints/mod.rs` and its mounting in `server/src/main.rs`. Applies: task creates `modules/fundamental/src/remediation/endpoints/mod.rs` matching the convention's .rs endpoint scope.
- Per CONVENTIONS.md §Error Handling: all handlers must return `Result<T, AppError>` and wrap errors with `.context()`. Applies: task creates `modules/fundamental/src/remediation/endpoints/summary.rs` matching the convention's .rs scope.
- Per CONVENTIONS.md §Response Types: the `by-product` endpoint must return `PaginatedResults<ProductRemediation>` from `common/src/model/paginated.rs`. Applies: task creates `modules/fundamental/src/remediation/endpoints/by_product.rs` matching the convention's .rs scope.
- Per CONVENTIONS.md §Caching: configure `tower-http` caching middleware on the summary endpoint route builder since summary data is suitable for short-lived caching (e.g., 60s). Applies: task creates `modules/fundamental/src/remediation/endpoints/summary.rs` matching the convention's .rs endpoint scope.
- The summary handler calls `RemediationService::summary()` and serializes the result as JSON.
- The by-product handler parses pagination query parameters, calls `RemediationService::by_product()`, and returns paginated JSON.
- Reference `modules/fundamental/src/sbom/endpoints/list.rs` for the pagination query parameter extraction pattern.
- Reference `modules/fundamental/src/advisory/endpoints/mod.rs` for route registration pattern.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration pattern; reuse the same `Router::new().route()` structure
- `modules/fundamental/src/sbom/endpoints/list.rs` — pagination query parameter extraction pattern; reuse for by-product endpoint
- `common/src/model/paginated.rs::PaginatedResults` — paginated response wrapper; reuse as return type for by-product endpoint
- `common/src/error.rs::AppError` — error type with IntoResponse; reuse for all handler error returns

## Acceptance Criteria
- [ ] `GET /api/v2/remediation/summary` returns 200 with JSON containing severity/status count breakdown
- [ ] `GET /api/v2/remediation/by-product` returns 200 with paginated JSON containing per-product remediation data
- [ ] `GET /api/v2/remediation/by-product` supports `offset` and `limit` query parameters for pagination
- [ ] Both endpoints return proper error responses (400, 500) with `AppError` formatting
- [ ] Remediation routes are mounted in `server/src/main.rs` and accessible at `/api/v2/remediation/*`
- [ ] Summary endpoint has caching middleware configured

## Dependencies
- Depends on: Task 1 — Add remediation models and aggregation service
