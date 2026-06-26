## Repository
trustify-backend

## Target Branch
main

## Description
Add integration tests for the license compliance report endpoint. Tests should cover the full request-response cycle against a real PostgreSQL test database, verifying correct license grouping, compliance flagging, transitive dependency inclusion, and error cases. This follows the existing integration test patterns in `tests/api/`.

## Files to Create
- `tests/api/license_report.rs` — Integration tests for `GET /api/v2/sbom/{id}/license-report`

## Files to Modify
- `tests/Cargo.toml` — Add any needed test dependencies (if not already present)

## Implementation Notes
Follow the existing integration test patterns in `tests/api/sbom.rs` and `tests/api/advisory.rs`. These tests demonstrate the convention for setting up test fixtures, making HTTP requests to the test server, and asserting response status codes and body content using `assert_eq!(resp.status(), StatusCode::OK)`.

The test file should include these test cases:

1. **Happy path — multiple licenses**: Ingest an SBOM with packages under MIT, Apache-2.0, and GPL-3.0 licenses. Call the endpoint and verify the response contains three groups with correct package assignments and compliance flags matching the default policy.

2. **Transitive dependencies included**: Ingest an SBOM with a dependency tree (A depends on B, B depends on C). Verify that C's license appears in the report even though it is a transitive dependency.

3. **Non-compliant license flagged**: Configure the policy to deny a specific license. Ingest an SBOM containing a package with that license. Verify the group's `compliant` field is `false`.

4. **All compliant**: Ingest an SBOM where all packages use allowed licenses. Verify all groups have `compliant: true`.

5. **Non-existent SBOM**: Call the endpoint with a non-existent ID. Verify 404 response.

6. **Performance sanity check**: Ingest an SBOM with a substantial number of packages (if feasible in the test environment) and assert the response completes within a reasonable timeout.

Per CONVENTIONS.md §Testing: integration tests in `tests/api/` hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern.
Applies: task creates `tests/api/license_report.rs` matching the convention's test file scope.

## Reuse Candidates
- `tests/api/sbom.rs` — Existing SBOM integration tests; follow the same setup, request, and assertion patterns
- `tests/api/advisory.rs` — Additional reference for integration test patterns with different entity types

## Acceptance Criteria
- [ ] All integration tests pass against a PostgreSQL test database
- [ ] Happy path test verifies correct license grouping and package assignment
- [ ] Transitive dependency test verifies full dependency tree inclusion
- [ ] Non-compliant license test verifies `compliant: false` flag
- [ ] All-compliant test verifies `compliant: true` for all groups
- [ ] 404 test verifies error response for non-existent SBOM
- [ ] Tests follow existing patterns in `tests/api/`

## Test Requirements
- [ ] Integration test: GET returns grouped license data with correct compliance flags
- [ ] Integration test: transitive dependencies appear in the report
- [ ] Integration test: non-compliant licenses are flagged correctly
- [ ] Integration test: all-compliant SBOM returns all groups as compliant
- [ ] Integration test: non-existent SBOM ID returns 404

## Dependencies
- Depends on: Task 3 — Add license report endpoint and route registration

[sdlc-workflow] Description digest: sha256-md:59860afa58812a250503b42e003b5ff7238f7c7bb4ad8c6f3ec957950838721c
