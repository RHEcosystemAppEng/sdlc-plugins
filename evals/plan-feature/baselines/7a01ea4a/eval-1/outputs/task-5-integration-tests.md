## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint covering the full range of scenarios: successful aggregation, non-existent SBOM handling, deduplication, caching behavior, and threshold filtering. These tests follow the existing integration test patterns in `tests/api/` and hit a real PostgreSQL test database.

## Files to Create
- `tests/api/sbom_advisory_summary.rs` — integration test module for the advisory summary endpoint with test functions covering all acceptance criteria

## Files to Modify
- `tests/api/sbom.rs` — add reference or import for the new test module if tests are organized as submodules (inspect existing test structure to determine if a separate file or additions to existing file are appropriate)

## Implementation Notes
- Follow the existing integration test pattern in `tests/api/sbom.rs` and `tests/api/advisory.rs`: use `assert_eq!(resp.status(), StatusCode::OK)` pattern and hit a real PostgreSQL test database.
- Set up test fixtures: create an SBOM, create advisories at different severity levels (critical, high, medium, low), and link them via the `sbom_advisory` join table.
- Test deduplication: link the same advisory to the same SBOM multiple times and verify it is counted once.
- Test 404: use a non-existent SBOM ID and verify the response status is 404.
- Test caching: verify response headers include cache control directives (this may require inspecting `tower-http` cache headers in the response).
- Test threshold filtering: test each threshold level and verify the correct subset of counts is returned.
- Per Key Conventions (Testing): integration tests in `tests/api/` hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern.
  Applies: task creates `tests/api/sbom_advisory_summary.rs` matching the convention's test file scope.

## Reuse Candidates
- `tests/api/sbom.rs` — existing SBOM endpoint integration tests demonstrating test setup, fixture creation, and assertion patterns
- `tests/api/advisory.rs` — existing advisory endpoint integration tests demonstrating advisory fixture creation
- `common/src/model/paginated.rs::PaginatedResults` — response wrapper used in existing tests for deserialization patterns

## Acceptance Criteria
- [ ] All integration tests pass against the PostgreSQL test database
- [ ] Tests cover: successful aggregation, 404 for non-existent SBOM, deduplication, caching headers, and threshold filtering
- [ ] Tests follow the existing patterns in `tests/api/`

## Test Requirements
- [ ] Test: valid SBOM with advisories at all severity levels returns correct counts
- [ ] Test: SBOM with no advisories returns all-zero counts
- [ ] Test: non-existent SBOM ID returns 404
- [ ] Test: duplicate advisory links are deduplicated (same advisory counted once)
- [ ] Test: response includes cache control headers
- [ ] Test: each threshold level filters counts correctly
- [ ] Test: invalid threshold returns 400
- [ ] Test: no threshold returns full counts

## Verification Commands
- `cargo test --test api sbom_advisory_summary` — all tests pass
- `cargo test --test api` — full API integration test suite passes (no regressions)

## Dependencies
- Depends on: Task 1 — Add advisory severity summary model and service method
- Depends on: Task 2 — Add advisory-summary REST endpoint with caching
- Depends on: Task 4 — Add optional threshold query parameter for severity filtering
