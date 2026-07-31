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
Add integration tests for the remediation REST API endpoints. Tests exercise `GET /api/v2/remediation/summary` and `GET /api/v2/remediation/by-product` against a real PostgreSQL test database with seeded vulnerability and SBOM data, verifying correct aggregation results, pagination behavior, and error handling.

## Files to Create
- `tests/api/remediation.rs` — Integration tests for remediation summary and by-product endpoints

## Files to Modify
- `tests/Cargo.toml` — Add any test-specific dependencies if needed for remediation test fixtures

## Implementation Notes
Follow the integration test pattern in `tests/api/sbom.rs` and `tests/api/advisory.rs`. Tests connect to a real PostgreSQL test database, seed test data through the ingestion pipeline, and make HTTP requests to the remediation endpoints.

Use the `assert_eq!(resp.status(), StatusCode::OK)` pattern established in existing tests. Seed test data covering multiple severities (Critical, High, Medium, Low) and multiple products to validate both aggregation endpoints.

Test the by-product endpoint pagination using the same query parameter patterns tested in `tests/api/sbom.rs`.

Per CONVENTIONS.md §Testing: integration tests in tests/api/ hit a real PostgreSQL test database. Applies: task creates `tests/api/remediation.rs` matching the convention's `.rs` test scope.

## Acceptance Criteria
- [ ] Summary endpoint integration test verifies correct severity-by-status counts
- [ ] By-product endpoint integration test verifies correct per-product breakdown
- [ ] Pagination test verifies correct page size and total count
- [ ] Tests verify empty result handling when no vulnerability data exists
- [ ] Tests use real PostgreSQL test database following existing test patterns

## Test Requirements
- [ ] Test summary endpoint with seeded data covering all four severity levels
- [ ] Test by-product endpoint with multiple products having different remediation statuses
- [ ] Test pagination with limit and offset parameters
- [ ] Test error responses for invalid parameters
- [ ] Verify p95 response time assertion for summary endpoint with >1000 seeded records

## Dependencies
- Depends on: Task 2 — remediation-endpoints (provides the endpoints to test)
