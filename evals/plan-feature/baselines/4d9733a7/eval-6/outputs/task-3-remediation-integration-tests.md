## Repository
trustify-backend

## Target Branch
main

## Description
Add integration tests for the remediation summary and by-product endpoints. Tests verify correct aggregation logic, response shapes, filtering, pagination, and error handling. The tests follow the established integration test pattern in `tests/api/` using a real PostgreSQL test database.

## Files to Create
- `tests/api/remediation.rs` — integration tests for `GET /api/v2/remediation/summary` and `GET /api/v2/remediation/by-product`

## Files to Modify
- `tests/Cargo.toml` — add remediation test module if test registration is needed

## Implementation Notes
- Per repo conventions (Testing): integration tests in `tests/api/` hit a real PostgreSQL test database. Use the `assert_eq!(resp.status(), StatusCode::OK)` pattern established in existing tests.
  Applies: task creates `tests/api/remediation.rs` matching the convention's Rust test file scope.
- Follow the test structure in `tests/api/sbom.rs` and `tests/api/advisory.rs` for setting up test data, making HTTP requests, and asserting response shapes.
- Test scenarios should cover: empty database (no vulnerabilities), single SBOM with mixed severity vulnerabilities, multiple products with different remediation states, and pagination boundaries for the by-product endpoint.
- Per repo conventions (Error handling): verify that error responses return the correct `AppError`-based error format.
  Applies: task creates `tests/api/remediation.rs` matching the convention's Rust test file scope.

## Reuse Candidates
- `tests/api/sbom.rs` — reference for integration test structure, test database setup, and HTTP assertion patterns
- `tests/api/advisory.rs` — reference for testing advisory-related data which overlaps with remediation aggregation
- `tests/api/search.rs` — reference for testing query parameter handling (filtering, pagination)

## Acceptance Criteria
- [ ] Integration tests exist for both `GET /api/v2/remediation/summary` and `GET /api/v2/remediation/by-product`
- [ ] Tests verify correct response shapes and status codes
- [ ] Tests cover edge cases: empty data, single product, multiple products, pagination
- [ ] All tests pass against a PostgreSQL test database

## Test Requirements
- [ ] Test `GET /api/v2/remediation/summary` returns correct aggregated counts by severity and status
- [ ] Test `GET /api/v2/remediation/summary` returns empty counts when no vulnerabilities exist
- [ ] Test `GET /api/v2/remediation/by-product` returns correct per-product breakdown
- [ ] Test `GET /api/v2/remediation/by-product` pagination with offset and limit parameters
- [ ] Test error responses for invalid query parameters

## Verification Commands
- `cargo test --test remediation` — run remediation integration tests
- `cargo test` — confirm all tests pass including new remediation tests

## Dependencies
- Depends on: Task 1 — Create remediation module with summary endpoint
- Depends on: Task 2 — Add remediation by-product endpoint
