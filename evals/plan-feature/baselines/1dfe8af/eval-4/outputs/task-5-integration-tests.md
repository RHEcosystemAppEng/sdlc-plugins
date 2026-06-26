## Repository
trustify-backend

## Target Branch
main

## Description
Add integration tests for the license compliance report endpoint. These tests verify end-to-end behavior including correct license grouping, compliance flag evaluation, transitive dependency inclusion, and error handling for invalid SBOM IDs. Tests follow the existing integration test pattern using a real PostgreSQL test database.

## Files to Create
- `tests/api/license_report.rs` — Integration tests for `GET /api/v2/sbom/{id}/license-report`

## Files to Modify
- `tests/Cargo.toml` — Add any necessary test dependencies if not already present

## Implementation Notes
- Follow the existing integration test pattern in `tests/api/sbom.rs` and `tests/api/advisory.rs` which use `assert_eq!(resp.status(), StatusCode::OK)` for status assertions and deserialize JSON response bodies.
- Test scenarios:
  1. **Happy path**: Ingest an SBOM with packages under known licenses (MIT, Apache-2.0, GPL-3.0), call the license report endpoint, verify the response groups packages correctly and flags GPL-3.0 as non-compliant per the default policy.
  2. **Empty SBOM**: Ingest an SBOM with no packages, verify the report returns an empty `groups` array with `total_packages: 0`.
  3. **All compliant**: Ingest an SBOM where every package has an allowed license, verify `non_compliant_count: 0` and all groups have `compliant: true`.
  4. **Transitive dependencies**: Ingest an SBOM with transitive dependency chains, verify all transitive packages appear in the report.
  5. **Not found**: Call the endpoint with a non-existent SBOM ID, verify HTTP 404.
- Use the existing SBOM ingestion test utilities to set up test data.

## Reuse Candidates
- `tests/api/sbom.rs` — Existing SBOM integration tests; reuse test setup patterns and HTTP client configuration
- `tests/api/advisory.rs` — Additional reference for integration test patterns

## Acceptance Criteria
- [ ] All five test scenarios pass against a PostgreSQL test database
- [ ] Tests verify JSON response structure (fields, types, grouping)
- [ ] Tests verify compliance flags match the default license policy
- [ ] Tests run as part of the standard `cargo test` suite

## Test Requirements
- [ ] Happy path test with mixed compliant/non-compliant licenses
- [ ] Empty SBOM test
- [ ] All-compliant SBOM test
- [ ] Transitive dependency inclusion test
- [ ] 404 for non-existent SBOM ID test

## Dependencies
- Depends on: Task 4 — Add license report endpoint handler

[sdlc-workflow] Description digest: sha256-md:ccdc5f430f099f81e604de018ea6f6e07801b202a36389c7fa8710cf21f6c73f
