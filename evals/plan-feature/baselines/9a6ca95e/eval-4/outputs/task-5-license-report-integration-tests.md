## Repository

trustify-backend

## Target Branch

main

## Description

Add comprehensive integration tests for the license compliance report endpoint. These tests cover the core use cases: successful report generation, compliance flagging, transitive dependency inclusion, and error handling. They follow the existing integration test patterns in the `tests/api/` directory.

## Files to Modify

- `tests/Cargo.toml` — add any necessary test dependencies if not already present

## Files to Create

- `tests/api/license_report.rs` — integration tests for `GET /api/v2/sbom/{id}/license-report`

## Implementation Notes

- Follow the integration test patterns in `tests/api/sbom.rs` and `tests/api/advisory.rs` for test setup, database fixture loading, and assertion style
- Tests should use a real PostgreSQL test database as described in the repository conventions
- Use the `assert_eq!(resp.status(), StatusCode::OK)` pattern consistent with existing tests
- Test fixture data should include:
  - An SBOM with packages having MIT (compliant) and GPL-3.0 (non-compliant) licenses
  - An SBOM with transitive dependencies having different licenses
  - An SBOM with no packages (edge case)
- Register the new test file in the test module structure if required by the existing test organization

## Acceptance Criteria

- All integration tests pass against a PostgreSQL test database
- Tests cover: successful report, compliance flagging, transitive deps, empty SBOM, non-existent SBOM
- Tests follow existing patterns and conventions from `tests/api/sbom.rs`
- `cargo test` passes with no failures

## Test Requirements

- `test_license_report_success` — ingest an SBOM with known packages and licenses, call the endpoint, verify the response groups are correct
- `test_license_report_compliance_flagging` — verify that GPL-3.0 packages are flagged as non-compliant and MIT packages as compliant
- `test_license_report_transitive_deps` — verify that transitive dependency licenses are included in the report
- `test_license_report_empty_sbom` — verify that an SBOM with no packages returns an empty groups array
- `test_license_report_not_found` — verify that requesting a report for a non-existent SBOM returns 404
