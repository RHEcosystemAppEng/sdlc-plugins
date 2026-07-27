## Repository
trustify-backend

## Target Branch
TC-9006

## Description
Add REST API endpoints for the remediation aggregation service created in Task 2. This task creates the HTTP handler layer with two endpoints: `GET /api/v2/remediation/summary` for aggregated counts by severity and status, and `GET /api/v2/remediation/by-product` for per-product remediation breakdown. Endpoints are registered following the established route mounting pattern.

## Files to Create
- `modules/fundamental/src/remediation/endpoints/mod.rs` -- route registration for /api/v2/remediation, defines router with summary and by_product handlers
- `modules/fundamental/src/remediation/endpoints/summary.rs` -- GET /api/v2/remediation/summary handler, calls RemediationService.get_summary()
- `modules/fundamental/src/remediation/endpoints/by_product.rs` -- GET /api/v2/remediation/by-product handler, calls RemediationService.get_by_product()

## Files to Modify
- `server/src/main.rs` -- mount the remediation module routes alongside existing module routes (sbom, advisory, search)

## API Changes
- `GET /api/v2/remediation/summary` -- NEW: returns aggregated remediation counts grouped by severity (Critical/High/Medium/Low) x status (Open/In Progress/Resolved). Response shape: `{ items: [{ severity: string, status: string, count: number }] }`
- `GET /api/v2/remediation/by-product` -- NEW: returns per-product remediation breakdown. Response shape: `{ items: [{ product_name: string, total: number, open: number, in_progress: number, resolved: number }] }`

## Implementation Notes
- Follow the endpoint registration pattern from `modules/fundamental/src/sbom/endpoints/mod.rs` and `modules/fundamental/src/advisory/endpoints/mod.rs` for route definition and mounting.
  Per CONVENTIONS.md: each module's endpoints/mod.rs registers routes; server/main.rs mounts all modules.
  Applies: task creates `modules/fundamental/src/remediation/endpoints/mod.rs` matching the convention's Rust endpoint module scope.
- Handlers return `Result<Json<T>, AppError>` following the established error handling pattern.
  Per CONVENTIONS.md: all handlers return Result<T, AppError> with .context() wrapping.
  Applies: task creates `modules/fundamental/src/remediation/endpoints/summary.rs` matching the convention's Rust file scope.
- For the by-product endpoint, support pagination using `PaginatedResults<T>` from `common/src/model/paginated.rs` to handle portfolios with many products (>50 products per the customer considerations).
  Per CONVENTIONS.md: list endpoints return PaginatedResults<T> from common/src/model/paginated.rs.
  Applies: task creates `modules/fundamental/src/remediation/endpoints/by_product.rs` matching the convention's Rust endpoint file scope.
- Consider adding `tower-http` caching middleware configuration for the summary endpoint since the data can tolerate short-term staleness (cache TTL of 30-60 seconds recommended for p95 < 500ms target).
  Per CONVENTIONS.md: uses tower-http caching middleware; cache configuration in endpoint route builders.
  Applies: task creates `modules/fundamental/src/remediation/endpoints/mod.rs` matching the convention's Rust endpoint file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/mod.rs` -- route registration pattern for /api/v2/sbom; follow as template for remediation route registration
- `modules/fundamental/src/sbom/endpoints/list.rs` -- GET handler returning list data; reference for handler structure
- `modules/fundamental/src/advisory/endpoints/mod.rs` -- route registration pattern for /api/v2/advisory; another template reference
- `common/src/model/paginated.rs` -- PaginatedResults<T> response wrapper for list endpoints

## Acceptance Criteria
- [ ] GET /api/v2/remediation/summary returns JSON with aggregated counts by severity x status
- [ ] GET /api/v2/remediation/by-product returns JSON with per-product breakdown including total, open, in_progress, resolved counts
- [ ] By-product endpoint supports pagination for large product portfolios
- [ ] Routes are registered in server/src/main.rs and accessible
- [ ] Endpoints return proper HTTP error responses (400, 500) with AppError formatting

## Test Requirements
- [ ] Verify GET /api/v2/remediation/summary returns 200 with expected JSON structure
- [ ] Verify GET /api/v2/remediation/by-product returns 200 with expected JSON structure
- [ ] Verify by-product endpoint pagination (offset, limit parameters)
- [ ] Verify error handling returns appropriate status codes

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9006 from main
- Depends on: Task 2 -- Add remediation model types and aggregation service
