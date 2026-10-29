## Repository
trustify-backend

## Target Branch
main

## Description
Add the HTTP API endpoints for vulnerability remediation data. This task creates two GET endpoints under `/api/v2/remediation/` that expose the aggregation service from Task 1: a summary endpoint returning counts by severity and status, and a by-product endpoint returning per-product remediation breakdowns. Both endpoints follow the existing Axum route registration pattern.

## Files to Create
- `modules/fundamental/src/remediation/endpoints/mod.rs` — route registration for `/api/v2/remediation` path, mounts summary and by-product handlers
- `modules/fundamental/src/remediation/endpoints/summary.rs` — GET /api/v2/remediation/summary handler
- `modules/fundamental/src/remediation/endpoints/by_product.rs` — GET /api/v2/remediation/by-product handler

## Files to Modify
- `server/src/main.rs` — mount the remediation module routes alongside existing module routes

## API Changes
- `GET /api/v2/remediation/summary` — NEW: returns aggregated remediation counts grouped by severity (Critical/High/Medium/Low) and status (Open/In Progress/Resolved)
- `GET /api/v2/remediation/by-product` — NEW: returns per-product remediation breakdown with total, open, and resolved counts; supports pagination and filtering query parameters

## Implementation Notes
Per CONVENTIONS.md §Endpoint Registration: each module's `endpoints/mod.rs` registers routes, and `server/main.rs` mounts all modules. Follow the pattern in `modules/fundamental/src/sbom/endpoints/mod.rs` for route registration.
Applies: task creates `modules/fundamental/src/remediation/endpoints/mod.rs` matching the convention's `.rs` endpoint file scope.

Per CONVENTIONS.md §Error Handling: all handlers must return `Result<T, AppError>` with `.context()` wrapping.
Applies: task creates `modules/fundamental/src/remediation/endpoints/summary.rs` matching the convention's `.rs` file scope.

Per CONVENTIONS.md §Response Types: the by-product endpoint returns a paginated list and must use `PaginatedResults<T>` from `common/src/model/paginated.rs`.
Applies: task creates `modules/fundamental/src/remediation/endpoints/by_product.rs` matching the convention's `.rs` file scope.

Per CONVENTIONS.md §Caching: use `tower-http` caching middleware in endpoint route builders where appropriate. The summary endpoint is a good candidate for short-duration caching given the p95 < 500ms requirement.
Applies: task creates `modules/fundamental/src/remediation/endpoints/mod.rs` matching the convention's `.rs` file scope.

The summary endpoint handler should accept optional query parameters for date range filtering (for the trend-over-time chart on the frontend).

The by-product endpoint handler should accept query parameters for pagination (offset, limit) and optional filtering by product name.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/mod.rs` — reference for route registration pattern and Axum router setup
- `modules/fundamental/src/sbom/endpoints/list.rs` — reference for list endpoint with pagination and filtering
- `modules/fundamental/src/advisory/endpoints/get.rs` — reference for single-resource GET handler pattern
- `common/src/db/query.rs` — shared query parameter extraction for filtering and pagination
- `common/src/model/paginated.rs::PaginatedResults<T>` — paginated response wrapper

## Acceptance Criteria
- [ ] GET /api/v2/remediation/summary returns 200 with aggregated severity x status counts
- [ ] GET /api/v2/remediation/by-product returns 200 with paginated product remediation entries
- [ ] Both endpoints return proper error responses (AppError) on failure
- [ ] Remediation routes are mounted in server/main.rs
- [ ] Summary endpoint response time is p95 < 500ms
- [ ] By-product endpoint supports pagination via offset and limit query parameters

## Test Requirements
- [ ] Verify summary endpoint returns correct JSON structure with severity x status matrix
- [ ] Verify by-product endpoint returns paginated results with correct product entry structure
- [ ] Verify both endpoints return 200 with empty results when no vulnerability data exists
- [ ] Verify by-product endpoint pagination works correctly (offset, limit, total count)

## Dependencies
- Depends on: Task 1 — Add remediation model and aggregation service
