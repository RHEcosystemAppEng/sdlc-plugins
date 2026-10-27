## Repository
trustify-backend

## Target Branch
main

## Description
Write comprehensive integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint. Tests should cover the happy path (valid SBOM with advisories), 404 for nonexistent SBOM, empty advisories (SBOM exists but has no linked advisories), deduplication of advisories, and cache behavior.

## Files to Create
- `tests/api/advisory_summary.rs` — integration test module for the advisory summary endpoint

## Files to Modify
- `tests/Cargo.toml` — add any required test dependencies if not already present

## Implementation Notes
Follow the existing integration test pattern in `tests/api/sbom.rs` (SBOM endpoint tests) and `tests/api/advisory.rs` (advisory endpoint tests). These tests:

1. Hit a real PostgreSQL test database (not mocks)
2. Use `assert_eq!(resp.status(), StatusCode::OK)` pattern for status assertions
3. Set up test data (SBOMs, advisories) via the ingestion pipeline or direct database insertion
4. Make HTTP requests to the test server and assert on response bodies

Test scenarios:
- **Happy path**: Create an SBOM, link advisories at various severity levels, call the endpoint, verify counts match
- **404**: Request summary for a nonexistent SBOM ID, verify 404 response
- **Empty advisories**: Create an SBOM with no linked advisories, verify all counts are 0
- **Deduplication**: Link the same advisory to an SBOM multiple times, verify it's counted once
- **Cache headers**: Verify the response includes cache control headers with 5-minute TTL

Per CONVENTIONS.md §Testing: integration tests in `tests/api/` hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern.
Applies: task creates `tests/api/advisory_summary.rs` matching the convention's Rust test file scope.

## Reuse Candidates
- `tests/api/sbom.rs` — SBOM endpoint integration tests, demonstrates test setup and assertion patterns
- `tests/api/advisory.rs` — advisory endpoint integration tests, demonstrates advisory data setup

## Acceptance Criteria
- [ ] Integration test for valid SBOM with advisories at multiple severity levels passes
- [ ] Integration test for nonexistent SBOM ID returning 404 passes
- [ ] Integration test for SBOM with no advisories returning zero counts passes
- [ ] Integration test for advisory deduplication passes
- [ ] Integration test for cache control headers passes
- [ ] All existing tests continue to pass

## Test Requirements
- [ ] Verify all test scenarios listed in test plan pass against a real PostgreSQL database
- [ ] Verify no regressions in existing integration tests

## Verification Commands
- `cargo test --test api` — run all integration tests including the new advisory summary tests

## Dependencies
- Depends on: Task 3 — Advisory summary endpoint
- Depends on: Task 4 — Cache invalidation
