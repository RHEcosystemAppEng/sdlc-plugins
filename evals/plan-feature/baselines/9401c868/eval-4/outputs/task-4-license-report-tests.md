## Repository
trustify-backend

## Target Branch
main

## Description
Add integration tests for the `GET /api/v2/sbom/{id}/license-report` endpoint. The tests verify end-to-end behavior including: successful report generation with grouped license data, non-compliant license flagging, transitive dependency inclusion, error handling for missing SBOMs, and performance characteristics for large SBOMs.

These tests validate the complete license compliance report feature (TC-9004) through the HTTP API layer against a real PostgreSQL test database.

## Files to Create
- `tests/api/license_report.rs` -- Integration test module containing test functions for the license report endpoint, following the existing test patterns in `tests/api/sbom.rs`

## Files to Modify
- `tests/Cargo.toml` -- Add any new test dependencies if needed (likely none, as existing test infrastructure should suffice)

## Implementation Notes
- Follow the integration test pattern in `tests/api/sbom.rs`: tests hit a real PostgreSQL test database and use `assert_eq!(resp.status(), StatusCode::OK)` for status code assertions.
- Test setup should: (1) ingest a test SBOM with known packages and licenses, (2) create a license policy config file with known allowed/denied lists, (3) call the endpoint and verify the response.
- For the transitive dependency test, set up an SBOM with both direct and transitive package relationships to verify the full dependency tree is included in the report.
- For the performance test, consider using a test SBOM with a large number of packages (up to 1000) and asserting that the response time is under 500ms (p95 requirement from NFRs). This may be better suited as a benchmark test rather than a CI integration test.
- Per CONVENTIONS.md: integration tests in `tests/api/` hit a real PostgreSQL test database and use `assert_eq!(resp.status(), StatusCode::OK)` pattern.
  Applies: task creates `tests/api/license_report.rs` matching the convention's `.rs` test file scope.

## Reuse Candidates
- `tests/api/sbom.rs` -- Existing SBOM endpoint integration tests; demonstrates test setup, HTTP client configuration, request/response handling, and assertion patterns for the SBOM domain
- `tests/api/advisory.rs` -- Additional example of integration test patterns showing entity creation and endpoint verification

## Acceptance Criteria
- [ ] Test: GET license report for a valid SBOM returns 200 with grouped license data
- [ ] Test: response contains packages grouped by license type with correct `compliant` flags
- [ ] Test: non-compliant licenses (in the `denied` list) have `compliant: false`
- [ ] Test: compliant licenses (in the `allowed` list) have `compliant: true`
- [ ] Test: transitive dependency packages appear in the license groups
- [ ] Test: GET license report for a non-existent SBOM returns 404
- [ ] Test: all existing tests continue to pass (`cargo test`)

## Test Requirements
- [ ] Integration test: successful report generation with known license data returns correct groupings
- [ ] Integration test: SBOM with a mix of compliant and non-compliant packages returns correct flags per group
- [ ] Integration test: SBOM with transitive dependencies includes all packages in the report
- [ ] Integration test: non-existent SBOM ID returns 404 status
- [ ] Integration test: empty SBOM (no packages) returns 200 with an empty groups array

## Verification Commands
- `cargo test --test license_report` -- All license report integration tests pass
- `cargo test` -- All tests (including existing) pass without regressions

## Dependencies
- Depends on: Task 3 -- Add license report endpoint and route registration
