## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the license compliance report endpoint. Tests cover the full request-response cycle against a test database, validating correct grouping by license, conflict detection, policy classification, error handling, and response shape.

## Files to Modify
- `tests/api/sbom.rs` -- add shared test fixture helpers for creating SBOMs with packages and license associations

## Files to Create
- `tests/api/license_report.rs` -- integration test suite for `GET /api/v2/sbom/{id}/license-report`

## Implementation Notes
- Follow the existing integration test patterns in `tests/api/sbom.rs` for test setup, database seeding, and HTTP assertions
- Test fixtures should:
  1. Create a test SBOM
  2. Create packages with known license associations via `package_license`
  3. Link packages to the SBOM via `sbom_package`
  4. Seed `license_policy` entries with known classifications
- Test scenarios:
  - **Happy path**: SBOM with packages under different licenses, verify grouping and classification
  - **Conflict detection**: Package with both "MIT" and "GPL-3.0-only" licenses, verify it appears in conflicts
  - **All compliant**: SBOM where all packages have "Allowed" licenses, verify summary counts
  - **Mixed compliance**: SBOM with Allowed, Denied, and ReviewRequired packages, verify counts
  - **Empty SBOM**: SBOM with no packages, verify empty report (not error)
  - **Unknown SBOM**: Request with non-existent UUID, verify 404
  - **No policy entries**: Packages with licenses not in policy table, verify default to ReviewRequired
- Use `reqwest` or the test HTTP client established in the test suite for making requests
- Assert on JSON response structure matching `LicenseReport` schema
- Per CONVENTIONS.md Key Conventions (Testing): integration tests go in `tests/api/` and hit a real PostgreSQL test database. Use `assert_eq!(resp.status(), StatusCode::OK)` pattern.
  Applies: task creates `tests/api/license_report.rs` matching the convention's test directory scope.

## Reuse Candidates
- `tests/api/sbom.rs` -- reference for test setup, database initialization, and assertion patterns
- `tests/api/advisory.rs` -- additional reference for integration test patterns

## Acceptance Criteria
- [ ] All integration tests pass against a clean test database
- [ ] Tests cover at least 5 distinct scenarios (happy path, conflicts, empty, not found, no policy)
- [ ] Test fixtures properly seed and clean up database state
- [ ] Tests validate response JSON structure, not just status codes

## Test Requirements
- [ ] Happy path: correct grouping, classification, and summary counts
- [ ] Conflict detection: conflicting licenses flagged correctly
- [ ] All-compliant SBOM: zero non-compliant and zero review-required counts
- [ ] Mixed-compliance SBOM: accurate breakdown of counts
- [ ] Empty SBOM: returns 200 with empty groups and conflicts, zero counts
- [ ] Non-existent SBOM: returns 404
- [ ] Missing policy: unclassified licenses default to ReviewRequired

## Dependencies
- Depends on: Task 4 -- Add license report endpoint
