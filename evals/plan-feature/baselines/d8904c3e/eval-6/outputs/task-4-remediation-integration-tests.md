## Repository
trustify-backend

## Target Branch
TC-9006

## Description
Add comprehensive integration tests for the remediation API endpoints created in Task 3. Tests hit a real PostgreSQL test database following the established testing pattern in tests/api/, verifying correct aggregation logic, response shapes, pagination, and error handling for both the summary and by-product endpoints.

## Files to Create
- `tests/api/remediation.rs` -- integration tests for GET /api/v2/remediation/summary and GET /api/v2/remediation/by-product

## Files to Modify
- `tests/Cargo.toml` -- add remediation test module if test modules are registered explicitly

## Implementation Notes
- Follow the integration test pattern established in `tests/api/sbom.rs` and `tests/api/advisory.rs`: tests hit a real PostgreSQL test database with `assert_eq!(resp.status(), StatusCode::OK)` pattern.
  Per CONVENTIONS.md: integration tests in tests/api/ hit a real PostgreSQL test database; use assert_eq!(resp.status(), StatusCode::OK) pattern.
  Applies: task creates `tests/api/remediation.rs` matching the convention's Rust test file scope.
- Set up test data by ingesting sample SBOMs and advisories with known vulnerability counts, then verify the aggregation endpoints return correct totals.
- Test the by-product endpoint with pagination parameters (offset=0, limit=10) to verify PaginatedResults behavior.
- Non-functional validation: add a test with a larger dataset (hundreds of vulnerabilities) to verify response time stays reasonable, though strict p95 benchmarking belongs in dedicated performance tests.

## Reuse Candidates
- `tests/api/sbom.rs` -- SBOM endpoint integration test patterns; follow for test setup and assertion style
- `tests/api/advisory.rs` -- advisory endpoint integration test patterns; reference for advisory/vulnerability test data setup
- `tests/api/search.rs` -- search endpoint integration tests; reference for additional test patterns

## Acceptance Criteria
- [ ] Integration test verifies GET /api/v2/remediation/summary returns correct aggregated counts for known test data
- [ ] Integration test verifies GET /api/v2/remediation/by-product returns correct per-product breakdown for known test data
- [ ] Integration test verifies pagination on by-product endpoint
- [ ] Integration test verifies empty database returns valid empty response
- [ ] All tests pass against PostgreSQL test database

## Test Requirements
- [ ] Test summary endpoint with multiple severities and statuses, verifying all severity x status combinations are represented
- [ ] Test by-product endpoint with multiple products, verifying per-product totals match expected values
- [ ] Test by-product pagination with offset and limit parameters
- [ ] Test both endpoints with no vulnerability data to verify graceful empty response
- [ ] Test error scenarios (malformed query parameters)

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9006 from main
- Depends on: Task 3 -- Add remediation API endpoints and register routes
