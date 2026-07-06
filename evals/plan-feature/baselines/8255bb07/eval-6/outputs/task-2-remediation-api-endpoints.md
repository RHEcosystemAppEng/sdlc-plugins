## Repository
trustify-backend

## Target Branch
main

## Parent Epic
TC-9007 (TC-9006: trustify-backend)

## Description
Add the REST API endpoints for the remediation module and register them in the server route configuration. This task exposes the aggregation service created in Task 1 through two new endpoints: `GET /api/v2/remediation/summary` for severity-by-status aggregation and `GET /api/v2/remediation/by-product` for per-product remediation breakdown. Both endpoints support query parameter filtering. Integration tests verify the endpoints against a real test database.

## Files to Create
- `modules/fundamental/src/remediation/endpoints/mod.rs` — Route registration for /api/v2/remediation, mounts summary and by-product handlers
- `modules/fundamental/src/remediation/endpoints/summary.rs` — GET /api/v2/remediation/summary handler
- `modules/fundamental/src/remediation/endpoints/by_product.rs` — GET /api/v2/remediation/by-product handler
- `tests/api/remediation.rs` — Integration tests for both remediation endpoints

## Files to Modify
- `server/src/main.rs` — Mount remediation module routes alongside existing module routes

## API Changes
- `GET /api/v2/remediation/summary` — NEW: Returns aggregated remediation counts grouped by severity (Critical/High/Medium/Low) and status (Open/In Progress/Resolved)
- `GET /api/v2/remediation/by-product` — NEW: Returns per-product remediation breakdown with total, open, and resolved counts for each product

## Implementation Notes
Follow the endpoint registration pattern established by existing modules. Each module's `endpoints/mod.rs` registers routes and `server/main.rs` mounts all modules.

Per CONVENTIONS.md §Endpoint registration: create `endpoints/mod.rs` with route registration function, mount in `server/src/main.rs` alongside existing modules (sbom, advisory, package, search).
Applies: task creates `modules/fundamental/src/remediation/endpoints/mod.rs` matching the convention's `.rs` file scope.

Per CONVENTIONS.md §Error handling: all endpoint handlers must return `Result<T, AppError>` with `.context()` wrapping.
Applies: task creates `modules/fundamental/src/remediation/endpoints/summary.rs` matching the convention's `.rs` file scope.

Per CONVENTIONS.md §Testing: integration tests go in `tests/api/` and hit a real PostgreSQL test database using the `assert_eq!(resp.status(), StatusCode::OK)` pattern.
Applies: task creates `tests/api/remediation.rs` matching the convention's `.rs` test file scope.

Per CONVENTIONS.md §Caching: configure `tower-http` caching middleware on the endpoint route builders for appropriate cache control.
Applies: task creates `modules/fundamental/src/remediation/endpoints/mod.rs` matching the convention's `.rs` file scope.

Reference `modules/fundamental/src/sbom/endpoints/mod.rs` for route registration pattern and `modules/fundamental/src/sbom/endpoints/list.rs` for handler structure with query parameter extraction. Reference `tests/api/sbom.rs` for integration test patterns.

The summary endpoint should accept optional query parameters for filtering by severity and status. The by-product endpoint should accept optional pagination parameters. Both endpoints should return JSON responses.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Route registration pattern to follow for remediation endpoint mounting
- `modules/fundamental/src/sbom/endpoints/list.rs` — Handler structure with query parameter extraction and paginated response
- `modules/fundamental/src/advisory/endpoints/list.rs` — Alternative handler reference showing list endpoint pattern
- `tests/api/sbom.rs` — Integration test pattern for endpoint testing with test database
- `common/src/db/query.rs` — Query parameter extraction helpers for filtering and pagination

## Acceptance Criteria
- [ ] GET /api/v2/remediation/summary returns JSON with severity-by-status aggregation
- [ ] GET /api/v2/remediation/by-product returns JSON with per-product breakdown including total, open, and resolved counts
- [ ] Both endpoints return HTTP 200 with valid JSON on success
- [ ] Both endpoints return appropriate error responses (500) on service failures
- [ ] Routes are registered and accessible from the server
- [ ] Summary endpoint response time meets p95 < 500ms target for up to 10,000 vulnerabilities

## Test Requirements
- [ ] Integration test: GET /api/v2/remediation/summary returns 200 with expected aggregation structure
- [ ] Integration test: GET /api/v2/remediation/by-product returns 200 with expected per-product structure
- [ ] Integration test: summary endpoint returns correct counts when test data has mixed severities and statuses
- [ ] Integration test: by-product endpoint returns correct per-product counts
- [ ] Integration test: both endpoints handle empty dataset gracefully (return zero counts, not errors)

## Verification Commands
- `cargo test --test api remediation` — Run remediation integration tests, expect all tests to pass
- `curl http://localhost:8080/api/v2/remediation/summary` — Verify summary endpoint returns valid JSON response

## Dependencies
- Depends on: Task 1 — Add remediation model and service layer
