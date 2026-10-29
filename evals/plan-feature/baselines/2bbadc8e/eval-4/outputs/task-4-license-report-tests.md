## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the license report endpoint (`GET /api/v2/sbom/{id}/license-report`) in the existing test infrastructure. These tests validate the complete request-response cycle including database queries, transitive dependency resolution, and license compliance checking against a test PostgreSQL database.

## Files to Create
- `tests/api/license_report.rs` — Integration tests for the license report endpoint covering: successful report generation, non-existent SBOM handling, compliance flagging accuracy, transitive dependency inclusion, and performance characteristics

## Files to Modify
- `tests/Cargo.toml` — Ensure test dependencies include any new crates needed for the license report test fixtures (e.g., test SBOM/package data setup)

## Implementation Notes
- Follow the integration test pattern established by existing tests in `tests/api/`: `tests/api/sbom.rs` (SBOM endpoint tests), `tests/api/advisory.rs` (advisory endpoint tests), and `tests/api/search.rs` (search endpoint tests).
  Per CONVENTIONS.md: integration tests in `tests/api/` hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern.
  Applies: task creates `tests/api/license_report.rs` matching the convention's `.rs` test file scope.
- Tests should set up test data (SBOMs with packages and license mappings) using the existing test infrastructure patterns seen in `tests/api/sbom.rs`.
- Each test should have a doc comment explaining its purpose, and non-trivial tests should use given-when-then inline comments.
- Test at least the following scenarios:
  1. SBOM with packages having only compliant licenses → all groups have `compliant: true`
  2. SBOM with packages having non-compliant licenses → relevant groups have `compliant: false`
  3. SBOM with transitive dependencies → transitive packages appear in the report
  4. Non-existent SBOM ID → 404 response
  5. SBOM with no packages → empty groups list

## Reuse Candidates
- `tests/api/sbom.rs` — Existing SBOM integration tests; reference for test setup, HTTP client configuration, and assertion patterns
- `tests/api/advisory.rs` — Additional reference for integration test patterns and test data setup
- `entity/src/package_license.rs` — Package-License mapping entity needed for setting up test license data

## Acceptance Criteria
- [ ] Integration tests exist for the license report endpoint in `tests/api/license_report.rs`
- [ ] Tests cover all success and error scenarios (valid SBOM, non-existent SBOM, mixed compliance, transitive dependencies, empty SBOM)
- [ ] Tests follow the existing integration test patterns (real PostgreSQL database, status code assertions)
- [ ] All tests pass in CI with the test PostgreSQL database

## Test Requirements
- [ ] Test: valid SBOM with compliant licenses returns 200 with all groups marked compliant
- [ ] Test: valid SBOM with non-compliant licenses returns 200 with flagged groups
- [ ] Test: transitive dependencies are included in the license report
- [ ] Test: non-existent SBOM ID returns 404
- [ ] Test: SBOM with no packages returns 200 with empty groups
- [ ] Test: response JSON structure matches the expected schema

## Verification Commands
- `cargo test --test license_report` — all integration tests pass

## Dependencies
- Depends on: Task 3 — Add license report endpoint and route registration
