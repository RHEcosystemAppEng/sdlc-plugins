## Repository
trustify-backend

## Target Branch
main

## Description
Add integration tests for the license compliance report endpoint
(`GET /api/v2/sbom/{id}/license-report`). The tests verify the full request-response
cycle against a real PostgreSQL test database, covering the happy path (SBOM with
packages and licenses), error cases (non-existent SBOM), and compliance policy
evaluation (compliant vs. non-compliant licenses, transitive dependencies).

## Files to Create
- `tests/api/license_report.rs` -- Integration tests for the license report endpoint

## Files to Modify
- `tests/Cargo.toml` -- Add test dependencies if needed (e.g., test fixtures for license data)

## Implementation Notes
- Follow the integration test pattern established in `tests/api/sbom.rs` and
  `tests/api/advisory.rs` -- tests use a real PostgreSQL test database, set up
  test data via the ingestion pipeline, and make HTTP requests to the running
  server.
- Per CONVENTIONS.md Section "Testing": tests hit a real PostgreSQL test database
  and use the `assert_eq!(resp.status(), StatusCode::OK)` pattern for status
  assertions.
  Applies: task creates `tests/api/license_report.rs` matching the convention's
  test file scope.
- Test scenarios should include:
  1. Ingest an SBOM with known packages and licenses, call the endpoint, verify
     the response groups packages correctly by license
  2. Configure a policy with a denied license, verify the `compliant` flag is
     `false` for the denied license group
  3. Verify transitive dependencies appear in the report
  4. Request a report for a non-existent SBOM ID, verify 404 response
  5. Ingest an SBOM with packages that have no license data, verify they appear
     in an appropriate group (e.g., "UNKNOWN" or "NOASSERTION")
- Use test fixtures that create a minimal SBOM with a known dependency tree and
  license assignments for deterministic assertions.

## Reuse Candidates
- `tests/api/sbom.rs` -- demonstrates the integration test pattern for SBOM
  endpoints; reuse the test server setup and SBOM ingestion helpers
- `tests/api/advisory.rs` -- demonstrates the assertion pattern and HTTP client
  setup for API tests
- `modules/ingestor/src/graph/sbom/mod.rs` -- SBOM ingestion logic; use this to
  set up test data

## Acceptance Criteria
- [ ] Integration test passes: valid SBOM returns 200 with correctly grouped license data
- [ ] Integration test passes: non-existent SBOM returns 404
- [ ] Integration test passes: denied license is flagged as non-compliant
- [ ] Integration test passes: transitive dependencies are included in the report
- [ ] All tests use the established test database pattern (no mocking the database)

## Test Requirements
- [ ] Test: GET /api/v2/sbom/{id}/license-report returns 200 with license groups for a valid SBOM
- [ ] Test: GET /api/v2/sbom/{id}/license-report returns 404 for non-existent SBOM
- [ ] Test: License groups contain correct package lists grouped by license identifier
- [ ] Test: Non-compliant licenses (per policy) have `compliant: false`
- [ ] Test: Transitive dependency licenses are included in the report

## Verification Commands
- `cargo test -p trustify-tests -- license_report` -- all integration tests pass
- `cargo test -p trustify-tests -- license_report --nocapture` -- run with output for debugging

## Dependencies
- Depends on: Task 1 -- Add license report model types and policy configuration
- Depends on: Task 2 -- Implement license compliance report service
- Depends on: Task 3 -- Add license compliance report REST endpoint
