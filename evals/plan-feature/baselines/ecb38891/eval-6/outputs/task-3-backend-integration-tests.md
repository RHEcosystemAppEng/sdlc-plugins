# Task 3: Add integration tests for remediation endpoints

## Repository
trustify-backend

## Target Branch
TC-9006

## Description
Add comprehensive integration tests for the remediation aggregation endpoints created in Task 2. Tests verify correct aggregation logic, filtering, pagination, edge cases, and performance characteristics against a real PostgreSQL test database, following the existing test patterns in `tests/api/`.

## Files to Create
- `tests/api/remediation.rs` -- integration tests for both remediation endpoints

## Files to Modify
- `tests/Cargo.toml` -- add remediation test module if tests are organized as separate compilation units

## Implementation Notes
- Follow the integration test pattern in `tests/api/sbom.rs` and `tests/api/advisory.rs` -- these hit a real PostgreSQL test database and use `assert_eq!(resp.status(), StatusCode::OK)`.
- Seed test data by creating advisory and SBOM entities with known severity and status combinations to verify correct aggregation counts.
- Test the summary endpoint with multiple severity levels and statuses to verify the cross-product grouping is correct.
- Test the by-product endpoint with multiple products having different remediation profiles.
- Include edge cases: empty database, single vulnerability, large dataset simulation.
- Each test function should have a doc comment explaining the scenario being tested.

## Reuse Candidates
- `tests/api/sbom.rs` -- reference for integration test structure, database seeding, and assertion patterns
- `tests/api/advisory.rs` -- reference for advisory-related test data seeding

## Acceptance Criteria
- [ ] Integration tests exist for `GET /api/v2/remediation/summary` covering multiple severity/status combinations
- [ ] Integration tests exist for `GET /api/v2/remediation/by-product` covering multiple products
- [ ] Edge case test for empty database (no vulnerabilities) returns valid empty response
- [ ] Edge case test for single vulnerability returns correct single-entry aggregation
- [ ] Pagination tests verify `offset` and `limit` parameters work correctly on both endpoints
- [ ] All tests pass against the test PostgreSQL database

## Test Requirements
- [ ] Test `GET /api/v2/remediation/summary` with seeded data: 2 Critical/Open, 1 High/Resolved, 3 Medium/In Progress -- verify exact counts in response
- [ ] Test `GET /api/v2/remediation/by-product` with seeded data for 3 products with different remediation profiles -- verify per-product counts
- [ ] Test empty database scenario for both endpoints
- [ ] Test pagination with `limit=1` to verify partial result sets
- [ ] Test sorting parameters if supported

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9006 from main
- Depends on: Task 2 -- Add remediation aggregation service and API endpoints
