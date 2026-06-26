## Repository
trustify-backend

## Target Branch
main

## Description
Add integration tests for the advisory-summary endpoint covering the core scenarios: successful aggregation, SBOM not found, threshold filtering, cache behavior, and deduplication of advisories. These tests validate the full request-response cycle against a real PostgreSQL test database, consistent with the project's existing integration test patterns.

## Files to Modify
- `tests/api/sbom.rs` — Add integration tests for GET /api/v2/sbom/{id}/advisory-summary

## Implementation Notes
Add integration test functions to the existing `tests/api/sbom.rs` file, which already contains SBOM endpoint integration tests. Follow the established test patterns in this file:
- Tests hit a real PostgreSQL test database
- Use `assert_eq!(resp.status(), StatusCode::OK)` for success assertions
- Set up test data by inserting SBOM, advisory, and sbom_advisory records before each test

Test scenarios to cover:

1. **Happy path**: Create an SBOM, link advisories with mixed severities (2 critical, 1 high, 3 medium, 1 low), call the endpoint, assert response is `{ critical: 2, high: 1, medium: 3, low: 1, total: 7 }`.

2. **SBOM not found**: Call the endpoint with a non-existent SBOM ID, assert 404 response.

3. **No advisories**: Create an SBOM with zero linked advisories, assert response is `{ critical: 0, high: 0, medium: 0, low: 0, total: 0 }`.

4. **Threshold filter**: Create an SBOM with mixed-severity advisories, call with `?threshold=high`, assert critical and high counts are present, medium and low are zero.

5. **Deduplication**: Link the same advisory to an SBOM twice (if the join table allows it), verify it is only counted once.

Per CONVENTIONS.md §Error Handling: use Result<T, AppError> with .context() wrapping.
Applies: task modifies `tests/api/sbom.rs` matching the convention's `.rs` module scope.

## Reuse Candidates
- `tests/api/sbom.rs` — Existing SBOM integration tests; follow the same test setup, teardown, and assertion patterns
- `tests/api/advisory.rs` — Advisory integration tests; reference for advisory test data setup
- `entity/src/sbom_advisory.rs` — Use for creating test join table records

## Acceptance Criteria
- [ ] At least 5 integration test functions covering: happy path, not found, no advisories, threshold filter, deduplication
- [ ] Tests follow existing patterns in tests/api/sbom.rs
- [ ] All tests pass against a PostgreSQL test database
- [ ] Tests validate response status codes and JSON body content

## Test Requirements
- [ ] Happy path: correct severity counts for known test data
- [ ] 404 response for non-existent SBOM ID
- [ ] Zero counts for SBOM with no linked advisories
- [ ] Threshold filter correctly zeroes out lower severity counts
- [ ] Duplicate advisory links do not inflate counts

## Verification Commands
- `cargo test -p trustify-tests sbom` — all SBOM integration tests pass including new ones
- `cargo test -p trustify-tests advisory_summary` — new advisory summary tests pass specifically

## Dependencies
- Depends on: Task 3 — Advisory summary endpoint
- Depends on: Task 4 — Endpoint caching
- Depends on: Task 5 — Cache invalidation on ingestion

[sdlc-workflow] Description digest: sha256-md:a1c3e5f7b9d0624139e75a0b1d4f8a2c3e56b7d9f1a3545a7b9c1d3e5f6a8b0
