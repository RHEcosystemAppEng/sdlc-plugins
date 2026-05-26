# Task 5 — Add end-to-end integration tests for the license report endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the `GET /api/v2/sbom/{id}/license-report` endpoint. These tests verify the full request/response lifecycle including compliance evaluation, transitive dependency inclusion, edge cases, and performance characteristics. The tests use the existing integration test infrastructure that hits a real PostgreSQL test database.

## Files to Create
- `tests/api/license_report.rs` — Integration tests for the license report endpoint covering the scenarios listed in Test Requirements below.

## Files to Modify
- `tests/Cargo.toml` — Add any necessary test dependencies if not already present (inspect to confirm).

## Implementation Notes
- Follow the existing integration test patterns in `tests/api/` — see `sbom.rs` and `advisory.rs` for how tests set up test data, make HTTP requests, and assert on responses.
- Use the `assert_eq!(resp.status(), StatusCode::OK)` pattern consistent with existing tests.
- Test data setup: ingest an SBOM with packages that have known licenses (some allowed by policy, some denied) to create a predictable test scenario.
- For the transitive dependency test: set up a dependency chain (A depends on B depends on C) and verify all three appear in the report.
- For the CI/CD gate use case: verify that when any group has `compliant: false`, a consumer can detect it by checking the response.
- Per docs/constraints.md §5.11: add a doc comment to every test function.
- Per docs/constraints.md §5.12: add given-when-then inline comments to non-trivial test functions.
- Per docs/constraints.md §5.9: consider parameterized tests when multiple test cases exercise the same behavior (e.g., testing different license combinations).
- Per docs/constraints.md §5.10: check sibling tests in `tests/api/sbom.rs` to see whether parameterized test patterns are used in this project before introducing them.

## Reuse Candidates
- `tests/api/sbom.rs` — existing SBOM endpoint tests showing test setup, HTTP client usage, and assertion patterns.
- `tests/api/advisory.rs` — additional integration test examples for API endpoints.

## Acceptance Criteria
- [ ] Integration tests pass against a test PostgreSQL database
- [ ] Tests cover the happy path (compliant and non-compliant licenses), edge cases (empty SBOM, unknown licenses), and error cases (nonexistent SBOM)
- [ ] Tests verify transitive dependency inclusion
- [ ] Test functions have doc comments and given-when-then inline comments where applicable

## Test Requirements
- [ ] Test: happy path — SBOM with packages under MIT (allowed) and GPL-3.0 (denied) licenses returns correct groups with correct compliance flags
- [ ] Test: all-compliant — SBOM where all packages have allowed licenses returns all groups with `compliant: true`
- [ ] Test: transitive dependencies — SBOM with a dependency chain verifies transitive packages appear in the report with `transitive: true`
- [ ] Test: empty SBOM — SBOM with no packages returns an empty groups array
- [ ] Test: nonexistent SBOM — request for a nonexistent ID returns 404
- [ ] Test: unknown license — package with a license not in the policy is handled gracefully (grouped and flagged appropriately)

## Dependencies
- Depends on: Task 4 — Add GET /api/v2/sbom/{id}/license-report endpoint
