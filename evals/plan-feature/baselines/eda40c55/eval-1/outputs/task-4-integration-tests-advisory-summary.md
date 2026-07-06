## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the advisory-summary endpoint and its supporting service layer. These tests validate the full request-response cycle against a real PostgreSQL test database, covering the happy path, error cases, threshold filtering, caching behavior, and cache invalidation after advisory ingestion. This ensures the feature from TC-9001 works correctly end-to-end.

## Files to Create
- `tests/api/advisory_summary.rs` — integration test module for GET /api/v2/sbom/{id}/advisory-summary covering all acceptance criteria

## Files to Modify
- `tests/Cargo.toml` — add any necessary test dependencies if not already present (e.g., test helper utilities)

## Implementation Notes
- Follow the integration test pattern established in `tests/api/sbom.rs` and `tests/api/advisory.rs`: set up test data in the PostgreSQL test database, make HTTP requests, and assert on response status and body.
- Use the `assert_eq!(resp.status(), StatusCode::OK)` pattern for status code assertions, consistent with existing tests.
- Test data setup should create SBOMs with known advisory correlations at each severity level to verify correct counting.
- Include tests for deduplication: link the same advisory to an SBOM multiple times and verify it is counted only once.
- Test the threshold query parameter by verifying that filtered responses exclude severity levels below the threshold.
- Per CONVENTIONS.md §Testing: integration tests in `tests/api/` hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern. See `tests/api/sbom.rs` for the established test structure. Applies: task creates `tests/api/advisory_summary.rs` matching the convention's test file scope.

## Reuse Candidates
- `tests/api/sbom.rs` — existing SBOM integration tests showing test setup, HTTP client usage, and assertion patterns
- `tests/api/advisory.rs` — existing advisory integration tests showing how to create advisory test data and correlate with SBOMs

## Acceptance Criteria
- [ ] Integration test suite covers: happy path with correct severity counts, 404 for non-existent SBOM, threshold filter, advisory deduplication, and cache invalidation after ingestion
- [ ] All tests pass against the PostgreSQL test database
- [ ] Tests follow existing patterns in tests/api/ for consistency

## Test Requirements
- [ ] Test: GET /api/v2/sbom/{id}/advisory-summary returns 200 with correct severity counts for an SBOM with advisories at each severity level
- [ ] Test: GET returns 404 for a non-existent SBOM ID
- [ ] Test: GET with ?threshold=critical returns only critical count and total
- [ ] Test: GET with ?threshold=high returns critical and high counts and total
- [ ] Test: duplicate advisory links are counted only once
- [ ] Test: GET returns { critical: 0, high: 0, medium: 0, low: 0, total: 0 } for an SBOM with no advisories
- [ ] Test: after ingesting a new advisory, the endpoint returns updated counts

## Verification Commands
- `cargo test --test api advisory_summary` — all advisory-summary integration tests pass

## Dependencies
- Depends on: Task 1 — Add advisory severity summary model and service method
- Depends on: Task 2 — Add advisory-summary endpoint with caching
- Depends on: Task 3 — Add cache invalidation for advisory ingestion
