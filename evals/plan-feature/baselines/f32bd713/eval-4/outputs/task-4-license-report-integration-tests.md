## Repository
trustify-backend

## Target Branch
main

## Description
Add integration tests for the GET /api/v2/sbom/{id}/license-report endpoint (TC-9004). Tests should cover successful report generation with compliant and non-compliant licenses, transitive dependency inclusion in reports, policy violation detection, error handling for missing SBOMs, and behavior with empty SBOMs. Follow the established integration test patterns in the tests/api/ directory.

## Files to Create
- `tests/api/license_report.rs` — integration tests for the license compliance report endpoint

## Files to Modify
- `tests/Cargo.toml` — add the license_report test module to the test harness if required by the project test setup

## Implementation Notes
Follow the existing integration test patterns established in `tests/api/sbom.rs`. Tests should:

1. Set up a test PostgreSQL database with known SBOM and package-license data
2. Configure a test license policy with specific allowed and denied licenses
3. Make HTTP requests to the license report endpoint
4. Assert on response status codes and response body structure

Per CONVENTIONS.md §Testing: use a real PostgreSQL test database for integration tests and follow the `assert_eq!(resp.status(), StatusCode::OK)` assertion pattern. See `tests/api/sbom.rs` for the established test setup and teardown patterns.
Applies: task creates `tests/api/license_report.rs` matching the convention's `.rs` integration test file scope.

Test data should include:
- An SBOM with packages that have MIT licenses (allowed) and GPL-3.0 licenses (depending on policy)
- Packages with transitive dependencies to verify dependency tree walking
- An SBOM with no packages (edge case)

## Reuse Candidates
- `tests/api/sbom.rs` — existing SBOM integration test patterns, test database setup, and HTTP request helpers

## Acceptance Criteria
- [ ] Integration test: GET /api/v2/sbom/{id}/license-report returns HTTP 200 with valid ComplianceReport JSON for an SBOM with known packages and licenses
- [ ] Integration test: report correctly groups packages by license type
- [ ] Integration test: compliant flag is true for allowed licenses and false for denied licenses per the configured policy
- [ ] Integration test: transitive dependencies appear in the correct license groups
- [ ] Integration test: returns HTTP 404 for a non-existent SBOM ID
- [ ] Integration test: returns empty groups array for an SBOM with no associated packages

## Test Requirements
- [ ] Integration test: successful report generation with multiple license groups, verifying response structure and content
- [ ] Integration test: policy violation detection — a known denied license results in `compliant: false` for its group
- [ ] Integration test: transitive dependency inclusion — packages reached through dependency tree walking appear in groups
- [ ] Integration test: HTTP 404 response for non-existent SBOM ID with appropriate error body
- [ ] Integration test: empty SBOM handling — an SBOM with no packages returns an empty groups array

## Verification Commands
- `cargo test --test license_report` — all license report integration tests pass

## Dependencies
- Depends on: Task 3 — Add GET /api/v2/sbom/{id}/license-report endpoint
