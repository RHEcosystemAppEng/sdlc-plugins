# Task 4 — Add integration tests for the license compliance report endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the license compliance report endpoint. These tests exercise the full stack — from HTTP request through service logic to database queries — using the project's established integration test pattern with a real PostgreSQL test database. The tests validate the core use cases: generating a compliance report, handling non-compliant licenses, transitive dependency inclusion, and error cases.

## Files to Create
- `tests/api/license_report.rs` — Integration tests for GET /api/v2/sbom/{id}/license-report

## Files to Modify
- `tests/Cargo.toml` — Add the new test file to the test configuration if required by the project's test setup

## Implementation Notes
- Follow the existing integration test pattern established in `tests/api/sbom.rs` — use the same test database setup, HTTP client initialization, and assertion patterns (e.g., `assert_eq!(resp.status(), StatusCode::OK)`).
- See `tests/api/advisory.rs` and `tests/api/search.rs` for additional examples of the test pattern across different modules.
- Test fixtures should set up SBOMs with known packages and license data via the ingestion pipeline or direct database insertion, depending on the existing test patterns.
- Include test cases for both use cases from the feature description:
  - UC-1: Compliance officer generates a report and reviews flagged licenses
  - UC-2: CI/CD pipeline checks for `compliant: false` groups to fail a build
- Per docs/constraints.md section 5.9-5.13: prefer parameterized tests when multiple test cases exercise the same behavior with different inputs; add doc comments to every test function; add given-when-then inline comments to non-trivial test functions.
- Per docs/constraints.md section 2 (Commit Rules): commits must reference TC-9004, follow Conventional Commits, and include the `Assisted-by: Claude Code` trailer.

## Reuse Candidates
- `tests/api/sbom.rs` — SBOM endpoint integration test patterns (setup, assertions, HTTP client usage)
- `tests/api/advisory.rs` — Advisory endpoint integration test patterns for a second reference
- `tests/api/search.rs` — Search endpoint integration test patterns for a third reference

## Acceptance Criteria
- [ ] All integration tests pass against a PostgreSQL test database
- [ ] Tests cover the happy path: SBOM with mixed compliant/non-compliant licenses
- [ ] Tests cover error cases: non-existent SBOM ID, SBOM with no packages
- [ ] Tests verify the response structure matches the API contract (groups, compliant flags, summary counts)
- [ ] Tests verify transitive dependencies are included in the report

## Test Requirements
- [ ] Integration test: SBOM with all-compliant licenses returns report with all groups marked `compliant: true`
- [ ] Integration test: SBOM with a denied license returns at least one group marked `compliant: false`
- [ ] Integration test: SBOM with transitive dependencies includes those packages in the report
- [ ] Integration test: non-existent SBOM ID returns 404
- [ ] Integration test: SBOM with no packages returns empty report with zero summary counts
- [ ] Integration test: response body deserializes correctly into the LicenseComplianceReport struct

## Verification Commands
- `cargo test --test api license_report` — all license report integration tests pass
- `cargo test --test api` — full integration test suite passes (no regressions)

## Dependencies
- Depends on: Task 3 — Add GET /api/v2/sbom/{id}/license-report endpoint
