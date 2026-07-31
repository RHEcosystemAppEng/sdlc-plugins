## Repository
trustify-backend

## Parent Epic
TC-9007 (TC-9006: trustify-backend)

## Priority
Major (inherited from Feature TC-9006)

## Fix Versions
RHTPA 1.5.0 (inherited from Feature TC-9006)

## Target Branch
main

## Description
Create the REST API endpoints for vulnerability remediation tracking. Implement `GET /api/v2/remediation/summary` which returns aggregated vulnerability counts grouped by severity and remediation status, and `GET /api/v2/remediation/by-product` which returns per-product remediation breakdowns. Both endpoints use the RemediationService from Task 1 and follow the existing endpoint patterns.

## Files to Create
- `modules/fundamental/src/remediation/endpoints/mod.rs` — Route registration for /api/v2/remediation, configures summary and by-product sub-routes
- `modules/fundamental/src/remediation/endpoints/summary.rs` — GET /api/v2/remediation/summary handler returning RemediationSummary
- `modules/fundamental/src/remediation/endpoints/by_product.rs` — GET /api/v2/remediation/by-product handler returning PaginatedResults<RemediationByProduct>

## Files to Modify
- `server/src/main.rs` — Mount remediation endpoint routes alongside existing sbom, advisory, and search routes

## API Changes
- `GET /api/v2/remediation/summary` — NEW: Returns aggregated counts grouped by severity (Critical/High/Medium/Low) and status (Open/In Progress/Resolved)
- `GET /api/v2/remediation/by-product` — NEW: Returns per-product remediation breakdown with total, open, and resolved counts; supports pagination

## Implementation Notes
Follow the endpoint pattern in `modules/fundamental/src/sbom/endpoints/mod.rs` for route registration and `modules/fundamental/src/sbom/endpoints/list.rs` for handler structure. Each handler receives the service via Axum state extraction and returns JSON responses.

The by-product endpoint should use `PaginatedResults<T>` from `common/src/model/paginated.rs` to support pagination for large portfolios (>50 products). Apply query helpers from `common/src/db/query.rs` for filtering and sorting parameters.

The summary endpoint must meet p95 < 500ms response time. Consider using SeaORM's `select_with_count()` or raw SQL aggregation for performance.

Mount routes in `server/src/main.rs` following the pattern used by existing modules (sbom, advisory, search).

Per CONVENTIONS.md §Endpoint registration: register routes in endpoints/mod.rs and mount in server/main.rs. Applies: task creates `modules/fundamental/src/remediation/endpoints/mod.rs` matching the convention's `.rs` endpoint scope.

Per CONVENTIONS.md §Response types: list endpoints return PaginatedResults<T>. Applies: task creates `modules/fundamental/src/remediation/endpoints/by_product.rs` matching the convention's `.rs` scope.

## Acceptance Criteria
- [ ] GET /api/v2/remediation/summary returns JSON with severity-by-status aggregation
- [ ] GET /api/v2/remediation/by-product returns PaginatedResults with per-product breakdown
- [ ] By-product endpoint supports pagination parameters
- [ ] Summary endpoint responds within p95 < 500ms for up to 10,000 vulnerabilities
- [ ] Routes are mounted in server/src/main.rs
- [ ] All handlers return Result<T, AppError>

## Test Requirements
- [ ] Verify summary endpoint returns correct JSON structure with severity groupings
- [ ] Verify by-product endpoint returns paginated results
- [ ] Verify error responses for invalid query parameters
- [ ] Verify endpoint routing is correctly registered

## Dependencies
- Depends on: Task 1 — remediation-model-service (provides RemediationService and model types)
