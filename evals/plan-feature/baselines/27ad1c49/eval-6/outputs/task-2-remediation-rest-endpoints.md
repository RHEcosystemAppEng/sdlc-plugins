## Repository
trustify-backend

## Target Branch
main

## Parent Epic
TC-9006: trustify-backend

## Description
Add REST endpoints for the remediation module: `GET /api/v2/remediation/summary` returning aggregated vulnerability counts by severity and status, and `GET /api/v2/remediation/by-product` returning per-product remediation breakdowns. Both endpoints delegate to the `RemediationService` created in Task 1 and follow the existing endpoint registration pattern.

## Files to Create
- `modules/fundamental/src/remediation/endpoints/mod.rs` — Route registration for `/api/v2/remediation`, mounting summary and by-product handlers
- `modules/fundamental/src/remediation/endpoints/summary.rs` — Handler for `GET /api/v2/remediation/summary`, returns `RemediationSummary` as JSON
- `modules/fundamental/src/remediation/endpoints/by_product.rs` — Handler for `GET /api/v2/remediation/by-product`, returns `PaginatedResults<ProductRemediation>` with optional query parameters for filtering and pagination

## Files to Modify
- `server/src/main.rs` — Mount the remediation module routes alongside existing module routes (sbom, advisory, package, search)

## API Changes
- `GET /api/v2/remediation/summary` — NEW: returns aggregated remediation counts grouped by severity (Critical/High/Medium/Low) and status (Open/In Progress/Resolved)
- `GET /api/v2/remediation/by-product` — NEW: returns per-product remediation breakdown with total, open, in-progress, and resolved counts; supports pagination query parameters

## Implementation Notes
Follow the endpoint patterns established in the advisory and sbom modules.

- Register routes in `modules/fundamental/src/remediation/endpoints/mod.rs` using the same `Router` pattern as `modules/fundamental/src/advisory/endpoints/mod.rs`
- Each handler should extract the database pool from Axum state and call the corresponding `RemediationService` method
- The summary handler returns `Json<RemediationSummary>` directly
- The by-product handler should accept pagination query parameters and return `Json<PaginatedResults<ProductRemediation>>`, following the pattern in `modules/fundamental/src/sbom/endpoints/list.rs`
- Mount routes in `server/src/main.rs` alongside existing `.merge()` calls for sbom, advisory, package, and search modules
- Apply `tower-http` caching middleware to the summary endpoint with a short TTL (e.g., 60s) since the data changes infrequently, following the caching pattern noted in the repository conventions
- The summary endpoint must meet the p95 < 500ms response time requirement

Per CONVENTIONS.md §Endpoint Registration: register routes in endpoints/mod.rs and mount in server/main.rs. Applies: task creates `modules/fundamental/src/remediation/endpoints/mod.rs` matching the convention's `.rs` scope.

Per CONVENTIONS.md §Response Types: return `PaginatedResults<T>` from list endpoints. Applies: task creates `modules/fundamental/src/remediation/endpoints/by_product.rs` matching the convention's `.rs` scope.

Per CONVENTIONS.md §Caching: apply tower-http caching middleware to endpoints. Applies: task creates `modules/fundamental/src/remediation/endpoints/mod.rs` matching the convention's `.rs` scope.

## Reuse Candidates
- `modules/fundamental/src/advisory/endpoints/mod.rs` — Endpoint route registration pattern; replicate for remediation routes
- `modules/fundamental/src/sbom/endpoints/list.rs` — List endpoint with pagination; use as template for by-product handler
- `common/src/db/query.rs` — Query parameter extraction helpers for pagination and filtering

## Acceptance Criteria
- [ ] `GET /api/v2/remediation/summary` returns 200 with JSON body containing severity-by-status counts
- [ ] `GET /api/v2/remediation/by-product` returns 200 with paginated JSON body containing per-product breakdown
- [ ] Both endpoints return appropriate error responses (500) when database errors occur
- [ ] By-product endpoint supports pagination query parameters (offset, limit)
- [ ] Routes are mounted and accessible from the main server
- [ ] Summary endpoint response time meets p95 < 500ms requirement

## Test Requirements
- [ ] Integration test for `GET /api/v2/remediation/summary` verifying correct JSON structure and status code 200
- [ ] Integration test for `GET /api/v2/remediation/by-product` verifying paginated response format
- [ ] Integration test verifying pagination parameters are respected in by-product endpoint
- [ ] Integration tests placed in `tests/api/` following existing test patterns (e.g., `tests/api/advisory.rs`)

## Dependencies
- Depends on: Task 1 — Create remediation module with model structs and aggregation service
