# Task 4 — Add integration tests for license compliance report endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the license compliance report feature, covering the full request-response lifecycle against a real PostgreSQL test database. The tests validate correct license grouping, compliance flagging against different policy configurations, transitive dependency inclusion, error handling, and performance characteristics.

## Files to Modify
- `tests/Cargo.toml` — add any test-specific dependencies if needed (e.g., test fixture helpers)

## Files to Create
- `tests/api/license_report.rs` — integration tests for the license report endpoint

## Implementation Notes
- Follow the existing integration test pattern in `tests/api/sbom.rs` and `tests/api/advisory.rs`:
  - Tests hit a real PostgreSQL test database
  - Use `assert_eq!(resp.status(), StatusCode::OK)` pattern for status assertions
  - Set up test data by ingesting an SBOM with known packages and licenses before calling the report endpoint
- Test scenarios should cover:
  - **Happy path:** SBOM with multiple packages under MIT, Apache-2.0, and GPL-3.0 licenses; policy denies GPL-3.0. Verify grouping and that GPL-3.0 group has `compliant: false`.
  - **All compliant:** SBOM with only allowed licenses. Verify all groups have `compliant: true`.
  - **Empty SBOM:** SBOM with no packages. Verify the report returns an empty groups array.
  - **Transitive dependencies:** SBOM with a dependency tree; verify that transitive dependency licenses appear in the report.
  - **Missing SBOM:** Request with a non-existent SBOM ID returns 404.
- Create a test license policy JSON fixture for use across tests.
- Per docs/constraints.md: keep changes scoped to the files listed (constraint 5.1), follow patterns referenced in implementation notes (constraint 5.3).

## Reuse Candidates
- `tests/api/sbom.rs` — demonstrates SBOM endpoint integration test patterns (setup, request, assertion)
- `tests/api/advisory.rs` — demonstrates advisory endpoint integration test patterns
- `tests/api/search.rs` — demonstrates search endpoint integration test patterns

## Acceptance Criteria
- [ ] Integration tests cover the happy path with mixed compliant and non-compliant licenses
- [ ] Integration tests verify correct grouping by license type
- [ ] Integration tests verify transitive dependency inclusion
- [ ] Integration tests verify 404 response for non-existent SBOM
- [ ] Integration tests verify the response JSON structure matches the API contract
- [ ] All tests pass in CI against a PostgreSQL test database

## Test Requirements
- [ ] At least 5 integration test cases covering: happy path, all-compliant, empty SBOM, transitive dependencies, and missing SBOM
- [ ] Each test function has a doc comment explaining the scenario
- [ ] Non-trivial tests include given-when-then inline comments

## Verification Commands
- `cargo test -p trustify-tests -- license_report` — run all license report integration tests

## Dependencies
- Depends on: Task 3 — Add GET /api/v2/sbom/{id}/license-report endpoint
