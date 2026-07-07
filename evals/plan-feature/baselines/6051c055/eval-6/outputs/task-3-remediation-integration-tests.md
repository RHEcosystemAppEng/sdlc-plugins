## Repository
trustify-backend

## Target Branch
main

## Description
Add integration tests for the remediation aggregation endpoints (TC-9006). The tests verify both `GET /api/v2/remediation/summary` and `GET /api/v2/remediation/by-product` endpoints against a real PostgreSQL test database, following the established integration test patterns in `tests/api/`.

## Files to Create
- `tests/api/remediation.rs` — integration tests for both remediation endpoints

## Files to Modify
- `tests/Cargo.toml` — register the new test module if needed

## Implementation Notes
- Follow the existing integration test pattern from `tests/api/sbom.rs` and `tests/api/advisory.rs`: tests hit a real PostgreSQL test database and use `assert_eq!(resp.status(), StatusCode::OK)` assertions.
- Set up test data by inserting advisory and SBOM records with known severity and status values to verify aggregation correctness.
- Test both populated and empty database scenarios.
- For the by-product endpoint, verify pagination parameters work correctly.
- Verify the response JSON shape matches the model structs defined in Task 1.

Per CONVENTIONS.md Section "Testing": integration tests in `tests/api/` hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern.
Applies: task creates `tests/api/remediation.rs` matching the convention's `.rs` test file scope.

## Reuse Candidates
- `tests/api/sbom.rs` — reference for integration test setup, database seeding, and assertion patterns
- `tests/api/advisory.rs` — reference for advisory-related test data setup (severity values)

## Acceptance Criteria
- [ ] Integration tests for GET /api/v2/remediation/summary pass against PostgreSQL test database
- [ ] Integration tests for GET /api/v2/remediation/by-product pass against PostgreSQL test database
- [ ] Tests verify correct aggregation counts for known test data
- [ ] Tests verify empty-state behavior (zero counts when no data exists)
- [ ] Tests verify response status codes and JSON shape

## Test Requirements
- [ ] Test summary endpoint returns correct severity x status counts with seeded data
- [ ] Test summary endpoint returns all-zero counts with empty database
- [ ] Test by-product endpoint returns correct per-product breakdown
- [ ] Test by-product endpoint pagination works correctly
- [ ] Test both endpoints return 200 OK status code

## Verification Commands
- `cargo test -p trustify-tests -- api::remediation` — all remediation integration tests pass

## Dependencies
- Depends on: Task 1 — Create remediation domain models and aggregation service
- Depends on: Task 2 — Add remediation REST endpoints with route registration
