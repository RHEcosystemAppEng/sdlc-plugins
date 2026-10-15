## Repository
trustify-backend

## Target Branch
main

## Description
Add integration tests for the license report endpoint covering the happy path, error cases, compliance evaluation, and transitive dependency inclusion. Tests follow the existing integration test pattern in `tests/api/` using a real PostgreSQL test database.

## Files to Create
- `tests/api/license_report.rs` — Integration tests for `GET /api/v2/sbom/{id}/license-report`

## Files to Modify
- `tests/Cargo.toml` — Add the new test file to the test harness if required by the project's test configuration

## Implementation Notes
- Follow the existing integration test pattern in `tests/api/sbom.rs` and `tests/api/advisory.rs` for test setup, database seeding, and assertion style.
  Applies: task creates `tests/api/license_report.rs` matching the convention's Rust source file scope.
- Per Key Conventions (Testing): integration tests hit a real PostgreSQL test database; use the `assert_eq!(resp.status(), StatusCode::OK)` pattern for status code assertions.
  Applies: task creates `tests/api/license_report.rs` matching the convention's Rust test file scope.
- Set up test data by ingesting an SBOM with known packages and license mappings. Use the existing ingestor infrastructure from `modules/ingestor/` to create realistic test data.
- Test scenarios should include:
  - SBOM with packages having various licenses (MIT, Apache-2.0, GPL-3.0)
  - SBOM with transitive dependencies to verify they appear in the report
  - SBOM with packages that have no license mapping
  - Non-existent SBOM ID
  - Policy configuration with denied licenses to verify compliance flags
- Assert on the full response shape, not just status codes — verify `groups` array content, `compliant` flag values, and package list correctness.

## Reuse Candidates
- `tests/api/sbom.rs` — reference for SBOM endpoint test setup and database seeding pattern
- `tests/api/advisory.rs` — reference for integration test structure and assertions
- `modules/ingestor/src/graph/sbom/mod.rs` — SBOM ingestion for creating test data with known packages

## Acceptance Criteria
- [ ] Integration test verifies 200 response with correct `LicenseReport` shape for an SBOM with known license data
- [ ] Integration test verifies packages are correctly grouped by license
- [ ] Integration test verifies `compliant` flag is `false` for denied licenses and `true` for allowed licenses
- [ ] Integration test verifies transitive dependencies are included in the report
- [ ] Integration test verifies 404 response for a non-existent SBOM ID
- [ ] Integration test verifies packages without license data are handled gracefully
- [ ] All tests pass with `cargo test --test api`

## Test Requirements
- [ ] Happy path: SBOM with MIT and Apache-2.0 packages returns grouped report with `compliant: true`
- [ ] Denied license: SBOM with GPL-3.0 package returns group with `compliant: false`
- [ ] Transitive deps: SBOM with transitive dependencies includes them in the report
- [ ] No license: packages without license mapping appear in the report under a fallback group
- [ ] Not found: non-existent SBOM ID returns 404 status
- [ ] Empty SBOM: SBOM with no packages returns an empty `groups` array

## Verification Commands
- `cargo test --test api -- license_report` — run all license report integration tests, expect all to pass
- `cargo test --test api` — run full integration test suite, expect no regressions

## Dependencies
- Depends on: Task 4 — Add license report endpoint
