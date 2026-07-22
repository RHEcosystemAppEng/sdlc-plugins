## Repository
trustify-backend

## Target Branch
main

## Description
Add integration tests for the remediation API endpoints. Tests verify the full request-response cycle against a real PostgreSQL test database, covering both the summary and by-product endpoints with various data scenarios.

## Files to Create
- `tests/api/remediation.rs` — integration tests for GET /api/v2/remediation/summary and GET /api/v2/remediation/by-product

## Files to Modify
- `tests/Cargo.toml` — add remediation test module if test modules are registered there

## Implementation Notes
Follow the integration test pattern in `tests/api/sbom.rs` and `tests/api/advisory.rs`. Tests should hit a real PostgreSQL test database and use the `assert_eq!(resp.status(), StatusCode::OK)` pattern. Seed test data by creating advisory and SBOM entities with known severity and status values, then verify the aggregation endpoints return correct counts.

Per CONVENTIONS.md §Testing: integration tests hit real PostgreSQL, use assert_eq!(resp.status(), StatusCode::OK) pattern.
Applies: task creates `tests/api/remediation.rs` matching the convention's `.rs` file scope.

## Reuse Candidates
- `tests/api/sbom.rs` — integration test setup and assertion patterns
- `tests/api/advisory.rs` — advisory-specific test data seeding

## Acceptance Criteria
- [ ] Integration tests pass against PostgreSQL test database
- [ ] Summary endpoint returns correct aggregated counts for seeded test data
- [ ] By-product endpoint returns correct per-product breakdown
- [ ] Edge case: empty database returns zero counts, not an error
- [ ] Pagination parameters work correctly on by-product endpoint

## Test Requirements
- [ ] Test summary endpoint with multiple severities and statuses
- [ ] Test by-product endpoint with multiple products
- [ ] Test empty state returns valid empty response
- [ ] Test pagination on by-product endpoint

## Dependencies
- Depends on: Task 3 — Create remediation API endpoints
