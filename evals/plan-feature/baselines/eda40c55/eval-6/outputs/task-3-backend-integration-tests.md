## Repository
trustify-backend

## Target Branch
main

## Description
Add integration tests for both remediation endpoints (`GET /api/v2/remediation/summary` and `GET /api/v2/remediation/by-product`). Tests validate correct aggregation logic, response shapes, edge cases (empty data, single product, multiple severities), and performance characteristics against a real PostgreSQL test database.

## Files to Create
- `tests/api/remediation.rs` -- Integration tests for remediation summary and by-product endpoints

## Files to Modify
- `tests/Cargo.toml` -- Register the new remediation test module if required by the test harness configuration

## Implementation Notes
- Follow the existing integration test pattern in `tests/api/sbom.rs` and `tests/api/advisory.rs`: set up test data, call endpoints via HTTP client, assert on response status and body.
- Use `assert_eq!(resp.status(), StatusCode::OK)` pattern for status assertions as established in existing tests.
- Test data setup should insert advisory and SBOM entities with known severity and status values to verify aggregation correctness.
- Per CONVENTIONS.md §Testing: integration tests hit a real PostgreSQL test database. See `tests/api/sbom.rs` for the test database setup and teardown pattern.
  Applies: task creates `tests/api/remediation.rs` matching the convention's Rust test file scope.

## Reuse Candidates
- `tests/api/sbom.rs` -- SBOM endpoint integration tests; reuse the test setup pattern (database initialization, HTTP client configuration)
- `tests/api/advisory.rs` -- Advisory endpoint integration tests; reference for testing aggregation-style endpoints

## Acceptance Criteria
- [ ] Integration tests cover `GET /api/v2/remediation/summary` with known test data and verify aggregation counts
- [ ] Integration tests cover `GET /api/v2/remediation/by-product` with multiple products and verify per-product breakdowns
- [ ] Edge case tests: empty database returns empty results (not errors)
- [ ] Edge case tests: single product with vulnerabilities across all severity levels
- [ ] All tests pass against the PostgreSQL test database

## Test Requirements
- [ ] Test summary endpoint returns correct aggregation for mixed severity/status data
- [ ] Test by-product endpoint returns correct breakdown per product
- [ ] Test pagination on by-product endpoint with offset and limit
- [ ] Test empty state returns 200 with empty items array
- [ ] Test response shape matches defined struct types

## Verification Commands
- `cargo test --test api remediation` -- Expected: all remediation integration tests pass

## Dependencies
- Depends on: Task 1 -- Add remediation summary aggregation service and endpoint
- Depends on: Task 2 -- Add remediation by-product aggregation service and endpoint
