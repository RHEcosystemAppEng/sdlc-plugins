## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the license compliance report endpoint (`GET /api/v2/sbom/{id}/license-report`). Tests cover the full request-response cycle against a real PostgreSQL test database, verifying correct license grouping, compliance flagging, transitive dependency inclusion, and error handling for edge cases.

## Files to Modify
- `tests/Cargo.toml` -- add test dependencies if needed for license report test fixtures

## Files to Create
- `tests/api/license_report.rs` -- integration tests for the license report endpoint covering: compliant SBOM, non-compliant SBOM with denied licenses, SBOM with transitive dependencies, SBOM with no packages, non-existent SBOM ID, SBOM with packages missing license data

## Implementation Notes
- Per Key Conventions "Testing": integration tests go in `tests/api/` and hit a real PostgreSQL test database. Use the `assert_eq!(resp.status(), StatusCode::OK)` assertion pattern.
  Applies: task creates `tests/api/license_report.rs` matching the convention's test file scope.
- Follow the test setup patterns from existing tests in `tests/api/sbom.rs` for creating test SBOMs and packages with known license data.
- Each test should set up its own test data (SBOM with specific packages and licenses) to ensure test isolation.
- Test the performance requirement by verifying that report generation for a 1000-package SBOM completes within a reasonable time bound.

## Reuse Candidates
- `tests/api/sbom.rs` -- existing SBOM endpoint integration tests; follow the same test setup, HTTP client configuration, and assertion patterns
- `tests/api/advisory.rs` -- existing advisory endpoint integration tests; reference for additional test patterns and database setup utilities

## Acceptance Criteria
- [ ] All integration tests pass against a PostgreSQL test database
- [ ] Tests verify the response JSON structure matches the LicenseReport schema
- [ ] Tests verify compliant/non-compliant license flagging based on the policy
- [ ] Tests verify transitive dependencies are included in the report
- [ ] Tests verify 404 response for non-existent SBOM IDs
- [ ] Tests verify handling of packages with no license data

## Test Requirements
- [ ] Integration test: SBOM with all MIT-licensed packages returns all groups with `compliant: true`
- [ ] Integration test: SBOM with a GPL-3.0-licensed package returns that group with `compliant: false`
- [ ] Integration test: SBOM with transitive dependencies includes all transitive packages in the report
- [ ] Integration test: SBOM with no packages returns an empty groups array
- [ ] Integration test: non-existent SBOM ID returns 404 status
- [ ] Integration test: SBOM with packages missing license data groups them appropriately (e.g., "Unknown" license group)
- [ ] Performance test: report generation for SBOM with 1000 packages completes within 500ms

## Verification Commands
- `cargo test --test api license_report` -- runs all license report integration tests; expect all tests to pass
- `cargo test --test api license_report -- --nocapture` -- runs tests with stdout output for debugging

## Dependencies
- Depends on: Task 1 -- Add license policy configuration and compliance report model
- Depends on: Task 2 -- Add license report service with transitive dependency traversal
- Depends on: Task 3 -- Add license compliance report REST endpoint
