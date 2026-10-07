## Repository
trustify-backend

## Target Branch
main

## Description
Add integration tests for the license compliance report endpoint (`GET /api/v2/sbom/{id}/license-report`). Tests verify end-to-end behavior: ingesting an SBOM with packages that have various licenses, generating the compliance report, and validating the response structure, grouping, compliance flags, and edge cases. Tests hit a real PostgreSQL test database following the project's established integration testing pattern.

## Files to Create
- `tests/api/license_report.rs` -- integration tests covering the license report endpoint: happy path with mixed compliant/non-compliant licenses, transitive dependency inclusion, empty SBOM, missing SBOM (404), and performance baseline for large SBOMs

## Files to Modify
- `tests/Cargo.toml` -- add test module reference if required by the project's test registration pattern

## Implementation Notes
- Per CONVENTIONS.md $Testing: integration tests in `tests/api/` must hit a real PostgreSQL test database using the established test setup pattern. Use `assert_eq!(resp.status(), StatusCode::OK)` for status assertions.
  Applies: task creates `tests/api/license_report.rs` matching the convention's Rust test file scope.
  See `tests/api/sbom.rs` for the established integration test pattern including test database setup, HTTP client creation, and response assertion style.
- Test data setup: ingest a test SBOM with known packages and license mappings before calling the report endpoint. Reuse existing test fixtures from the SBOM tests if available.
- Include a test case that verifies transitive dependencies appear in the report (not just direct SBOM packages).
- Include a test case verifying that the license policy configuration is respected (denied licenses result in `compliant: false`).

## Reuse Candidates
- `tests/api/sbom.rs` -- existing SBOM endpoint integration tests; reuse test setup pattern (database initialization, HTTP client, SBOM ingestion helpers)
- `tests/api/advisory.rs` -- additional integration test pattern reference for assertion style and error case testing

## Acceptance Criteria
- [ ] Integration test: valid SBOM returns 200 with packages grouped by license
- [ ] Integration test: non-compliant licenses (per policy) have `compliant: false`
- [ ] Integration test: transitive dependencies are included in the report groups
- [ ] Integration test: SBOM with no packages returns 200 with empty groups array
- [ ] Integration test: non-existent SBOM ID returns 404
- [ ] Integration test: invalid SBOM ID format returns appropriate error response
- [ ] All tests pass against the PostgreSQL test database

## Test Requirements
- [ ] Happy path: ingest SBOM with MIT and GPL-3.0 licensed packages, verify MIT group is compliant and GPL-3.0 group is non-compliant
- [ ] Transitive deps: ingest SBOM with nested dependencies, verify all levels appear in the report
- [ ] Empty SBOM: ingest SBOM with no packages, verify empty groups response
- [ ] Not found: request report for non-existent SBOM UUID, verify 404
- [ ] Policy enforcement: verify that the configured license policy determines compliance flags

## Verification Commands
- `cargo test -p trustify-tests -- license_report` -- all integration tests pass

## Dependencies
- Depends on: Task 3 -- Add license report REST endpoint
