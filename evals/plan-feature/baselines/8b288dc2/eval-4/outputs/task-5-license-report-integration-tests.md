## Repository
trustify-backend

## Target Branch
main

## Description
Add integration tests for the license compliance report endpoint. Tests should cover the full request-response cycle against a real PostgreSQL test database, verifying correct license grouping, compliance flagging, transitive dependency inclusion, and error handling.

## Files to Modify
- `tests/Cargo.toml` -- add any additional test dependencies if needed

## Files to Create
- `tests/api/license_report.rs` -- integration tests for `GET /api/v2/sbom/{id}/license-report`

## Implementation Notes
- Follow the existing integration test pattern in `tests/api/sbom.rs` -- tests hit a real PostgreSQL test database and use `assert_eq!(resp.status(), StatusCode::OK)` pattern.
- Test setup should ingest a test SBOM with known packages and licenses. Reuse any existing test fixture utilities from the `tests/` directory.
- Configure a test license policy (denylist mode with known non-compliant licenses) for tests that verify compliance flagging.
- Per CONVENTIONS.md (Key Conventions): integration tests in `tests/api/` hit a real PostgreSQL test database.
  Applies: task creates `tests/api/license_report.rs` matching the convention's `.rs` test file scope.

## Reuse Candidates
- `tests/api/sbom.rs` -- existing SBOM endpoint integration tests; follow the same test setup, fixture loading, and assertion patterns
- `tests/api/advisory.rs` -- additional integration test pattern reference

## Acceptance Criteria
- [ ] Integration tests pass against a PostgreSQL test database
- [ ] Tests cover successful report generation with grouped licenses
- [ ] Tests cover compliance flagging for non-compliant licenses
- [ ] Tests cover the 404 response for non-existent SBOM IDs
- [ ] Tests verify transitive dependency licenses are included

## Test Requirements
- [ ] Integration test: SBOM with all compliant licenses returns report with all groups having `compliant: true`
- [ ] Integration test: SBOM with a non-compliant license returns report with the flagged group having `compliant: false`
- [ ] Integration test: SBOM with mixed compliant and non-compliant licenses returns correct flags per group
- [ ] Integration test: non-existent SBOM ID returns 404 status
- [ ] Integration test: SBOM with no packages returns empty groups array

## Dependencies
- Depends on: Task 3 -- Add license report endpoint
- Depends on: Task 4 -- Add license policy configuration

## Description Digest
sha256-md:93c172452ed70c4e91e5efc8879f6210a412f60c0863b1cac1de46e40f1b0423
