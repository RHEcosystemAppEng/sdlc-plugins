## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint covering the full request-response lifecycle against a real PostgreSQL test database. These tests validate the end-to-end behavior including severity aggregation, deduplication, threshold filtering, 404 handling, and cache headers.

## Files to Modify
- `tests/api/advisory.rs` — add integration test functions for the advisory summary endpoint (extending the existing advisory test file)

## Implementation Notes
- Follow the integration test pattern established in `tests/api/sbom.rs` (SBOM endpoint tests) and `tests/api/advisory.rs` (advisory endpoint tests). Both hit a real PostgreSQL test database and use the `assert_eq!(resp.status(), StatusCode::OK)` assertion pattern.
- Set up test data by inserting an SBOM, creating advisories with known severity levels, and linking them via the `sbom_advisory` join table. This ensures deterministic count expectations.
- Test the deduplication requirement: insert the same advisory linked to the same SBOM multiple times and verify the count is not inflated.
- Test the threshold filter: call with `?threshold=critical` and verify that only critical counts are non-zero, with medium and low zeroed out and total recalculated.
- Test 404: call with a non-existent SBOM UUID and verify a 404 response.
- Test cache headers: verify the response includes appropriate Cache-Control headers for 5-minute caching.
- Per docs/constraints.md §5.9-5.10: prefer parameterized tests if sibling test files use them; otherwise follow the existing pattern in `tests/api/advisory.rs`.
- Per docs/constraints.md §5.11-5.13: add doc comments to every test function; add given-when-then inline comments to non-trivial test functions.

## Reuse Candidates
- `tests/api/sbom.rs` — SBOM endpoint integration tests; follow its test setup, database seeding, and assertion patterns.
- `tests/api/advisory.rs` — advisory endpoint integration tests; extend this file with the new tests, following its existing test structure and helper functions.
- `tests/api/search.rs` — search endpoint tests; provides an additional reference for the integration test pattern used across the project.

## Acceptance Criteria
- [ ] Integration tests exist for: successful severity aggregation, 404 for missing SBOM, threshold filtering, deduplication, and cache headers
- [ ] All tests pass against the PostgreSQL test database
- [ ] Tests follow the project's established integration test patterns (setup, request, assertion)
- [ ] Every test function has a doc comment
- [ ] Non-trivial test functions include given-when-then inline comments

## Test Requirements
- [ ] Test: GET with valid SBOM having advisories at all severity levels returns correct counts
- [ ] Test: GET with valid SBOM having zero advisories returns `{ critical: 0, high: 0, medium: 0, low: 0, total: 0 }`
- [ ] Test: GET with non-existent SBOM ID returns 404
- [ ] Test: GET with `?threshold=critical` zeroes out high, medium, low and recalculates total
- [ ] Test: GET with `?threshold=high` zeroes out medium and low but keeps critical and high
- [ ] Test: SBOM with duplicate advisory links returns deduplicated counts
- [ ] Test: response includes Cache-Control header with 5-minute max-age

## Verification Commands
- `cargo test --test api advisory_summary` — all new tests pass
- `cargo test --test api` — all existing integration tests still pass (no regressions)

## Dependencies
- Depends on: Task 3 — Add advisory-summary endpoint with caching

[sdlc-workflow] Description digest: sha256:77017522f0d59b97bcc01860a6dc9b27b18f769e0eb626c739588611e8bc97e1
