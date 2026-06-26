## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add comprehensive integration tests for the SBOM comparison endpoint. These tests exercise the full HTTP request/response cycle against a real PostgreSQL test database, verifying correct diff computation, error handling, and response format.

## Files to Create
- `tests/api/sbom_compare.rs` — Integration tests for `GET /api/v2/sbom/compare`

## Files to Modify
- `tests/api/mod.rs` or test runner configuration — Register the new test module (if a mod.rs exists for test modules)

## Implementation Notes
Follow the integration test pattern in `tests/api/sbom.rs` and `tests/api/advisory.rs`. These tests hit a real PostgreSQL test database and use the `assert_eq!(resp.status(), StatusCode::OK)` assertion pattern.

Test setup should:
1. Ingest two test SBOMs with known package sets (some overlapping, some unique to each)
2. Ensure test packages have known licenses and linked advisories with known severities

Test cases:
- **Happy path**: Compare two SBOMs with known differences; assert each section of the response contains the expected items
- **Identical SBOMs**: Compare an SBOM with itself; assert all diff sections are empty arrays
- **Missing left parameter**: Send request without `left`; assert 400 status
- **Missing right parameter**: Send request without `right`; assert 400 status
- **Non-existent left SBOM**: Use a random UUID for `left`; assert 404 status
- **Non-existent right SBOM**: Use a random UUID for `right`; assert 404 status
- **Version change direction**: Include packages with version upgrades and downgrades; assert `direction` field is correct
- **Critical vulnerability highlighting**: Include a new vulnerability with "critical" severity; verify it appears in `new_vulnerabilities` with correct severity

## Reuse Candidates
- `tests/api/sbom.rs` — test structure, setup patterns, SBOM ingestion helpers
- `tests/api/advisory.rs` — advisory ingestion helpers for test data

## Acceptance Criteria
- [ ] At least 6 integration test cases covering happy path, edge cases, and error cases
- [ ] Tests use real PostgreSQL test database following existing test conventions
- [ ] All tests pass in CI

## Test Requirements
- [ ] Happy path test with known diff results
- [ ] Identity comparison test (SBOM compared with itself)
- [ ] Missing query parameter tests (400 responses)
- [ ] Non-existent SBOM ID tests (404 responses)
- [ ] Version direction correctness test
- [ ] Critical vulnerability presence test

## Verification Commands
- `cargo test --test api sbom_compare` — all integration tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch
- Depends on: Task 4 — Backend comparison endpoint

[sdlc-workflow] Description digest: sha256-md:25fc80d99414ff28fb92430693ad75b2f24c87766ca7cc39779b356ff359ead5
