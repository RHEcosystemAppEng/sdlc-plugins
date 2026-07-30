## Repository
trustify-backend

## Target Branch
main

## Description
Add REST API endpoints for the remediation aggregation data. Implement `GET /api/v2/remediation/summary` (returns aggregated counts by severity and status) and `GET /api/v2/remediation/by-product` (returns per-product remediation breakdown). Register the endpoint routes and mount them in the server application.

## Files to Create
- `modules/fundamental/src/remediation/endpoints/mod.rs` — route registration for `/api/v2/remediation`, configures summary and by-product sub-routes
- `modules/fundamental/src/remediation/endpoints/summary.rs` — handler for `GET /api/v2/remediation/summary`
- `modules/fundamental/src/remediation/endpoints/by_product.rs` — handler for `GET /api/v2/remediation/by-product`

## Files to Modify
- `modules/fundamental/src/remediation/mod.rs` — add `pub mod endpoints;` to expose the endpoints module
- `server/src/main.rs` — mount the remediation routes alongside existing module routes

## API Changes
- `GET /api/v2/remediation/summary` — NEW: returns `RemediationSummary[]` grouped by severity (Critical/High/Medium/Low) x status (Open/In Progress/Resolved) with count per group
- `GET /api/v2/remediation/by-product` — NEW: returns `PaginatedResults<ProductRemediation>` with per-product total, open, in_progress, resolved counts

## Implementation Notes
- Follow the endpoint registration pattern: each module's `endpoints/mod.rs` registers routes and `server/main.rs` mounts all modules. See `modules/fundamental/src/sbom/endpoints/mod.rs` for the route registration pattern and `server/src/main.rs` for how routes are mounted.
  Per CONVENTIONS.md §Endpoint Registration: register routes in endpoints/mod.rs and mount in server/main.rs.
  Applies: task creates `modules/fundamental/src/remediation/endpoints/mod.rs` matching the convention's `.rs` endpoint file scope.
- Error handling: all handlers must return `Result<T, AppError>` with `.context()` wrapping. See `modules/fundamental/src/sbom/endpoints/get.rs` for the established pattern.
  Per CONVENTIONS.md §Error Handling: use `Result<T, AppError>` with `.context()` wrapping.
  Applies: task creates `modules/fundamental/src/remediation/endpoints/summary.rs` matching the convention's `.rs` file scope.
- Response types: the by-product endpoint should return `PaginatedResults<ProductRemediation>` from `common/src/model/paginated.rs` for consistency with existing list endpoints.
  Per CONVENTIONS.md §Response Types: list endpoints return `PaginatedResults<T>`.
  Applies: task creates `modules/fundamental/src/remediation/endpoints/by_product.rs` matching the convention's `.rs` endpoint file scope.
- Use `common/src/db/query.rs` for any filtering or pagination support on the by-product endpoint.
- Consider adding `tower-http` caching middleware for the summary endpoint since remediation data changes infrequently.
  Per CONVENTIONS.md §Caching: use tower-http caching middleware.
  Applies: task creates `modules/fundamental/src/remediation/endpoints/mod.rs` matching the convention's `.rs` endpoint file scope.
- Non-functional requirement: summary endpoint p95 < 500ms — ensure the handler delegates to efficient service-layer aggregation.
- Per docs/constraints.md §5.3: follow patterns referenced in Implementation Notes.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration pattern for a domain module
- `modules/fundamental/src/sbom/endpoints/list.rs` — handler pattern for list/aggregation endpoints returning PaginatedResults
- `common/src/model/paginated.rs::PaginatedResults<T>` — response wrapper for list endpoints
- `common/src/db/query.rs` — shared query filtering and pagination helpers

## Acceptance Criteria
- [ ] `GET /api/v2/remediation/summary` returns 200 with aggregated remediation counts by severity and status
- [ ] `GET /api/v2/remediation/by-product` returns 200 with per-product remediation breakdown in PaginatedResults format
- [ ] Endpoints are mounted and accessible via the server
- [ ] Error responses follow the AppError convention

## Test Requirements
- [ ] Handler returns correct JSON structure for summary endpoint
- [ ] Handler returns correct JSON structure for by-product endpoint
- [ ] Handlers return appropriate error responses for database failures

## Verification Commands
- `cargo check -p trustify-server` — server compiles with new routes
- `curl http://localhost:8080/api/v2/remediation/summary` — returns valid JSON response

## Dependencies
- Depends on: Task 1 — Add remediation model and aggregation service
