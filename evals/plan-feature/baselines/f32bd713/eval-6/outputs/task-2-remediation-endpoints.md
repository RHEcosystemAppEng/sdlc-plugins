## Repository
trustify-backend

## Parent Epic
TC-9007 (TC-9006: trustify-backend)

## Target Branch
main

## Description
Add the REST API endpoints for the vulnerability remediation tracking dashboard. This task creates `GET /api/v2/remediation/summary` (aggregated counts by severity x status) and `GET /api/v2/remediation/by-product` (per-product remediation breakdown), wiring them through the Axum router to the RemediationService created in Task 1.

## Files to Create
- `modules/fundamental/src/remediation/endpoints/mod.rs` -- route registration for `/api/v2/remediation` subroutes
- `modules/fundamental/src/remediation/endpoints/summary.rs` -- GET /api/v2/remediation/summary handler
- `modules/fundamental/src/remediation/endpoints/by_product.rs` -- GET /api/v2/remediation/by-product handler

## Files to Modify
- `server/src/main.rs` -- mount the remediation module routes alongside existing sbom, advisory, and search routes
- `modules/fundamental/src/remediation/mod.rs` -- add `pub mod endpoints;` declaration

## API Changes
- `GET /api/v2/remediation/summary` -- NEW: returns aggregated remediation counts grouped by severity (Critical/High/Medium/Low) x status (Open/In Progress/Resolved). Response shape: `{ groups: [{ severity: string, status: string, count: number }] }`
- `GET /api/v2/remediation/by-product` -- NEW: returns per-product remediation breakdown with pagination. Response shape: `PaginatedResults<RemediationByProduct>` where each item contains `{ product: string, total: number, open: number, in_progress: number, resolved: number }`

## Implementation Notes
- Register routes in `endpoints/mod.rs` following the pattern established in `modules/fundamental/src/sbom/endpoints/mod.rs` -- each endpoint function is defined in its own file and registered via `.route()` calls.
  Per CONVENTIONS.md section Endpoint Registration: each module's endpoints/mod.rs registers routes; server/main.rs mounts all modules.
  Applies: task creates `modules/fundamental/src/remediation/endpoints/mod.rs` matching the convention's endpoint registration scope.
- Mount the remediation routes in `server/src/main.rs` following the existing pattern where each module's routes are merged into the main router.
- The summary endpoint requires no query parameters and returns the full aggregation.
- The by-product endpoint should accept pagination parameters (offset, limit) and return `PaginatedResults<RemediationByProduct>` consistent with other list endpoints.
  Per CONVENTIONS.md section Response Types: list endpoints return PaginatedResults<T> from common/src/model/paginated.rs.
  Applies: task creates `modules/fundamental/src/remediation/endpoints/by_product.rs` matching the convention's Rust endpoint scope.
- Both handlers must return `Result<Json<T>, AppError>` with `.context()` wrapping.
- Consider adding `tower-http` caching middleware configuration for the summary endpoint given the p95 < 500ms requirement.
  Per CONVENTIONS.md section Caching: uses tower-http caching middleware; cache configuration in endpoint route builders.
  Applies: task creates `modules/fundamental/src/remediation/endpoints/summary.rs` matching the convention's Rust endpoint scope.
- The endpoints must handle up to 10,000 tracked vulnerabilities without performance degradation.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/mod.rs` -- route registration pattern for the remediation module
- `modules/fundamental/src/sbom/endpoints/list.rs` -- list endpoint handler pattern with pagination
- `modules/fundamental/src/advisory/endpoints/get.rs` -- single-resource endpoint handler pattern
- `common/src/db/query.rs` -- shared filtering, pagination, and sorting helpers
- `common/src/model/paginated.rs::PaginatedResults<T>` -- paginated response wrapper

## Acceptance Criteria
- [ ] `GET /api/v2/remediation/summary` returns HTTP 200 with correct aggregation by severity x status
- [ ] `GET /api/v2/remediation/by-product` returns HTTP 200 with per-product breakdown and pagination metadata
- [ ] Both endpoints are accessible from the main Axum router
- [ ] Error cases return appropriate HTTP status codes with `AppError` responses
- [ ] p95 response time < 500ms with up to 10,000 tracked vulnerabilities (design-level; verified in Task 3)

## Test Requirements
- [ ] Endpoint compiles and is reachable at the documented path
- [ ] Summary endpoint returns well-formed JSON matching the documented response shape
- [ ] By-product endpoint supports offset/limit pagination parameters
- [ ] Both endpoints handle database errors gracefully

## Verification Commands
- `cargo build -p trustify-server` -- verify the server compiles with new routes mounted
- `curl http://localhost:8080/api/v2/remediation/summary` -- verify summary endpoint responds (manual smoke test)
- `curl http://localhost:8080/api/v2/remediation/by-product` -- verify by-product endpoint responds (manual smoke test)

## Dependencies
- Depends on: Task 1 -- Add remediation data models and aggregation service
