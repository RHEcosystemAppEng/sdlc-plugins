## Repository
trustify-backend

## Target Branch
main

## Description
Add integration tests for the license compliance report endpoint. Tests verify the full request/response cycle against a real PostgreSQL test database, covering the happy path (valid SBOM with mixed licenses and compliance policy), edge cases (empty SBOM, non-existent SBOM), and transitive dependency handling.

These tests follow the existing integration test patterns in `tests/api/`.

## Files to Create
- `tests/api/license_report.rs` — Integration tests for `GET /api/v2/sbom/{id}/license-report`

## Files to Modify
- `tests/Cargo.toml` — Add the new test file to the test binary if required by the project's test configuration

## Implementation Notes
- Follow the existing integration test pattern in `tests/api/sbom.rs` for test structure, test database setup, and assertion patterns.
- Use the `assert_eq!(resp.status(), StatusCode::OK)` pattern per codebase conventions.
- Test setup should:
  1. Ingest a test SBOM with known packages and licenses using the ingestion infrastructure
  2. Configure a test license policy with specific allowed/denied licenses
  3. Call the endpoint and verify the response
- Test cases should cover:
  - SBOM with multiple packages across different license types (MIT, Apache-2.0, GPL-3.0)
  - Policy marking GPL-3.0 as non-compliant — verify the response shows `compliant: false` for that group
  - SBOM with transitive dependencies — verify all dependencies appear in the report
  - Empty SBOM (no packages) — verify empty groups array
  - Non-existent SBOM ID — verify 404 response
- Deserialize the response body to verify the `LicenseReport` structure matches the API contract.

## Reuse Candidates
- `tests/api/sbom.rs` — Existing SBOM endpoint integration tests. Follow the same test setup, database seeding, and assertion patterns.
- `tests/api/advisory.rs` — Additional reference for integration test patterns with entity relationships.
- `modules/ingestor/src/graph/sbom/mod.rs` — SBOM ingestion logic. Use for setting up test data with known packages and licenses.

## Acceptance Criteria
- [ ] Integration tests exist for the license report endpoint in `tests/api/license_report.rs`
- [ ] Tests cover happy path: valid SBOM with mixed licenses returns correct grouping
- [ ] Tests cover compliance flagging: non-compliant licenses are flagged per policy
- [ ] Tests cover transitive dependencies: all linked packages appear in the report
- [ ] Tests cover error case: non-existent SBOM ID returns 404
- [ ] All tests pass against the PostgreSQL test database

## Test Requirements
- [ ] Integration test: valid SBOM with MIT and Apache-2.0 packages returns 200 with two groups, both compliant
- [ ] Integration test: valid SBOM with a GPL-3.0 package and a policy denying GPL-3.0 returns the GPL group with `compliant: false`
- [ ] Integration test: SBOM with transitive dependencies includes all transitive packages in the report
- [ ] Integration test: SBOM with no packages returns 200 with empty groups array
- [ ] Integration test: non-existent SBOM ID returns 404
- [ ] Integration test: response JSON shape matches `{ groups: [{ license, packages, compliant }] }`

## Verification Commands
- `cargo test --test api -- license_report` — run license report integration tests

## Dependencies
- Depends on: Task 3 — Add license report endpoint and route registration
