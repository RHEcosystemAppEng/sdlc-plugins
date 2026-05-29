## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the license compliance report endpoint. The tests exercise the full request-response cycle against a real PostgreSQL test database, covering the happy path, error cases, policy-based compliance evaluation, and transitive dependency inclusion.

## Files to Create
- `tests/api/license_report.rs` — integration tests for `GET /api/v2/sbom/{id}/license-report`

## Files to Modify
- `tests/Cargo.toml` — add any necessary test dependencies if not already present (verify during implementation)

## Implementation Notes
- Follow the integration test pattern established in `tests/api/sbom.rs` and `tests/api/advisory.rs` — these tests hit a real PostgreSQL test database and use the `assert_eq!(resp.status(), StatusCode::OK)` pattern.
- Test setup should:
  1. Create a test SBOM with known packages and licenses using the ingestion pipeline
  2. Set up a license policy file in the test's temp directory
  3. Call the license report endpoint and verify the response
- Test cases to implement:
  - **Happy path**: ingest an SBOM with packages having MIT, Apache-2.0, and GPL-3.0 licenses; call the endpoint; verify groups are correctly formed with one entry per license
  - **Non-compliant detection**: configure a policy that denies GPL-3.0; verify the GPL-3.0 group has `compliant: false` while MIT and Apache-2.0 have `compliant: true`
  - **Transitive dependencies**: ingest an SBOM where package A depends on package B (transitive); verify both appear in the report
  - **Empty SBOM**: call the endpoint for an SBOM with no packages; verify an empty groups array is returned
  - **Not found**: call with a non-existent SBOM ID; verify 404 response
- Per constraints doc section 2 (Commit Rules): use Conventional Commits format, reference TC-9004 in the footer, include `--trailer="Assisted-by: Claude Code"`.

## Reuse Candidates
- `tests/api/sbom.rs` — demonstrates the test setup pattern: database seeding, HTTP request construction, response assertion for SBOM endpoints
- `tests/api/advisory.rs` — demonstrates a similar test setup pattern for advisory endpoints; useful as a second reference for test structure
- `tests/api/search.rs` — demonstrates test patterns for endpoints that return structured query results

## Acceptance Criteria
- [ ] All integration tests pass against a PostgreSQL test database
- [ ] Happy path test verifies correct license grouping
- [ ] Non-compliant license detection is tested with a deny-list policy
- [ ] Transitive dependency licenses are verified in the report
- [ ] Edge cases (empty SBOM, non-existent SBOM) are covered
- [ ] Tests follow the existing test patterns in `tests/api/`

## Test Requirements
- [ ] Integration test: happy path — SBOM with multiple licenses returns correctly grouped report
- [ ] Integration test: compliance — denied license is flagged as non-compliant
- [ ] Integration test: transitive deps — indirect dependency licenses appear in report
- [ ] Integration test: empty SBOM — returns empty groups array with zero counts
- [ ] Integration test: 404 — non-existent SBOM ID returns 404

## Verification Commands
- `cargo test --test api license_report` — run all license report integration tests, expect all to pass

## Dependencies
- Depends on: Task 3 — Add license report endpoint

[sdlc-workflow] Description digest: sha256:3a5ca82e6d7965ade5a6b7e6021d2dca40cdacd7fad2c0e8ed48794c61a29889
