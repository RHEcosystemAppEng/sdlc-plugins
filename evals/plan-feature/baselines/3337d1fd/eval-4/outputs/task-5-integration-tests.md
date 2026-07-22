## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the license compliance report endpoint. Tests cover the full request-response cycle against a real test database, verifying correct license grouping, policy compliance flagging, transitive dependency inclusion, and error handling.

## Files to Modify
- `tests/Cargo.toml` — Add dependency on the license report module if needed for test fixtures

## Files to Create
- `tests/api/license_report.rs` — Integration tests for `GET /api/v2/sbom/{id}/license-report`. Tests include: (1) happy path with mixed license types returning correct groups and compliance flags, (2) SBOM with all compliant licenses, (3) SBOM with denied licenses flagged as non-compliant, (4) transitive dependencies included with `is_transitive: true`, (5) non-existent SBOM returns 404, (6) summary statistics are accurate, (7) packages with no license data grouped under "Unknown".
- `tests/fixtures/license-policy-test.json` — Test license policy configuration used by integration tests

## Implementation Notes
- Follow the existing integration test pattern in `tests/api/sbom.rs` — use the same test database setup and teardown approach.
- Use the `assert_eq!(resp.status(), StatusCode::OK)` pattern consistent with existing tests.
- Test fixtures should set up SBOM records with known packages and licenses to produce deterministic results.
- The test license policy should classify MIT and Apache-2.0 as approved, GPL-3.0 as denied, and LGPL-2.1 as restricted for clear test assertions.
- Verify the JSON response body structure matches `LicenseReportResponse` schema.

## Acceptance Criteria
- [ ] All integration tests pass against the test database
- [ ] Happy path test verifies correct grouping and compliance flags
- [ ] Error case tests verify proper HTTP status codes
- [ ] Tests cover both direct and transitive dependency scenarios
- [ ] Test coverage includes edge cases: empty SBOM, packages with multiple licenses

## Test Requirements
- [ ] Integration test: happy path with multiple license types
- [ ] Integration test: all-compliant SBOM
- [ ] Integration test: SBOM with denied licenses
- [ ] Integration test: transitive dependency inclusion
- [ ] Integration test: non-existent SBOM returns 404
- [ ] Integration test: summary statistics correctness
- [ ] Integration test: packages with unknown/missing licenses

## Dependencies
- Depends on: Task 4 — License report endpoint (endpoint must be implemented and registered)
