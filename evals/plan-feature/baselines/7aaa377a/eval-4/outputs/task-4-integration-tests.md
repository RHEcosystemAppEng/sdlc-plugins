# Task 4 — Add integration tests for license report endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Add integration tests for the `GET /api/v2/sbom/{id}/license-report` endpoint. The tests verify the full request-response cycle against a real PostgreSQL test database, covering successful report generation, non-compliant license flagging, transitive dependency inclusion, edge cases, and the p95 < 500ms performance requirement for SBOMs with up to 1000 packages.

## Files to Create
- `tests/api/license_report.rs` -- Integration tests for the license report endpoint

## Files to Modify
- `tests/Cargo.toml` -- Add the test file to the test suite if required by the test harness configuration

## Implementation Notes
- Follow the test patterns established in `tests/api/sbom.rs` (SBOM endpoint integration tests). Use the same test database setup, HTTP client configuration, and assertion patterns.
- **Test database**: integration tests hit a real PostgreSQL test database per the repository convention. Set up test data by ingesting a test SBOM with known packages and licenses before each test.
- **Assertion pattern**: use `assert_eq!(resp.status(), StatusCode::OK)` as established in existing tests.
  Applies: task creates `tests/api/license_report.rs` matching the convention's test file scope.
- **Performance test**: for the p95 < 500ms NFR, create a test that generates a large SBOM (1000 packages) and asserts the response time is under the threshold. Use `std::time::Instant` to measure elapsed time.
- Set up test SBOMs with a mix of compliant and non-compliant licenses so the report can be verified for correct grouping and compliance flagging.

## Reuse Candidates
- `tests/api/sbom.rs` -- Existing SBOM endpoint integration tests; follow the same test setup, fixtures, and assertion patterns
- `tests/api/advisory.rs` -- Additional reference for integration test patterns in this repository

## Acceptance Criteria
- [ ] Test: successful report generation returns 200 with correctly grouped license data
- [ ] Test: non-compliant licenses are flagged with `compliant: false` in their group
- [ ] Test: transitive dependencies appear in the report
- [ ] Test: non-existent SBOM ID returns 404
- [ ] Test: SBOM with no packages returns an empty report
- [ ] Test: report generation completes within 500ms for an SBOM with 1000 packages
- [ ] All tests pass against the PostgreSQL test database

## Test Requirements
- [ ] Integration test: GET /api/v2/sbom/{id}/license-report returns 200 for a valid SBOM
- [ ] Integration test: response body contains packages grouped by license type
- [ ] Integration test: groups with denied licenses have `compliant: false`
- [ ] Integration test: groups with allowed licenses have `compliant: true`
- [ ] Integration test: overall `compliant` field reflects all-groups compliance
- [ ] Integration test: transitive dependencies are present in the response
- [ ] Integration test: 404 response for invalid SBOM ID
- [ ] Performance test: response time under 500ms for 1000-package SBOM

## Verification Commands
- `cargo test --test api -- license_report` -- Run the license report integration tests

## Dependencies
- Depends on: Task 1 -- Add license report model types and policy configuration
- Depends on: Task 2 -- Add license report service with dependency tree traversal
- Depends on: Task 3 -- Add GET /api/v2/sbom/{id}/license-report endpoint
