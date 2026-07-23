# Task 5 — Add integration tests for license report endpoint

**Summary:** Add integration tests for the license report endpoint

**Epic:** TC-9004: License report service and API

## Repository
trustify-backend

## Target Branch
main

## Description
Add integration tests for the `GET /api/v2/sbom/{id}/license-report` endpoint. Tests should cover the full request-response cycle against a real PostgreSQL test database, following the established integration test patterns in `tests/api/`.

## Files to Create
- `tests/api/license_report.rs` — integration tests for the license report endpoint

## Files to Modify
- `tests/Cargo.toml` — add the new test file to the test suite if needed (depends on test runner configuration)

## Implementation Notes
- Follow the existing integration test pattern in `tests/api/sbom.rs`. Tests should:
  1. Set up test data: create an SBOM with packages that have various licenses (some compliant, some non-compliant) via the ingestion pipeline or direct database seeding
  2. Include transitive dependencies in the test data to verify dependency tree walking
  3. Send HTTP requests to the endpoint using the test client
  4. Assert response status codes and JSON body shapes using `assert_eq!(resp.status(), StatusCode::OK)` pattern
- Create test scenarios covering:
  - **Happy path**: SBOM with mixed licenses, verifying correct grouping and compliance flags
  - **All compliant**: SBOM where all packages use allowed licenses, verifying all groups have `compliant: true`
  - **Non-compliant detection**: SBOM with packages using denied licenses, verifying `compliant: false` flags
  - **Transitive dependencies**: SBOM with a dependency chain, verifying transitive packages appear with `transitive: true`
  - **Empty SBOM**: SBOM with no packages, verifying empty `groups` array
  - **Not found**: Request for non-existent SBOM ID returns 404
- Use the same test database setup and teardown approach as other integration tests in `tests/api/`

## Reuse Candidates
- `tests/api/sbom.rs` — existing SBOM endpoint integration tests; follow the same test structure, setup, and assertion patterns
- `tests/api/advisory.rs` — additional reference for integration test patterns, particularly for error case testing

## Acceptance Criteria
- [ ] Integration tests pass against a PostgreSQL test database
- [ ] Tests cover happy path, compliance detection, transitive dependencies, empty SBOM, and 404 cases
- [ ] Tests verify the JSON response shape matches the API specification
- [ ] Tests follow the established patterns in `tests/api/`

## Test Requirements
- [ ] Test that a compliant SBOM returns all groups with `compliant: true`
- [ ] Test that an SBOM with denied licenses returns groups with `compliant: false`
- [ ] Test that transitive dependencies appear in the report with `transitive: true`
- [ ] Test that an SBOM with no packages returns an empty `groups` array
- [ ] Test that requesting a non-existent SBOM returns 404
- [ ] Test that the response Content-Type is application/json

## Dependencies
- Depends on: Task 4 — Add GET /api/v2/sbom/{id}/license-report endpoint
