## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the license compliance report endpoint. The tests cover the full request-response cycle against a real PostgreSQL test database, following the existing test patterns in `tests/api/`. The test suite validates correct license grouping, transitive dependency inclusion, policy compliance flagging, and error handling.

## Files to Create
- `tests/api/license_report.rs` — integration tests for the `GET /api/v2/sbom/{id}/license-report` endpoint

## Files to Modify
- `tests/Cargo.toml` — add the license_report test module to the test harness (if test modules are explicitly registered)

## Implementation Notes
- Per Key Conventions §Testing: integration tests in `tests/api/` hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern. Applies: task creates `tests/api/license_report.rs` matching the convention's test directory scope.
- Follow the testing pattern established in `tests/api/sbom.rs` and `tests/api/advisory.rs` — set up test data, make HTTP requests, and assert response status and body.
- Test data setup should include: ingesting an SBOM with packages that have various licenses (MIT, Apache-2.0, GPL-3.0), including packages with transitive dependencies.
- Ensure tests cover both the happy path (valid SBOM with licenses) and edge cases (empty SBOM, missing SBOM, SBOM with no license data).

## Reuse Candidates
- `tests/api/sbom.rs` — existing SBOM endpoint integration tests; follow the same test setup and assertion patterns
- `tests/api/advisory.rs` — existing advisory endpoint integration tests; reference for test data setup and teardown patterns

## Acceptance Criteria
- [ ] Integration tests pass against a PostgreSQL test database
- [ ] Tests cover: valid SBOM with multiple licenses grouped correctly
- [ ] Tests cover: compliance flags match the configured policy (compliant and non-compliant licenses)
- [ ] Tests cover: transitive dependencies are included in the report
- [ ] Tests cover: 404 response for non-existent SBOM ID
- [ ] Tests cover: SBOM with no packages returns an empty report
- [ ] Tests cover: packages with no license data are handled gracefully

## Test Requirements
- [ ] Test: GET /api/v2/sbom/{id}/license-report returns 200 with grouped licenses for a valid SBOM
- [ ] Test: report groups include correct package lists per license
- [ ] Test: non-compliant licenses (per policy) have `compliant: false`
- [ ] Test: approved licenses (per policy) have `compliant: true`
- [ ] Test: transitive dependency packages appear in the report with their licenses
- [ ] Test: GET /api/v2/sbom/{nonexistent}/license-report returns 404
- [ ] Test: SBOM with zero packages returns `{ groups: [] }`

## Verification Commands
- `cargo test --test api -- license_report` — runs all license report integration tests
- `cargo test --test api` — runs the full integration test suite to verify no regressions

## Dependencies
- Depends on: Task 1 — Add license policy configuration and license report models
- Depends on: Task 2 — Add license report service with transitive dependency resolution
- Depends on: Task 3 — Add GET /api/v2/sbom/{id}/license-report endpoint
