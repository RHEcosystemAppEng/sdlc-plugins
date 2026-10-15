## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the license compliance report endpoint. Tests verify the full request-response cycle through the API, including compliant and non-compliant license scenarios, transitive dependency inclusion, empty SBOM handling, and error cases. Tests follow the existing integration test pattern in `tests/api/`.

## Files to Create
- `tests/api/license_report.rs` -- integration tests for `GET /api/v2/sbom/{id}/license-report`

## Files to Modify
- `tests/Cargo.toml` -- add test module dependency if needed for the new test file

## Implementation Notes
- Follow the existing integration test pattern: see `tests/api/sbom.rs` for the SBOM endpoint integration tests as the structural reference. Tests should use the same test database setup, HTTP client pattern, and assertion style.
- Use `assert_eq!(resp.status(), StatusCode::OK)` pattern for status code assertions per the project testing convention.
- Test against a real PostgreSQL test database as per the project's testing approach (not mocks).
- Test data setup: ingest a test SBOM with known package-license mappings before running assertions. Include packages with both compliant and non-compliant licenses relative to the test policy.
- Include a test for transitive dependency inclusion: create an SBOM with a dependency chain (A depends on B depends on C) and verify all three appear in the license report.
- Include a performance-oriented test: create an SBOM with a large number of packages (approaching 1000) and verify the endpoint responds within acceptable time bounds (p95 < 500ms NFR).
- Per docs/constraints.md S5.11: add doc comments to every test function.
- Per docs/constraints.md S5.12: add given-when-then inline comments to non-trivial test functions.

## Reuse Candidates
- `tests/api/sbom.rs` -- existing SBOM integration tests; reference for test setup, HTTP client usage, and assertion patterns
- `tests/api/advisory.rs` -- additional reference for integration test structure and test data setup

## Acceptance Criteria
- [ ] Integration test: valid SBOM with all compliant licenses returns 200 with all groups having `compliant: true`
- [ ] Integration test: SBOM with a non-compliant license returns 200 with the violating group having `compliant: false`
- [ ] Integration test: SBOM with transitive dependencies includes all transitive packages in the report
- [ ] Integration test: non-existent SBOM ID returns 404
- [ ] Integration test: SBOM with no packages returns 200 with an empty groups array
- [ ] Integration test: response JSON shape matches `{ groups: [{ license, packages, compliant }] }`
- [ ] All test functions have doc comments

## Test Requirements
- [ ] Test compliant-only SBOM: ingest SBOM with packages all having MIT license (allowed), verify all groups report `compliant: true`
- [ ] Test non-compliant SBOM: ingest SBOM with a package using GPL-3.0 (denied), verify the GPL-3.0 group reports `compliant: false`
- [ ] Test mixed compliance: ingest SBOM with both allowed and denied licenses, verify correct per-group compliance flags
- [ ] Test transitive dependencies: ingest SBOM with a dependency chain, verify all transitive packages appear in the report
- [ ] Test empty SBOM: ingest SBOM with no packages, verify empty groups response
- [ ] Test invalid SBOM ID: request a non-existent SBOM ID, verify 404 response
- [ ] Test large SBOM: ingest SBOM with ~500 packages, verify the endpoint responds within 500ms

## Verification Commands
- `cargo test --test api license_report` -- run all license report integration tests, expect all pass
- `cargo test --test api` -- run all API integration tests to confirm no regressions

## Dependencies
- Depends on: Task 1 -- Add license compliance report model and policy configuration
- Depends on: Task 2 -- Add license compliance report service with transitive dependency resolution
- Depends on: Task 3 -- Add license compliance report endpoint
