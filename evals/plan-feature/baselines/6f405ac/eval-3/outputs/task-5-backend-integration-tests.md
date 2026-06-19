## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add integration tests for the SBOM comparison endpoint that exercise the full HTTP request/response cycle against a real PostgreSQL test database. These tests verify the end-to-end behavior of the comparison feature: ingesting two SBOMs with known differences, calling the comparison endpoint, and asserting the diff result matches expectations.

## Files to Create
- `tests/api/sbom_compare.rs` — Integration tests for GET /api/v2/sbom/compare

## Implementation Notes
Follow the existing integration test pattern in `tests/api/sbom.rs`:
- Set up test data by ingesting two SBOMs with known package/advisory/license differences
- Call `GET /api/v2/sbom/compare?left={id}&right={id}` via the test HTTP client
- Assert response status and JSON body structure

Per CONVENTIONS.md §Testing: integration tests in `tests/api/` hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern. Applies: task creates `tests/api/sbom_compare.rs` matching the convention's `.rs` test file scope.

## Reuse Candidates
- `tests/api/sbom.rs` — reference for test setup, SBOM ingestion, and HTTP assertion patterns
- `tests/api/advisory.rs` — reference for advisory-related test data setup

## Dependencies
- Depends on: Task 4 — Backend comparison endpoint (endpoint must exist to test)

## Acceptance Criteria
- [ ] Integration test file exists at `tests/api/sbom_compare.rs`
- [ ] Tests pass against a real PostgreSQL test database
- [ ] At least one test verifies a successful comparison with known differences
- [ ] At least one test verifies error handling for invalid inputs

## Test Requirements
- [ ] Integration test: compare two SBOMs with added packages — response contains the added packages
- [ ] Integration test: compare two SBOMs with removed packages — response contains the removed packages
- [ ] Integration test: compare two SBOMs with version changes — response contains version changes with correct direction
- [ ] Integration test: compare two SBOMs with different advisories — response contains new and resolved vulnerabilities
- [ ] Integration test: compare two SBOMs with license changes — response contains license changes
- [ ] Integration test: compare with non-existent SBOM ID returns 404
- [ ] Integration test: compare with missing query params returns 400
