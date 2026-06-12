# Task 5 — Add integration tests for the license report endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the license compliance report endpoint. Tests should cover the full request-response cycle including various license compliance scenarios, transitive dependency inclusion, edge cases, and error handling. These tests hit a real PostgreSQL test database following the established testing pattern.

## Files to Create
- `tests/api/license_report.rs` — Integration tests for the license report endpoint

## Files to Modify
- `tests/Cargo.toml` — Add the new test module if test discovery requires explicit registration

## Implementation Notes
- Follow the existing integration test patterns in `tests/api/sbom.rs` and `tests/api/advisory.rs`:
  - Use the `assert_eq!(resp.status(), StatusCode::OK)` pattern for status code assertions
  - Tests hit a real PostgreSQL test database
  - Set up test data (SBOM with packages and license mappings) before making API calls
- Test scenarios should cover:
  - SBOM with a mix of compliant and non-compliant licenses
  - SBOM with only compliant licenses (all groups `compliant: true`)
  - SBOM with only non-compliant licenses (all groups `compliant: false`)
  - SBOM with transitive dependencies that introduce additional licenses
  - SBOM with no packages (empty groups)
  - Non-existent SBOM ID (404 response)
- Verify the response JSON structure matches the specification: `{ groups: [{ license, packages, compliant }] }`
- Use the default license policy configuration for test assertions, or create a test-specific policy

## Reuse Candidates
- `tests/api/sbom.rs` — Follow its test setup patterns (database seeding, HTTP client configuration, assertion patterns)
- `tests/api/advisory.rs` — Additional reference for integration test structure
- `tests/api/search.rs` — Reference for query parameter testing patterns if applicable

## Acceptance Criteria
- [ ] All integration tests pass against a PostgreSQL test database
- [ ] Tests cover both compliant and non-compliant license scenarios
- [ ] Tests verify the correct JSON response shape
- [ ] Tests verify transitive dependency inclusion
- [ ] Tests verify error handling for invalid SBOM IDs

## Test Requirements
- [ ] Integration test: SBOM with mixed compliance — verify groups contain correct `compliant` flags
- [ ] Integration test: SBOM with transitive deps — verify transitive package licenses appear in the report
- [ ] Integration test: empty SBOM — verify empty groups array is returned
- [ ] Integration test: non-existent SBOM — verify 404 response status
- [ ] Integration test: verify each LicenseGroup contains the correct list of packages for that license

## Verification Commands
- `cargo test --test api license_report` — Run only the license report integration tests
- `cargo test --test api` — Run all API integration tests to verify no regressions

## Dependencies
- Depends on: Task 4 — Add GET /api/v2/sbom/{id}/license-report endpoint
