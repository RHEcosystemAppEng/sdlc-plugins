## Repository
trustify-backend

## Target Branch
main

## Description
Add integration tests for the license compliance report endpoint `GET /api/v2/sbom/{id}/license-report`. Tests verify the full request-response cycle against a real PostgreSQL test database, covering the happy path, edge cases (empty SBOM, unknown SBOM), and compliance flag behavior with both allowed and denied licenses.

## Files to Create
- `tests/api/license_report.rs` -- integration tests for the license report endpoint

## Implementation Notes
- Follow the integration test patterns established in `tests/api/sbom.rs` and `tests/api/advisory.rs`. Tests hit a real PostgreSQL test database and use the `assert_eq!(resp.status(), StatusCode::OK)` assertion pattern.
- Test setup should:
  1. Ingest a test SBOM with known packages and licenses (use existing ingestion utilities from the test helpers)
  2. Include packages with a mix of compliant and non-compliant licenses to verify flag behavior
  3. Include transitive dependencies to verify dependency tree walking
- Key test scenarios:
  - Happy path: SBOM with multiple packages across different licenses returns correctly grouped report
  - Compliance flags: packages with denied licenses (e.g., GPL-3.0) are flagged as `compliant: false`
  - Empty SBOM: SBOM with no packages returns an empty groups array
  - Non-existent SBOM: returns HTTP 404
  - Transitive dependencies: report includes licenses from the full dependency tree, not just direct dependencies
- Per CONVENTIONS.md §Testing: use integration tests in `tests/api/` with `assert_eq!(resp.status(), StatusCode::OK)` pattern.
  Applies: task creates `tests/api/license_report.rs` matching the convention's `.rs` test file scope.

## Reuse Candidates
- `tests/api/sbom.rs` -- existing SBOM endpoint integration tests; follow the same test setup, assertion, and teardown patterns
- `tests/api/advisory.rs` -- additional reference for integration test patterns with entity creation and validation

## Acceptance Criteria
- [ ] Integration test: `GET /api/v2/sbom/{id}/license-report` returns 200 with grouped license data for a valid SBOM
- [ ] Integration test: response includes compliance flags (true for allowed, false for denied licenses)
- [ ] Integration test: report includes transitive dependency licenses
- [ ] Integration test: empty SBOM returns 200 with empty groups array
- [ ] Integration test: non-existent SBOM ID returns 404
- [ ] All tests follow the established integration test patterns from `tests/api/sbom.rs`

## Test Requirements
- [ ] Test with SBOM containing multiple packages under MIT license (compliant) -- verify single group with `compliant: true`
- [ ] Test with SBOM containing a package under GPL-3.0 (denied) -- verify group with `compliant: false`
- [ ] Test with SBOM containing transitive dependencies -- verify all dependency licenses appear in report
- [ ] Test with SBOM that has no packages -- verify empty groups response
- [ ] Test with invalid SBOM ID -- verify 404 response

## Verification Commands
- `cargo test --test api -- license_report` -- integration tests pass against test database

## Dependencies
- Depends on: Task 3 -- Add license report endpoint and route registration
