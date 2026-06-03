# Task 5 — Add integration tests for license compliance report endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the license compliance report endpoint. The tests verify end-to-end behavior including correct license grouping, compliance flagging, transitive dependency inclusion, error handling, and performance characteristics. These tests exercise the full stack from HTTP request through service to database.

## Files to Create
- `tests/api/license_report.rs` — Integration tests for the license report endpoint

## Files to Modify
- `tests/Cargo.toml` — Add the new test file to the test harness if needed (check if tests are auto-discovered or explicitly listed)

## Implementation Notes
- Follow the integration test pattern established in `tests/api/sbom.rs` and `tests/api/advisory.rs`:
  - Tests hit a real PostgreSQL test database
  - Use `assert_eq!(resp.status(), StatusCode::OK)` pattern for status assertions
  - Set up test data by ingesting an SBOM with known package-license data before each test
- Test scenarios should cover:
  1. **Happy path**: SBOM with packages having known licenses, verify grouping and compliance flags
  2. **Non-compliant licenses**: SBOM with packages that have denied licenses, verify `compliant: false`
  3. **Mixed compliance**: SBOM with both compliant and non-compliant licenses in different groups
  4. **Transitive dependencies**: SBOM with a dependency tree, verify transitive packages are included with `transitive: true`
  5. **Empty SBOM**: SBOM with no packages returns empty groups array
  6. **Non-existent SBOM**: returns 404 status
  7. **Performance baseline**: SBOM with many packages completes within a reasonable time (not a strict p95 test, but a sanity check)
- Test data setup: create test SBOMs using the ingestion infrastructure in `modules/ingestor/` or by directly inserting into the test database using SeaORM entities from `entity/src/`.
- Use a test-specific license policy configuration (not the default one) to control the test conditions precisely.

## Reuse Candidates
- `tests/api/sbom.rs` — SBOM endpoint integration test patterns (test setup, assertions, DB fixtures)
- `tests/api/advisory.rs` — Advisory endpoint integration test patterns
- `modules/ingestor/src/graph/sbom/mod.rs` — SBOM ingestion for setting up test data
- `entity/src/package_license.rs` — Direct entity insertion for test fixtures

## Acceptance Criteria
- [ ] All integration tests pass against a PostgreSQL test database
- [ ] Tests cover compliant, non-compliant, mixed, transitive, empty, and 404 scenarios
- [ ] Tests use the established integration test patterns from the `tests/api/` directory
- [ ] No flaky tests — each test is deterministic with controlled test data

## Test Requirements
- [ ] Integration test: valid SBOM returns 200 with correctly grouped license data
- [ ] Integration test: non-compliant license group has `compliant: false`
- [ ] Integration test: transitive dependencies appear with `transitive: true`
- [ ] Integration test: SBOM with no packages returns `{ "groups": [] }`
- [ ] Integration test: non-existent SBOM ID returns 404
- [ ] Integration test: response includes all packages from the SBOM (no packages missing)

## Verification Commands
- `cargo test --test api` — all integration tests pass including new license report tests

## Dependencies
- Depends on: Task 4 — Add GET /api/v2/sbom/{id}/license-report endpoint
