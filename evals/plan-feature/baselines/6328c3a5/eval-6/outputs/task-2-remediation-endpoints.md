## Repository
trustify-backend

## Target Branch
main

## Description
Add the REST endpoints for the remediation aggregation API. Register two new routes under `/api/v2/remediation/`: a summary endpoint returning aggregated counts by severity and status, and a by-product endpoint returning per-product remediation breakdowns. Mount the remediation routes in the Axum server.

## Files to Create
- `modules/fundamental/src/remediation/endpoints/mod.rs` — route registration for `/api/v2/remediation`, defines router with summary and by-product handlers
- `modules/fundamental/src/remediation/endpoints/summary.rs` — `GET /api/v2/remediation/summary` handler calling `RemediationService::get_summary()`
- `modules/fundamental/src/remediation/endpoints/by_product.rs` — `GET /api/v2/remediation/by-product` handler calling `RemediationService::get_by_product()`

## Files to Modify
- `server/src/main.rs` — mount remediation routes in the Axum router alongside existing module routes (sbom, advisory, package, search)

## API Changes
- `GET /api/v2/remediation/summary` — NEW: returns `RemediationSummary` with aggregated counts by severity (Critical/High/Medium/Low) x status (Open/In Progress/Resolved)
- `GET /api/v2/remediation/by-product` — NEW: returns `Vec<ProductRemediation>` with per-product breakdown (product_name, total, open, resolved counts)

## Implementation Notes
- Follow the endpoint registration pattern used by existing modules. See `modules/fundamental/src/sbom/endpoints/mod.rs` for how routes are registered and `server/src/main.rs` for how module routers are mounted.
- Each handler function extracts `RemediationService` from Axum state (same pattern as `SbomService` extraction in `modules/fundamental/src/sbom/endpoints/list.rs`).
- Handlers return `Result<Json<T>, AppError>` following the error handling convention.
- The summary endpoint should support optional query parameters for filtering by date range (for the 30-day trend chart the frontend will use).
- The by-product endpoint may need pagination for large portfolios (>50 products per the customer considerations). Use `PaginatedResults<ProductRemediation>` from `common/src/model/paginated.rs` and accept standard pagination query parameters via `common/src/db/query.rs` helpers.
- Per Key Conventions: endpoint registration follows the pattern in each module's `endpoints/mod.rs`; `server/src/main.rs` mounts all modules.
  Applies: task creates `modules/fundamental/src/remediation/endpoints/mod.rs` matching the convention's `.rs` file scope.
- Per Key Conventions: list endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`.
  Applies: task creates `modules/fundamental/src/remediation/endpoints/by_product.rs` matching the convention's `.rs` file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/mod.rs` — reference implementation for route registration pattern
- `modules/fundamental/src/sbom/endpoints/list.rs` — reference for list endpoint handler with pagination and filtering
- `common/src/model/paginated.rs::PaginatedResults<T>` — paginated response wrapper for the by-product endpoint
- `common/src/db/query.rs` — shared filtering and pagination query builder helpers

## Acceptance Criteria
- [ ] `GET /api/v2/remediation/summary` returns 200 with JSON body containing severity x status aggregation
- [ ] `GET /api/v2/remediation/by-product` returns 200 with JSON body containing per-product breakdown
- [ ] Both endpoints return proper error responses (500 with AppError) on service failures
- [ ] Remediation routes are mounted in `server/src/main.rs`
- [ ] By-product endpoint supports pagination via standard query parameters

## Test Requirements
- [ ] Verify summary endpoint returns correct JSON structure
- [ ] Verify by-product endpoint returns correct JSON structure with pagination
- [ ] Verify error handling returns appropriate status codes

## Verification Commands
- `cargo build` — verify compilation with new endpoints
- `cargo clippy` — verify no linting warnings in new code

## Documentation Updates
- `README.md` — add remediation endpoints to the API endpoint list if one exists

## Dependencies
- Depends on: Task 1 — Create remediation model and service layer
