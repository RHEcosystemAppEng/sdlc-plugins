## Repository
trustify-backend

## Target Branch
main

## Description
Add integration tests for the license report endpoint that validate the full request-response cycle against a real PostgreSQL test database. Tests cover successful report generation, compliance flagging, handling of SBOMs with no packages, and error cases for invalid SBOM IDs.

## Files to Create
- `tests/api/license_report.rs` — Integration tests for `GET /api/v2/sbom/{id}/license-report`, following the test patterns established in `tests/api/sbom.rs` and `tests/api/advisory.rs`

## Files to Modify
- `tests/Cargo.toml` — Add the new test file to the test configuration if required by the project's test organization

## Implementation Notes
- Follow the integration test pattern from `tests/api/sbom.rs` for test setup, database seeding, and HTTP client configuration
- Use `assert_eq!(resp.status(), StatusCode::OK)` pattern as specified in the repository conventions
- Seed test data: create an SBOM with packages that have various licenses (MIT, Apache-2.0, GPL-3.0) to test both compliant and non-compliant grouping
- Test cases to implement:
  1. **Happy path**: SBOM with mixed licenses returns correctly grouped report with proper compliance flags
  2. **All compliant**: SBOM where all packages have allowed licenses; `non_compliant_count` should be 0
  3. **Non-compliant detected**: SBOM with denied licenses; verify groups are flagged `compliant: false`
  4. **Empty SBOM**: SBOM with no packages returns an empty groups array
  5. **Invalid SBOM ID**: Non-existent ID returns 404
  6. **Transitive dependencies**: Verify that transitively-included packages appear in the report
- Use the existing test database infrastructure; do not create separate database setup

## Acceptance Criteria
- [ ] All six test cases pass against the test database
- [ ] Tests verify JSON response structure matches the `LicenseReport` schema
- [ ] Tests verify compliance flags are correctly computed based on the license policy
- [ ] Tests clean up seed data after execution

## Test Requirements
- [ ] Happy path test with mixed compliant/non-compliant licenses
- [ ] Edge case test for SBOM with zero packages
- [ ] Error case test for non-existent SBOM ID returning 404
- [ ] Test verifying transitive dependency inclusion
- [ ] Test verifying response JSON shape matches expected schema

## Dependencies
- Depends on: Task 4 — Add license report endpoint and route registration

## Digest
[sdlc-workflow] Description digest: sha256-md:dbc9711329ad47651ecefe10b40a51a36dcd2f4bcd54f6f823fd5c543059d253
