# Task 5 -- Add integration tests for license report endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the `GET /api/v2/sbom/{id}/license-report` endpoint. Tests should cover the core use cases from the feature description: generating compliance reports with grouped license data, flagging non-compliant licenses, handling transitive dependencies, and the automated compliance gate scenario (CI/CD pipeline checking for `compliant: false`).

## Files to Create
- `tests/api/license_report.rs` -- Integration tests for the license report endpoint

## Files to Modify
- `tests/Cargo.toml` -- Add the new test file to the test crate if needed (depends on test discovery configuration)

## Implementation Notes
- Follow the existing integration test pattern in `tests/api/` -- see `sbom.rs` for the established test pattern: test functions using `assert_eq!(resp.status(), StatusCode::OK)`, setup with test database, and structured arrange/act/assert flow.
- Test setup should:
  1. Ingest a test SBOM with known packages and licenses
  2. Configure a test license policy with specific allowed/denied licenses
  3. Call the endpoint and verify the response
- Include the following test scenarios:
  - **Compliant SBOM**: all packages have allowed licenses -> all groups have `compliant: true`
  - **Non-compliant SBOM**: some packages have denied licenses -> those groups have `compliant: false`
  - **Mixed compliance**: SBOM with both compliant and non-compliant licenses -> correct flags per group
  - **Transitive dependencies**: verify packages from the transitive dependency tree appear in the report
  - **Empty SBOM**: SBOM with no packages -> returns empty groups list
  - **Non-existent SBOM**: invalid SBOM ID -> returns 404
  - **Compliance gate scenario** (UC-2): pipeline can check if any group has `compliant: false`
- Performance scenario: create a test SBOM with 1000 packages and verify report generation completes within the p95 < 500ms NFR.

## Reuse Candidates
- `tests/api/sbom.rs` -- SBOM endpoint integration tests; follow the same test structure, database setup, and assertion patterns
- `tests/api/advisory.rs` -- Advisory endpoint integration tests; demonstrates the test organization pattern for a different domain module

## Acceptance Criteria
- [ ] All integration tests pass against a test PostgreSQL database
- [ ] Tests cover compliant, non-compliant, mixed compliance, and transitive dependency scenarios
- [ ] Tests verify correct HTTP status codes (200 for success, 404 for missing SBOM)
- [ ] Tests verify response JSON shape matches the API contract
- [ ] Performance test verifies sub-500ms response time for 1000-package SBOMs

## Test Requirements
- [ ] Integration test: compliant SBOM returns all groups with `compliant: true`
- [ ] Integration test: non-compliant SBOM returns flagged groups with `compliant: false`
- [ ] Integration test: mixed SBOM returns correct compliance flags per license group
- [ ] Integration test: transitive dependencies are included in the report
- [ ] Integration test: empty SBOM returns empty groups list with 200 status
- [ ] Integration test: non-existent SBOM ID returns 404
- [ ] Performance test: 1000-package SBOM report generation under 500ms

## Verification Commands
- `cargo test --test license_report` -- all license report integration tests pass
- `cargo test` -- full test suite passes with no regressions

## Dependencies
- Depends on: Task 1 -- Add license policy configuration model and loader
- Depends on: Task 2 -- Add license compliance report model
- Depends on: Task 3 -- Add license report service
- Depends on: Task 4 -- Add license report endpoint
