## Repository
trustify-backend

## Target Branch
main

## Description
Add integration tests for the license compliance report endpoint. Tests hit a real PostgreSQL test database following the existing test patterns in `tests/api/`. Cover the happy path (valid SBOM with multiple licenses), compliance flagging (mix of compliant and non-compliant licenses), edge cases (SBOM with no packages, non-existent SBOM), and transitive dependency inclusion.

## Files to Create
- `tests/api/license_report.rs` — Integration tests for `GET /api/v2/sbom/{id}/license-report`

## Files to Modify
- `tests/Cargo.toml` — Add the new test file to the test suite if required by the project's test configuration

## Implementation Notes
Follow the integration test pattern established in `tests/api/sbom.rs` and `tests/api/advisory.rs`:
- Set up test data in the PostgreSQL test database (ingest an SBOM with packages that have known licenses)
- Call the endpoint via HTTP
- Assert on response status and body structure using `assert_eq!(resp.status(), StatusCode::OK)` pattern

Test scenarios:
1. **Happy path**: Ingest an SBOM with packages having MIT and Apache-2.0 licenses. Call the endpoint. Assert groups are returned with correct license identifiers and compliant flags.
2. **Non-compliant flagging**: Configure policy to deny a specific license. Ingest SBOM with a package using that license. Assert the group is flagged as non-compliant.
3. **Empty SBOM**: Call endpoint for an SBOM with no packages. Assert empty groups list.
4. **Non-existent SBOM**: Call endpoint with an invalid SBOM ID. Assert error response.
5. **Transitive dependencies**: Ingest SBOM with transitive dependency chain. Assert all levels are included in the report.

Per CONVENTIONS.md §Testing: integration tests in `tests/api/` hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern. Applies: task creates `tests/api/license_report.rs` matching the convention's `tests/api/` directory scope.

## Reuse Candidates
- `tests/api/sbom.rs` — Existing SBOM integration tests; follow the same setup, request, and assertion patterns
- `tests/api/advisory.rs` — Additional reference for integration test structure and database setup

## Acceptance Criteria
- [ ] All five test scenarios are implemented and pass
- [ ] Tests use the existing PostgreSQL test database infrastructure
- [ ] Tests follow the assertion pattern established in sibling test files
- [ ] Tests are included in the test suite and run with `cargo test`

## Test Requirements
- [ ] Integration test: valid SBOM returns 200 with correctly grouped license data
- [ ] Integration test: non-compliant license is flagged with `compliant: false`
- [ ] Integration test: SBOM with no packages returns empty groups
- [ ] Integration test: non-existent SBOM ID returns error status
- [ ] Integration test: transitive dependencies are included in the report

## Dependencies
- Depends on: Task 3 — License report endpoint
