## Repository
trustify-backend

## Target Branch
main

## Description
Add integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint, covering the core scenarios: valid SBOM with advisories at multiple severity levels, nonexistent SBOM (404 response), advisory deduplication, and empty advisory set. Tests follow the existing integration test pattern in `tests/api/` using a real PostgreSQL test database.

## Files to Create
- `tests/api/advisory_summary.rs` — integration tests for the advisory-summary endpoint

## Implementation Notes
- Per CONVENTIONS.md §Testing: write integration tests in `tests/api/` that hit a real PostgreSQL test database. Use the `assert_eq!(resp.status(), StatusCode::OK)` assertion pattern established in existing test files.
  Applies: task creates `tests/api/advisory_summary.rs` matching the convention's `tests/api/` integration test scope.
- Per CONVENTIONS.md §Framework: use Axum test utilities for making HTTP requests to the endpoint.
  Applies: convention has no file-type restriction (broadly applicable).
- Follow the test setup pattern in `tests/api/sbom.rs` for database seeding and HTTP client configuration.
- Test data should include: an SBOM with multiple advisories at different severity levels (e.g., 2 critical, 3 high, 1 medium, 0 low), an SBOM with duplicate advisory links to verify deduplication, and a valid SBOM with no advisories.

## Reuse Candidates
- `tests/api/sbom.rs` — existing SBOM endpoint integration tests demonstrating test setup, database seeding, and assertion patterns
- `tests/api/advisory.rs` — existing advisory endpoint integration tests for reference on how to create advisory test fixtures and seed advisory data

## Acceptance Criteria
- [ ] Test validates that a valid SBOM with advisories returns correct severity counts
- [ ] Test validates that a nonexistent SBOM ID returns 404
- [ ] Test validates that duplicate advisory-SBOM links are deduplicated in counts
- [ ] Test validates that an SBOM with no advisories returns all zero counts
- [ ] Test validates the response JSON structure matches `{ critical, high, medium, low, total }`
- [ ] All tests pass against the PostgreSQL test database

## Test Requirements
- [ ] Happy path: SBOM with 2 critical, 3 high, 1 medium, 0 low advisories returns `{ critical: 2, high: 3, medium: 1, low: 0, total: 6 }`
- [ ] 404 case: nonexistent SBOM UUID returns 404 status code
- [ ] Deduplication: SBOM with the same advisory linked twice counts it only once
- [ ] Empty case: SBOM with no linked advisories returns `{ critical: 0, high: 0, medium: 0, low: 0, total: 0 }`
- [ ] Response content-type is `application/json`

## Verification Commands
- `cargo test --package tests -- advisory_summary` — run the new integration tests

## Dependencies
- Depends on: Task 1 — Add advisory severity aggregation endpoint (endpoint must exist to test it)
