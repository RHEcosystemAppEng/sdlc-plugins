# Task 5 — Integration Tests for Advisory Summary Endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Add integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint covering the primary success path, error cases, severity counting correctness, deduplication, and threshold filtering. These tests follow the existing integration test pattern in `tests/api/` and run against a real PostgreSQL test database.

## Files to Create
- `tests/api/sbom_advisory_summary.rs` — Integration test module containing test functions for the advisory summary endpoint. Each test sets up fixture data (SBOM, advisories, sbom_advisory links), makes HTTP requests to the endpoint, and asserts on response status and body.

## Files to Modify
- `tests/api/sbom.rs` — If SBOM test fixture setup helpers are defined here and not already shared, extract them or reference them from the new test file. Alternatively, if tests use a shared test harness module, add imports there.

## Reuse Candidates
- `tests/api/sbom.rs` — Existing SBOM integration tests; follow the same test setup pattern (database seeding, HTTP client creation, request/response assertion style).
- `tests/api/advisory.rs` — Existing advisory integration tests; reuse advisory fixture creation patterns for setting up test data with known severity values.

## Implementation Notes
Follow the existing integration test pattern in `tests/api/sbom.rs` and `tests/api/advisory.rs`. Tests should:
1. Seed the test database with an SBOM and a known set of advisories at various severity levels, linked via `sbom_advisory` records.
2. Use the test HTTP client to call `GET /api/v2/sbom/{id}/advisory-summary`.
3. Assert response status with `assert_eq!(resp.status(), StatusCode::OK)`.
4. Deserialize the response body and assert exact counts match the seeded data.

Per CONVENTIONS.md §Testing: integration tests in `tests/api/` hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern. Applies: task creates `tests/api/sbom_advisory_summary.rs` matching the convention's `tests/api/` directory scope.

## Acceptance Criteria
- [ ] Integration test file exists at `tests/api/sbom_advisory_summary.rs`
- [ ] All tests pass against PostgreSQL test database
- [ ] Test coverage includes success path, 404 error, deduplication, and threshold filter
- [ ] Tests follow the existing assertion pattern using `StatusCode` comparisons

## Test Requirements
- [ ] Test: valid SBOM with mixed-severity advisories returns correct counts for each severity level and correct total
- [ ] Test: non-existent SBOM ID returns 404 status
- [ ] Test: SBOM with duplicate advisory links (same advisory linked multiple times) returns deduplicated counts
- [ ] Test: SBOM with zero advisories returns all-zero counts with 200 status
- [ ] Test: `?threshold=high` query param returns counts only for critical and high, with medium and low as zero
- [ ] Test: `?threshold=critical` query param returns only critical count with all others as zero
- [ ] Test: response includes `Cache-Control` header with `max-age=300`

## Dependencies
- Depends on: Task 3 — Advisory Summary Endpoint and Route Registration (endpoint must exist to test it)

[sdlc-workflow] Description digest: sha256-md:693689e894a5c12590410abf5d78d0d9e5f4bab00e58df25edfb9b83b2f074ac
