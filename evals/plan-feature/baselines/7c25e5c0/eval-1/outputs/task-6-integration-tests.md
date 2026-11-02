## Repository
trustify-backend

## Target Branch
main

## Description
Add integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint covering the full feature scope: successful aggregation, 404 for missing SBOM, deduplication of advisories, cache behavior, and threshold filtering. These tests validate the endpoint end-to-end against a real PostgreSQL test database.

## Files to Modify
- `tests/api/sbom.rs` — add integration test functions for the advisory summary endpoint

## Implementation Notes
- Follow the existing integration test patterns in `tests/api/sbom.rs` for SBOM-related endpoint tests and `tests/api/advisory.rs` for advisory-related test setup
- Use the existing test database setup and fixture patterns — tests hit a real PostgreSQL test database per the repo's testing convention
- Use `assert_eq!(resp.status(), StatusCode::OK)` pattern for status code assertions (per repo Key Conventions)
- Test data setup: create an SBOM, ingest advisories at different severity levels, link them via `sbom_advisory` records
- For deduplication test: link the same advisory to the SBOM multiple times and verify the count reflects unique advisories
- Reference `entity/src/sbom_advisory.rs` for the join table entity used in test setup
- Per CONVENTIONS.md §Testing: integration tests in `tests/api/` hit a real PostgreSQL test database.
  Applies: task modifies `tests/api/sbom.rs` matching the convention's integration test scope.

## Acceptance Criteria
- [ ] Test for successful aggregation with advisories at all severity levels
- [ ] Test for 404 response with non-existent SBOM ID
- [ ] Test for advisory deduplication (same advisory linked multiple times)
- [ ] Test for cache headers in response
- [ ] Test for threshold filtering with each valid threshold value
- [ ] Test for empty SBOM (no advisories) returns zero counts
- [ ] All tests pass against the real test database

## Test Requirements
- [ ] Integration test: `GET /api/v2/sbom/{id}/advisory-summary` with valid SBOM returns correct severity counts
- [ ] Integration test: `GET /api/v2/sbom/{id}/advisory-summary` with non-existent ID returns 404
- [ ] Integration test: duplicate advisory links produce correct (deduplicated) counts
- [ ] Integration test: response includes cache control headers
- [ ] Integration test: `?threshold=critical` filters correctly
- [ ] Integration test: SBOM with zero advisories returns `{ critical: 0, high: 0, medium: 0, low: 0, total: 0 }`

## Dependencies
- Depends on: Task 3 — Advisory summary endpoint with caching
- Depends on: Task 5 — Threshold query parameter filter
