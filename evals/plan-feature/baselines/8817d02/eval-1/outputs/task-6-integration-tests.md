## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint. Tests should cover the happy path (correct severity counts), error cases (404 for missing SBOM), the threshold query parameter, deduplication of advisories, and edge cases (SBOM with no advisories). Tests run against a real PostgreSQL test database following the existing test patterns.

## Files to Create
- `tests/api/advisory_summary.rs` — integration tests for the advisory summary endpoint

## Files to Modify
- `tests/Cargo.toml` — add the new test file to the test configuration if required by the project's test setup

## Implementation Notes
- Follow the existing integration test patterns in `tests/api/sbom.rs` and `tests/api/advisory.rs`:
  - Use `assert_eq!(resp.status(), StatusCode::OK)` pattern for status code assertions.
  - Tests hit a real PostgreSQL test database (per Key Conventions).
  - Inspect `tests/api/sbom.rs` for test setup patterns (creating test SBOMs, inserting test data).
  - Inspect `tests/api/advisory.rs` for patterns around creating test advisories with known severity levels.
- Test scenarios to cover:
  1. **Happy path**: create an SBOM, link advisories with known severities (e.g., 2 critical, 1 high, 3 medium, 1 low), call the endpoint, verify exact counts and total.
  2. **404 for missing SBOM**: call the endpoint with a non-existent SBOM ID, verify 404 status.
  3. **Empty advisories**: create an SBOM with no linked advisories, verify all counts are zero and total is zero.
  4. **Deduplication**: link the same advisory to the SBOM twice, verify it is counted only once.
  5. **Threshold filter — critical**: call with `?threshold=critical`, verify only critical count and recalculated total are returned.
  6. **Threshold filter — high**: call with `?threshold=high`, verify critical and high counts are included.
- Per docs/constraints.md §5.2: inspect existing test files before writing new tests.
- Per docs/constraints.md §5.11: add a doc comment to every test function.

## Reuse Candidates
- `tests/api/sbom.rs` — reference for test setup (creating SBOMs, making HTTP requests, asserting responses)
- `tests/api/advisory.rs` — reference for creating test advisories with specific severity levels
- `common/src/model/paginated.rs::PaginatedResults` — if needed for understanding response wrapper patterns

## Acceptance Criteria
- [ ] Integration test file `tests/api/advisory_summary.rs` exists with comprehensive test coverage
- [ ] Tests cover: happy path, 404 error, empty advisories, deduplication, threshold=critical, threshold=high
- [ ] All tests pass against the PostgreSQL test database
- [ ] Test assertions verify both HTTP status codes and response body field values
- [ ] Every test function has a doc comment describing its purpose

## Test Requirements
- [ ] At least 6 integration tests covering the scenarios listed above
- [ ] Tests follow the existing test patterns in `tests/api/sbom.rs` and `tests/api/advisory.rs`
- [ ] Tests are independent and do not depend on shared mutable state between test cases

## Verification Commands
- `cargo test --test api` — all integration tests pass including the new advisory summary tests
- `cargo test advisory_summary` — run only the new test module

## Dependencies
- Depends on: Task 3 — Advisory summary endpoint
- Depends on: Task 4 — Advisory summary caching

[sdlc-workflow] Description digest: sha256-md:67f63fb3651d712e8dba94420614495e07c86286cb01273ef57241a05cd2dc35
