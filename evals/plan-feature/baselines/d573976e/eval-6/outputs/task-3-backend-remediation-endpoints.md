# Task 3 — Add remediation REST API endpoints

## Repository
trustify-backend

## Target Branch
TC-9006

## Description
Add the HTTP endpoints for the remediation module: `GET /api/v2/remediation/summary` and `GET /api/v2/remediation/by-product`. These endpoints expose the aggregation service created in Task 2 through the Axum REST API, following the established endpoint registration pattern.

## Files to Create
- `modules/fundamental/src/remediation/endpoints/mod.rs` — route registration for `/api/v2/remediation` paths
- `modules/fundamental/src/remediation/endpoints/summary.rs` — handler for `GET /api/v2/remediation/summary`
- `modules/fundamental/src/remediation/endpoints/by_product.rs` — handler for `GET /api/v2/remediation/by-product`

## Files to Modify
- `server/src/main.rs` — mount the remediation module routes alongside existing modules

## API Changes
- `GET /api/v2/remediation/summary` — NEW: returns aggregated vulnerability counts by severity (Critical/High/Medium/Low) x status (Open/In Progress/Resolved)
- `GET /api/v2/remediation/by-product` — NEW: returns per-product remediation breakdown with total, open, and resolved counts; supports pagination via `PaginatedResults<ProductRemediation>`

## Implementation Notes
- Follow the endpoint registration pattern in `modules/fundamental/src/sbom/endpoints/mod.rs`: define routes in `endpoints/mod.rs` and register them in `server/src/main.rs`.
- Each handler function should call the corresponding `RemediationService` method and return the result.
- The `summary` endpoint returns a single `RemediationSummary` object (not paginated).
- The `by-product` endpoint returns `PaginatedResults<ProductRemediation>` using the wrapper from `common/src/model/paginated.rs`, supporting offset/limit query parameters via `common/src/db/query.rs`.
- All handlers must return `Result<T, AppError>` with `.context()` wrapping per `common/src/error.rs`.
- Consider adding `tower-http` caching middleware configuration on the endpoint route builders, following the caching patterns used by existing endpoints.
- The p95 response time target is < 500ms — ensure endpoint handlers do not add unnecessary overhead beyond the service layer.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/mod.rs` — reference for route registration pattern
- `modules/fundamental/src/sbom/endpoints/list.rs` — reference for paginated list endpoint handler
- `modules/fundamental/src/advisory/endpoints/mod.rs` — reference for route registration with Axum
- `common/src/model/paginated.rs` — `PaginatedResults<T>` response wrapper

## Acceptance Criteria
- [ ] `GET /api/v2/remediation/summary` returns a JSON response with severity x status aggregation
- [ ] `GET /api/v2/remediation/by-product` returns a paginated JSON response with per-product breakdown
- [ ] Both endpoints return `200 OK` for valid requests
- [ ] Both endpoints return appropriate error responses for failures
- [ ] Routes are mounted in `server/src/main.rs`

## Test Requirements
- [ ] Integration test in `tests/api/remediation.rs` for `GET /api/v2/remediation/summary` verifying correct response shape and status code
- [ ] Integration test for `GET /api/v2/remediation/by-product` verifying pagination and response shape
- [ ] Integration test verifying empty-data scenario returns valid empty response (not error)
- [ ] Follow the `assert_eq!(resp.status(), StatusCode::OK)` pattern from `tests/api/sbom.rs`

## Verification Commands
- `cargo test --test api remediation` — all remediation endpoint integration tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9006 from main
- Depends on: Task 2 — Add remediation service and model layer
