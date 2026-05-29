# Task 6 -- Add integration tests for advisory-summary endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint to the existing test suite. These tests verify the end-to-end behavior of the advisory severity aggregation feature, including correct severity counting, deduplication, 404 handling, and cache behavior, running against a real PostgreSQL test database.

## Files to Create
- `tests/api/advisory_summary.rs` -- integration tests for the advisory-summary endpoint

## Files to Modify
- `tests/Cargo.toml` -- add any necessary test dependencies if not already present (likely none needed)

## Implementation Notes
- Follow the existing integration test pattern established in `tests/api/sbom.rs` and `tests/api/advisory.rs`. Tests hit a real PostgreSQL test database and use the `assert_eq!(resp.status(), StatusCode::OK)` pattern.
- **Test setup**: Each test should:
  1. Create test SBOM(s) via the ingestion pipeline or direct database insertion
  2. Create test advisories with known severity levels (Critical, High, Medium, Low)
  3. Link advisories to SBOMs via the `sbom_advisory` join table
  4. Call the endpoint and assert the response
- **Test scenarios to cover:**
  - SBOM with advisories across all four severity levels -- verify correct counts
  - SBOM with duplicate advisory links -- verify deduplication (same advisory linked multiple ways counts as one)
  - SBOM with zero advisories -- verify all counts are zero
  - Nonexistent SBOM ID -- verify 404 response
  - Response shape validation -- verify JSON keys match `critical`, `high`, `medium`, `low`, `total`
  - Cache header validation -- verify `Cache-Control` header with `max-age=300`
- Reference the advisory model in `modules/fundamental/src/advisory/model/summary.rs` for valid severity values to use in test data.

## Reuse Candidates
- `tests/api/sbom.rs` -- existing SBOM integration tests; reference for test setup, HTTP client usage, and assertion patterns
- `tests/api/advisory.rs` -- existing advisory integration tests; reference for creating test advisories
- `entity/src/sbom_advisory.rs` -- SBOM-Advisory join table entity; needed for test data linking

## Acceptance Criteria
- [ ] Integration tests cover all specified scenarios
- [ ] Tests pass against the PostgreSQL test database
- [ ] Test file follows existing test module conventions

## Test Requirements
- [ ] Test: SBOM with mixed severity advisories returns correct per-severity counts
- [ ] Test: duplicate advisory links are deduplicated in counts
- [ ] Test: SBOM with no advisories returns all-zero counts and total=0
- [ ] Test: nonexistent SBOM returns 404
- [ ] Test: response JSON shape matches specification
- [ ] Test: response includes cache headers

## Verification Commands
- `cargo test --package tests -- api::advisory_summary` -- all integration tests pass

## Dependencies
- Depends on: Task 3 -- Add GET /api/v2/sbom/{id}/advisory-summary endpoint
- Depends on: Task 4 -- Add cache invalidation for advisory summaries
