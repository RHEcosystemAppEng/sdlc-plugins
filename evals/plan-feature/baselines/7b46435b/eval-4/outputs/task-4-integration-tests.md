# Task 4 — Add integration tests for license report endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the `GET /api/v2/sbom/{id}/license-report` endpoint. Tests should cover the happy path (SBOM with packages grouped by license), edge cases (empty SBOM, missing SBOM), compliance flag validation (non-compliant licenses are correctly flagged), and transitive dependency inclusion.

These tests validate the end-to-end behavior of TC-9004 from HTTP request through service logic to database query.

## Files to Create
- `tests/api/license_report.rs` — integration tests for the license report endpoint

## Files to Modify
- `tests/Cargo.toml` — add test module registration if needed (check if tests use a `mod.rs` or are auto-discovered)

## Implementation Notes
- Follow the existing integration test pattern in `tests/api/sbom.rs` for test setup, database seeding, HTTP client usage, and assertion conventions.
- Integration tests hit a real PostgreSQL test database — see `tests/api/sbom.rs` for the test database setup and teardown pattern.
- Use `assert_eq!(resp.status(), StatusCode::OK)` pattern as documented in Key Conventions.
- Test scenarios should seed the database with:
  1. An SBOM with packages having various licenses (MIT, Apache-2.0, GPL-3.0-only)
  2. A license policy marking GPL-3.0-only as non-compliant
  3. Both direct and transitive package dependencies
- Verify response JSON structure matches `LicenseReport` schema: `{ "groups": [{ "license": "...", "packages": [...], "compliant": true/false }] }`
- Test the 404 case with a non-existent SBOM ID.
- Performance test (optional): seed 1000 packages and verify response time is under 500ms.
- Per CONVENTIONS.md: follow the integration test pattern where tests are in `tests/api/` and use a real database. Applies: task creates `tests/api/license_report.rs` matching the convention's test directory scope.
- Per docs/constraints.md section 5.11: add a doc comment to every test function.
- Per docs/constraints.md section 5.12: add given-when-then inline comments to non-trivial test functions.

## Reuse Candidates
- `tests/api/sbom.rs` — SBOM endpoint integration tests; follow the same test setup, seeding, and assertion patterns
- `tests/api/advisory.rs` — Advisory endpoint integration tests; additional reference for GET-by-ID test patterns
- `tests/api/search.rs` — Search endpoint tests; reference for test database seeding with multiple entity types

## Acceptance Criteria
- [ ] Integration test for GET /api/v2/sbom/{id}/license-report with a valid SBOM returns 200 and correct JSON
- [ ] Integration test verifies packages are grouped by license type
- [ ] Integration test verifies `compliant: false` for licenses in the non-compliant policy list
- [ ] Integration test verifies `compliant: true` for licenses not in the non-compliant list
- [ ] Integration test verifies transitive dependencies are included in the report
- [ ] Integration test for non-existent SBOM returns 404
- [ ] All tests pass in CI with `cargo test`

## Test Requirements
- [ ] Happy path: SBOM with 3+ packages across 2+ license types, verify grouping and compliance flags
- [ ] Empty SBOM: SBOM with no packages, verify empty groups array
- [ ] Non-existent SBOM: invalid SBOM ID, verify 404 response
- [ ] Mixed compliance: SBOM with both compliant and non-compliant licenses, verify correct per-group flags
- [ ] Transitive dependencies: verify that packages linked via transitive dependency relationships appear in the report

## Verification Commands
- `cargo test --test api -- license_report` — run the license report integration tests
- `cargo test` — verify all existing tests still pass (no regressions)

## Dependencies
- Depends on: Task 3 — Add GET /api/v2/sbom/{id}/license-report endpoint
