## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint. The tests exercise normal operation (valid SBOM with advisories at multiple severity levels), error handling (non-existent SBOM returns 404), the `?threshold` query parameter (severity filtering), advisory deduplication (same advisory linked multiple times counts once), and edge cases (SBOM with no advisories returns zero counts).

Tests follow the existing integration test pattern in `tests/api/` which hits a real PostgreSQL test database.

## Files to Create
- `tests/api/advisory_summary.rs` — integration tests for the advisory-summary endpoint covering all acceptance scenarios

## Files to Modify
- `tests/Cargo.toml` — register the new test file if test discovery requires explicit inclusion

## Implementation Notes
- Follow the integration test pattern in `tests/api/sbom.rs` for test setup, HTTP client configuration, database fixture creation, and assertion style.
- Use `assert_eq!(resp.status(), StatusCode::OK)` and `assert_eq!(resp.status(), StatusCode::NOT_FOUND)` patterns consistent with existing tests.
- Test fixtures should create SBOMs and advisories at known severity levels using the existing test helper infrastructure visible in `tests/api/advisory.rs`.
- Each test should set up its own data to avoid test interdependence:
  - Create an SBOM via the ingestion API or direct DB insert
  - Create advisories with known severities (Critical, High, Medium, Low)
  - Link advisories to the SBOM via the sbom_advisory table
  - Call `GET /api/v2/sbom/{id}/advisory-summary` and verify the response
- For the deduplication test: link the same advisory to the SBOM twice and verify it is counted once.
- For the threshold test: call with `?threshold=high` and verify that medium and low counts are zero/absent.
- Per CONVENTIONS.md §Testing: integration tests in `tests/api/` hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern. Applies: task creates `tests/api/advisory_summary.rs` matching the convention's test file scope.
- Per docs/constraints.md §5 (Code Change Rules): follow the patterns in existing test files; do not duplicate test helper infrastructure.

## Reuse Candidates
- `tests/api/sbom.rs` — SBOM endpoint integration test patterns for setup, HTTP assertions, and fixture creation
- `tests/api/advisory.rs` — advisory endpoint integration test patterns and test data creation helpers
- `tests/api/search.rs` — additional reference for integration test structure

## Acceptance Criteria
- [ ] Test exists: valid SBOM with advisories returns correct severity counts (critical, high, medium, low, total)
- [ ] Test exists: non-existent SBOM ID returns 404
- [ ] Test exists: SBOM with no advisories returns zero counts for all severity levels
- [ ] Test exists: duplicate advisories are counted only once
- [ ] Test exists: `?threshold=critical` returns only critical count (other levels zeroed or filtered)
- [ ] Test exists: response Content-Type is `application/json`
- [ ] All tests pass with `cargo test`

## Test Requirements
- [ ] All integration tests pass against a PostgreSQL test database
- [ ] Tests are independent and do not depend on execution order
- [ ] Test data fixtures are created within each test (no shared mutable state)
- [ ] Tests cover both success (200) and error (404) response codes

## Verification Commands
- `cargo test --test api advisory_summary` — all advisory-summary tests pass
- `cargo test --test api` — full integration test suite passes (no regressions)

## Dependencies
- Depends on: Task 2 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint with caching
