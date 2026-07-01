# Task 5 — Add integration tests for license report endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the license compliance report endpoint covering the key use cases: a fully compliant SBOM, an SBOM with non-compliant licenses, transitive dependency inclusion, the CI/CD gate scenario (checking top-level compliant flag), and performance characteristics for large SBOMs. These tests validate the end-to-end behavior from HTTP request through service to database.

## Files to Modify
- `tests/Cargo.toml` — add any necessary test dependencies (if not already present)

## Files to Create
- `tests/api/license_report.rs` — integration tests for GET /api/v2/sbom/{id}/license-report

## Implementation Notes
- Follow the existing integration test pattern established in `tests/api/sbom.rs` and `tests/api/advisory.rs`:
  - Tests hit a real PostgreSQL test database
  - Use `assert_eq!(resp.status(), StatusCode::OK)` pattern for status assertions
  - Set up test data by ingesting SBOMs with known package-license mappings
- Test scenarios to cover:
  1. **All compliant**: SBOM with packages having only allowed licenses (MIT, Apache-2.0) — verify all groups have `compliant: true` and top-level `compliant: true`
  2. **Mixed compliance**: SBOM with both allowed and denied licenses — verify correct flags per group and top-level `compliant: false`
  3. **Transitive dependencies**: SBOM with a dependency tree where a transitive dep has a non-compliant license — verify the transitive dep appears in the report
  4. **CI/CD gate**: verify the top-level `compliant` boolean can be used programmatically to gate builds (essentially the same as checking `response.compliant == false`)
  5. **Empty SBOM**: SBOM with no packages — verify empty groups and compliant response
  6. **Unknown SBOM**: request with non-existent SBOM ID — verify 404 response
- Consider adding a test that verifies performance for a larger dataset (not a strict p95 assertion, but a sanity check that report generation completes within a reasonable time)

## Reuse Candidates
- `tests/api/sbom.rs` — follow test setup and assertion patterns for SBOM endpoint tests
- `tests/api/advisory.rs` — follow test structure and database setup patterns
- `tests/api/search.rs` — additional reference for integration test patterns

## Acceptance Criteria
- [ ] All integration tests pass against a test PostgreSQL database
- [ ] Tests cover compliant, non-compliant, mixed, and edge case scenarios
- [ ] Tests verify response shape matches the LicenseReportSummary schema
- [ ] Tests verify transitive dependency inclusion in the report

## Test Requirements
- [ ] Integration test: all-compliant SBOM returns compliant: true for all groups
- [ ] Integration test: SBOM with denied license returns compliant: false for that group
- [ ] Integration test: transitive dependency with non-compliant license appears in report
- [ ] Integration test: empty SBOM returns empty groups array
- [ ] Integration test: non-existent SBOM ID returns 404
- [ ] Integration test: response JSON shape matches specification

## Verification Commands
- `cargo test --test api -- license_report` — run license report integration tests

## Dependencies
- Depends on: Task 4 — Add license report REST endpoint
