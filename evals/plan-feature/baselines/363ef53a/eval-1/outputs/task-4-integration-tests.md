## Repository
trustify-backend

## Target Branch
main

## Description
Add integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint (TC-9001). Tests verify the complete request-response cycle against a real PostgreSQL test database, covering the happy path with correct severity counts, 404 for non-existent SBOMs, threshold query parameter filtering, and deduplication of advisory counts.

## Files to Create
- `tests/api/advisory_summary.rs` — integration tests for the advisory-summary endpoint covering all acceptance criteria

## Implementation Notes
- Follow the test patterns established in `tests/api/advisory.rs` and `tests/api/sbom.rs`: set up test data in the PostgreSQL test database, make HTTP requests to the endpoint, and assert on response status and body.
- Use the `assert_eq!(resp.status(), StatusCode::OK)` pattern for status code assertions, as established in the test conventions.
- Test data setup should use the existing ingestion service to create SBOMs and link advisories at various severity levels (critical, high, medium, low).
- Per CONVENTIONS.md §Testing: place tests in `tests/api/` and use the `assert_eq!(resp.status(), StatusCode::OK)` assertion pattern. See `tests/api/sbom.rs` and `tests/api/advisory.rs` for established test setup and assertion patterns. Applies: task creates `tests/api/advisory_summary.rs` matching the convention's `tests/api/` directory scope.

## Reuse Candidates
- `tests/api/sbom.rs` — existing SBOM endpoint tests; follow the same test setup, HTTP client usage, and assertion patterns
- `tests/api/advisory.rs` — existing advisory endpoint tests; follow the same pattern for advisory-related test data setup

## Acceptance Criteria
- [ ] Test: valid SBOM with advisories at all severity levels returns correct counts
- [ ] Test: SBOM with no advisories returns all-zero counts
- [ ] Test: non-existent SBOM ID returns 404
- [ ] Test: threshold query parameter filters severity counts correctly
- [ ] Test: duplicate advisory links are deduplicated in the count
- [ ] All existing tests continue to pass

## Test Requirements
- [ ] Happy path: create SBOM with advisories at critical (2), high (3), medium (1), low (0) severity; verify response `{ critical: 2, high: 3, medium: 1, low: 0, total: 6 }`
- [ ] Empty case: create SBOM with no linked advisories; verify response `{ critical: 0, high: 0, medium: 0, low: 0, total: 0 }`
- [ ] Not found: request advisory-summary for a UUID that does not correspond to any SBOM; verify 404 response
- [ ] Threshold filter: request with `?threshold=high`; verify only critical and high counts are returned
- [ ] Deduplication: link the same advisory to an SBOM twice; verify it is counted only once

## Verification Commands
- `cargo test --test advisory_summary` — all new tests pass
- `cargo test` — all tests pass (no regressions)

## Dependencies
- Depends on: Task 2 — Add advisory-summary endpoint with caching
