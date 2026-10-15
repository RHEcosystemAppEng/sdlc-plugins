## Repository
trustify-backend

## Target Branch
main

## Description
Add the REST API endpoints for the vulnerability remediation tracking dashboard (TC-9006). This task wires up the RemediationService (from Task 1) to two HTTP endpoints: GET /api/v2/remediation/summary for aggregated severity-by-status counts, and GET /api/v2/remediation/by-product for per-product remediation breakdowns. Both endpoints are registered in the Axum router and mounted in the server.

## Files to Create
- `modules/fundamental/src/remediation/endpoints/mod.rs` — Route registration for /api/v2/remediation, mounts summary and by-product handlers
- `modules/fundamental/src/remediation/endpoints/summary.rs` — GET /api/v2/remediation/summary handler
- `modules/fundamental/src/remediation/endpoints/by_product.rs` — GET /api/v2/remediation/by-product handler

## Files to Modify
- `modules/fundamental/src/remediation/mod.rs` — Add endpoints submodule export
- `server/src/main.rs` — Mount remediation routes alongside existing module routes

## API Changes
- `GET /api/v2/remediation/summary` — NEW: Returns aggregated remediation counts grouped by severity (Critical/High/Medium/Low) and status (Open/In Progress/Resolved)
- `GET /api/v2/remediation/by-product` — NEW: Returns per-product remediation breakdown with total, open, in-progress, and resolved counts; supports pagination via query parameters

## Implementation Notes
- Per CONVENTIONS.md §Module pattern: follow the `endpoints/` structure established by existing modules (sbom, advisory, package) with a `mod.rs` for route registration and separate handler files.
  Applies: task creates `modules/fundamental/src/remediation/endpoints/mod.rs` matching the convention's module structure scope.
- Per CONVENTIONS.md §Error handling: all handlers must return `Result<Json<T>, AppError>` with `.context()` wrapping.
  Applies: task creates `modules/fundamental/src/remediation/endpoints/summary.rs` matching the convention's `.rs` handler scope.
- Per CONVENTIONS.md §Endpoint registration: register routes in `endpoints/mod.rs` and mount in `server/src/main.rs`, following the pattern used by sbom and advisory modules.
  Applies: task modifies `server/src/main.rs` matching the convention's endpoint registration scope.
- Per CONVENTIONS.md §Response types: the by-product endpoint must return `PaginatedResults<ProductRemediation>`.
  Applies: task creates `modules/fundamental/src/remediation/endpoints/by_product.rs` matching the convention's `.rs` endpoint scope.
- Per CONVENTIONS.md §Caching: consider adding `tower-http` caching middleware for the summary endpoint to meet the p95 < 500ms NFR.
  Applies: task creates `modules/fundamental/src/remediation/endpoints/mod.rs` matching the convention's `.rs` endpoint scope.
- Reference `modules/fundamental/src/sbom/endpoints/mod.rs` for route registration pattern.
- Reference `modules/fundamental/src/sbom/endpoints/list.rs` for paginated list handler pattern.
- The summary endpoint should accept optional query parameters for date range filtering (for the 30-day trend chart).
- The by-product endpoint should accept pagination parameters consistent with other list endpoints.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Route registration pattern for Axum; follow the same router builder approach
- `modules/fundamental/src/sbom/endpoints/list.rs` — Paginated list handler pattern; reference for by-product endpoint
- `modules/fundamental/src/advisory/endpoints/mod.rs` — Alternative route registration reference
- `common/src/model/paginated.rs::PaginatedResults<T>` — Response wrapper for paginated by-product endpoint

## Acceptance Criteria
- [ ] GET /api/v2/remediation/summary returns 200 with a JSON body containing severity x status counts
- [ ] GET /api/v2/remediation/by-product returns 200 with a paginated JSON body of per-product breakdowns
- [ ] Endpoints are registered in server/src/main.rs and accessible when the server starts
- [ ] Error responses use AppError and return appropriate HTTP status codes
- [ ] Summary endpoint response time target: p95 < 500ms (non-functional requirement)

## Test Requirements
- [ ] Verify GET /api/v2/remediation/summary returns valid JSON with expected structure
- [ ] Verify GET /api/v2/remediation/by-product returns paginated results
- [ ] Verify endpoints return appropriate error responses for invalid parameters
- [ ] Verify routes are properly mounted in the server

## Verification Commands
- `cargo build -p trustify-server` — Server builds with new routes
- `cargo run -p trustify-server &` then `curl http://localhost:8080/api/v2/remediation/summary` — Returns valid JSON response

## Dependencies
- Depends on: Task 1 — Add remediation model types and aggregation service
