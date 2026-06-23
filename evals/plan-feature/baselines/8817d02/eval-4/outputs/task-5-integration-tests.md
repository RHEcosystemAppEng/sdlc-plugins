# Task 5 — Add license report integration tests

## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the license compliance report endpoint. Tests exercise the full stack — from HTTP request through service layer to database — using the project's existing integration test infrastructure with a real PostgreSQL test database. Tests cover the happy path, edge cases (empty SBOMs, unknown licenses, large SBOMs), and compliance policy enforcement.

## Files to Create
- `tests/api/license_report.rs` — integration tests for the license report endpoint

## Files to Modify
- `tests/Cargo.toml` — add the new test file to the test crate if needed (depending on test discovery configuration)

## Implementation Notes
- Follow the existing integration test patterns established in `tests/api/sbom.rs` and `tests/api/advisory.rs`:
  - Use the same test setup/teardown patterns (database initialization, test data seeding)
  - Use `assert_eq!(resp.status(), StatusCode::OK)` pattern for status code assertions
  - Make real HTTP requests to the test server
- Seed test data:
  - Create an SBOM with multiple packages having different licenses (MIT, Apache-2.0, GPL-3.0)
  - Include transitive dependency chains to verify deep license aggregation
  - Configure a license policy that allows MIT and Apache-2.0 but denies GPL-3.0
- Test cases:
  1. **Happy path**: SBOM with packages under multiple licenses; verify correct grouping and compliance flags
  2. **Transitive deps**: SBOM with a dependency chain A -> B -> C; verify C's license appears in the report
  3. **All compliant**: SBOM with only allowed licenses; verify all groups have `compliant: true`
  4. **Non-compliant licenses**: SBOM with denied licenses; verify those groups have `compliant: false`
  5. **Empty SBOM**: SBOM with no packages; verify empty `groups` array
  6. **Non-existent SBOM**: Request with invalid SBOM ID; verify 404 response
  7. **Performance**: SBOM with ~1000 packages; verify response time is within acceptable bounds (p95 < 500ms)
- Per docs/constraints.md section 5.11: add doc comments to every test function.
- Per docs/constraints.md section 5.12: add given-when-then inline comments to non-trivial test functions.
- Per docs/constraints.md section 5.9: consider parameterized tests for compliance flag scenarios (multiple licenses with known expected compliance status) using the Meszaros heuristic.

## Reuse Candidates
- `tests/api/sbom.rs` — follow the same test structure, setup, and assertion patterns for SBOM endpoint tests
- `tests/api/advisory.rs` — additional reference for integration test patterns in this project

## Acceptance Criteria
- [ ] All integration tests pass against the PostgreSQL test database
- [ ] Tests cover happy path, edge cases, and error cases as described
- [ ] Tests verify transitive dependency license aggregation
- [ ] Tests verify compliance flags match the configured license policy
- [ ] Performance test confirms p95 < 500ms for 1000-package SBOM

## Test Requirements
- [ ] Integration test: happy path with multiple license groups returns correct groupings and compliance flags
- [ ] Integration test: transitive dependencies are reflected in the license report
- [ ] Integration test: non-existent SBOM ID returns 404
- [ ] Integration test: empty SBOM returns empty groups array
- [ ] Integration test: performance assertion for large SBOMs (1000 packages)

## Verification Commands
- `cargo test --test api license_report` — run only the license report integration tests
- `cargo test --test api` — run all API integration tests to verify no regressions

## Dependencies
- Depends on: Task 4 — Add license report endpoint

sha256-md:4230f28eee91d4ac135ac18dbff0a2b5f83f320335c1cdf01a78cbcbfdf9b3e5
