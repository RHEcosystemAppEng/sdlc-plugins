## Repository
trustify-backend

## Target Branch
main

## Description
Add integration tests for the advisory severity summary endpoint. Tests verify correct severity counts, 404 for missing SBOMs, advisory deduplication, threshold query parameter filtering, and cache-control headers. These tests run against a real PostgreSQL test database following the project's existing integration test conventions.

## Files to Create
- `tests/api/sbom_advisory_summary.rs` — Integration tests for `GET /api/v2/sbom/{id}/advisory-summary`

## Implementation Notes
- Follow the integration test patterns in `tests/api/sbom.rs` and `tests/api/advisory.rs`: set up a test database, create test fixtures (SBOMs and advisories with known severities), make HTTP requests to the endpoint, and assert on response status codes and JSON body content.
- Use the `assert_eq!(resp.status(), StatusCode::OK)` pattern documented in the Key Conventions.
- Test cases to implement:
  1. **Happy path**: Create an SBOM, link advisories with varying severities (e.g., 2 critical, 3 high, 1 medium, 0 low), call the endpoint, assert counts match.
  2. **SBOM not found**: Call with a non-existent UUID, assert `StatusCode::NOT_FOUND` (404).
  3. **Deduplication**: Link the same advisory to an SBOM multiple times (if possible via test setup), assert it is counted only once.
  4. **Threshold filtering — critical**: Add `?threshold=critical` query param, assert only `critical` count is non-zero, `high`, `medium`, `low` are 0.
  5. **Threshold filtering — high**: Add `?threshold=high`, assert `critical` and `high` are non-zero, `medium` and `low` are 0.
  6. **Empty SBOM**: Create an SBOM with no linked advisories, assert all counts are 0 and total is 0.
  7. **Cache headers**: Assert the response includes `cache-control` header with `max-age=300`.
- Reference `tests/Cargo.toml` for test dependencies and ensure the new test file is included.

## Reuse Candidates
- `tests/api/sbom.rs` — Existing SBOM endpoint tests; follow for test setup, fixture creation, and assertion patterns
- `tests/api/advisory.rs` — Existing advisory endpoint tests; reference for creating advisory test fixtures with specific severities
- `tests/Cargo.toml` — Test dependencies and configuration

## Acceptance Criteria
- [ ] At least 6 test cases covering: happy path, 404, deduplication, threshold filtering (2 levels), empty SBOM, cache headers
- [ ] All tests follow existing integration test conventions (real database, HTTP assertions)
- [ ] Tests compile and pass against a properly configured test database
- [ ] Test file is properly included in the test suite

## Test Requirements
- [ ] Happy path test: correct severity counts for an SBOM with known advisories
- [ ] 404 test: non-existent SBOM returns NOT_FOUND
- [ ] Deduplication test: same advisory linked multiple times is counted once
- [ ] Threshold filter test (critical): only critical count returned
- [ ] Threshold filter test (high): critical and high counts returned
- [ ] Empty SBOM test: all counts are 0
- [ ] Cache header test: response includes cache-control max-age=300

## Dependencies
- Depends on: Task 3 — Advisory summary endpoint (endpoint must exist to test it)
- Depends on: Task 4 — Mount route in server (route must be reachable for integration tests)

## Digest
[sdlc-workflow] Description digest: sha256-md:ae8bfc653d7c1943c720ec32c0941eb64ddf86f176a7e53d7f96392b5b696d55
