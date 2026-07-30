## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint. These tests validate the end-to-end behavior including correct severity counting, deduplication, 404 handling, threshold filtering, and response shape. The tests follow the existing integration test patterns in `tests/api/`.

## Files to Create
- `tests/api/advisory_summary.rs` — integration tests for the advisory-summary endpoint covering all acceptance criteria

## Files to Modify
- `tests/Cargo.toml` — add the new test module if needed for test discovery

## Implementation Notes
- Follow the existing integration test pattern in `tests/api/sbom.rs` and `tests/api/advisory.rs` for test setup (PostgreSQL test database), HTTP client construction, and assertion style (`assert_eq!(resp.status(), StatusCode::OK)`).
- Test scenarios should cover:
  1. Valid SBOM with advisories at each severity level — verify counts are correct
  2. Valid SBOM with no advisories — verify all counts are 0
  3. Non-existent SBOM ID — verify 404 response
  4. Duplicate advisory links — verify deduplication (count is 1, not 2)
  5. Threshold parameter — verify filtering for each severity level (critical, high, medium, low)
  6. Response shape — verify JSON fields match `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`
- Per CONVENTIONS.md: integration tests hit a real PostgreSQL test database and use the `assert_eq!(resp.status(), StatusCode::OK)` assertion pattern.
  Applies: task creates `tests/api/advisory_summary.rs` matching the convention's `.rs` test file scope.

## Reuse Candidates
- `tests/api/sbom.rs` — SBOM endpoint integration tests showing test setup, fixture creation, and assertion patterns
- `tests/api/advisory.rs` — advisory endpoint integration tests showing how advisories are created in the test database

## Acceptance Criteria
- [ ] Integration tests pass for all scenarios: valid SBOM, empty advisories, non-existent SBOM, deduplication, threshold filtering
- [ ] Tests follow the existing test patterns in tests/api/
- [ ] Tests use a real PostgreSQL test database, not mocks

## Test Requirements
- [ ] Test: GET /api/v2/sbom/{id}/advisory-summary returns correct counts for each severity level
- [ ] Test: GET returns `{ "critical": 0, "high": 0, "medium": 0, "low": 0, "total": 0 }` for an SBOM with no advisories
- [ ] Test: GET returns 404 for a non-existent SBOM ID
- [ ] Test: duplicate advisory links are deduplicated in the count
- [ ] Test: threshold=critical returns only critical count and recalculated total
- [ ] Test: threshold=high returns critical and high counts
- [ ] Test: response content-type is application/json

## Verification Commands
- `cargo test --test api advisory_summary` — runs the advisory-summary integration tests

## Dependencies
- Depends on: Task 3 — Add advisory-summary REST endpoint with caching
