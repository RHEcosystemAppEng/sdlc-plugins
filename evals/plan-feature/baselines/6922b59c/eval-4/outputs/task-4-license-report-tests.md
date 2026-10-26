# Task 4 — Add integration tests for license report endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Add integration tests for the `GET /api/v2/sbom/{id}/license-report` endpoint that verify end-to-end behavior against a real PostgreSQL test database. Tests should cover compliant SBOMs, non-compliant license detection, transitive dependency inclusion, and error cases.

## Files to Create
- `tests/api/license_report.rs` — integration tests for the license report endpoint

## Implementation Notes
- Follow the existing integration test pattern in `tests/api/sbom.rs` and `tests/api/advisory.rs` for test setup, database fixture creation, and assertion style.
- Tests should set up SBOM and package fixture data with known license assignments, then call the endpoint and assert on the response structure and compliance flags.
- Test scenarios:
  1. SBOM with all packages having allowed licenses: all groups should have `compliant: true`
  2. SBOM with a package having a denied license: that group should have `compliant: false`
  3. SBOM with transitive dependencies: all packages (direct and transitive) appear in the report
  4. SBOM with no packages: response should have an empty `groups` array
  5. Non-existent SBOM ID: response should be 404
- Per CONVENTIONS.md §Testing: use the established `assert_eq!(resp.status(), StatusCode::OK)` pattern and hit a real PostgreSQL test database.
  Applies: task creates `tests/api/license_report.rs` matching the convention's test file scope.
- Per CONVENTIONS.md §Error Handling: verify that error responses use the `AppError` format.
  Applies: task creates `tests/api/license_report.rs` matching the convention's `.rs` file scope.

## Reuse Candidates
- `tests/api/sbom.rs` — existing SBOM integration tests demonstrating test setup, fixture creation, and assertion patterns
- `tests/api/advisory.rs` — additional integration test examples with database fixtures
- `common/src/model/paginated.rs::PaginatedResults` — reference for understanding response wrapper patterns in existing tests

## Acceptance Criteria
- [ ] Integration test passes: SBOM with compliant licenses returns all groups with `compliant: true`
- [ ] Integration test passes: SBOM with a denied license returns that group with `compliant: false`
- [ ] Integration test passes: transitive dependencies are included in the license report
- [ ] Integration test passes: SBOM with no packages returns empty groups
- [ ] Integration test passes: non-existent SBOM returns HTTP 404
- [ ] All tests run against a real PostgreSQL test database following the existing test infrastructure

## Test Requirements
- [ ] Test compliant SBOM: create SBOM with packages having only allowed licenses, verify all groups are compliant
- [ ] Test non-compliant SBOM: create SBOM with a package using a denied license (e.g., GPL-3.0 when denied), verify the group is flagged
- [ ] Test transitive dependencies: create SBOM with direct and transitive package relationships, verify all appear in the report
- [ ] Test empty SBOM: create SBOM with no associated packages, verify empty groups array
- [ ] Test 404: request license report for a non-existent SBOM ID, verify 404 response
- [ ] Test response shape: verify the JSON response matches the documented `LicenseReport` contract

## Verification Commands
- `cargo test --test api -- license_report` — integration tests pass
- `cargo test --test api` — all integration tests pass (no regressions)

## Dependencies
- Depends on: Task 1 — Add license report model types and policy configuration
- Depends on: Task 2 — Implement license compliance report service
- Depends on: Task 3 — Add license report endpoint and register route
