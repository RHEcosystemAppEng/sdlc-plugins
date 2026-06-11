## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the license compliance report endpoint. These tests verify end-to-end behavior by hitting a real PostgreSQL test database, following the project's established integration test pattern. The tests cover the happy path, error cases, compliance policy enforcement, and transitive dependency inclusion.

## Files to Create
- `tests/api/license_report.rs` — integration tests for `GET /api/v2/sbom/{id}/license-report` covering happy path, error cases, and compliance scenarios

## Files to Modify
- `tests/Cargo.toml` — add any necessary test dependencies if not already present

## Implementation Notes
- Follow the integration test pattern established in `tests/api/sbom.rs` and `tests/api/advisory.rs` — tests hit a real PostgreSQL test database and use the `assert_eq!(resp.status(), StatusCode::OK)` pattern.
- Test fixtures should ingest an SBOM with known packages and license data before calling the report endpoint. Use the SBOM ingestion flow from `modules/ingestor/src/graph/sbom/mod.rs` or an equivalent test helper to set up test data.
- Test scenarios to cover:
  1. **Happy path**: SBOM with multiple packages across different licenses returns a correctly grouped report
  2. **Non-compliant licenses**: configure a policy that denies a specific license and verify the corresponding group has `compliant: false`
  3. **All compliant**: SBOM where all licenses are allowed returns all groups with `compliant: true`
  4. **Transitive dependencies**: SBOM with transitive dependency chains verifies that transitive package licenses are included
  5. **Empty SBOM**: SBOM with no packages returns an empty groups array
  6. **Non-existent SBOM**: requesting a report for a non-existent SBOM ID returns 404
- Reference the existing test files for patterns on test database setup, HTTP client construction, and assertion style.

## Reuse Candidates
- `tests/api/sbom.rs` — demonstrates the established integration test pattern for SBOM endpoints; follow this pattern for test structure, database setup, and HTTP assertions
- `tests/api/advisory.rs` — another example of the integration test pattern; useful as a secondary reference
- `modules/ingestor/src/graph/sbom/mod.rs` — SBOM ingestion logic that can be used to set up test fixtures with known package/license data

## Acceptance Criteria
- [ ] Integration test file exists at `tests/api/license_report.rs`
- [ ] All test scenarios pass against a PostgreSQL test database
- [ ] Tests verify correct JSON response structure
- [ ] Tests verify compliance flag behavior with denied licenses
- [ ] Tests verify transitive dependency inclusion
- [ ] Tests verify 404 for non-existent SBOMs
- [ ] Test patterns are consistent with existing tests in `tests/api/`

## Test Requirements
- [ ] Happy path test: SBOM with packages across MIT, Apache-2.0, and GPL-3.0 licenses returns correct groups
- [ ] Non-compliant test: policy denying GPL-3.0 results in that group having `compliant: false`
- [ ] All-compliant test: permissive policy results in all groups having `compliant: true`
- [ ] Transitive dependency test: packages from transitive dependencies appear in the report
- [ ] Empty SBOM test: returns `{ "groups": [] }`
- [ ] 404 test: non-existent SBOM ID returns HTTP 404

## Verification Commands
- `cargo test --test api license_report` — should pass all integration tests

## Dependencies
- Depends on: Task 3 — Add license report endpoint
