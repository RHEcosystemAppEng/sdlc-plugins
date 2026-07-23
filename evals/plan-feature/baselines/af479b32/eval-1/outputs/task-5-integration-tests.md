## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint covering all MVP and non-MVP requirements from TC-9001. Tests should cover: happy path with known severity counts, 404 for nonexistent SBOM, advisory deduplication, caching behavior, threshold filtering, and edge cases (SBOM with no advisories, SBOM with advisories of only one severity level).

## Files to Create
- `tests/api/advisory_summary.rs` — integration test module for the advisory-summary endpoint, following the established test patterns in `tests/api/`

## Files to Modify
- `tests/Cargo.toml` — add the new test module if Cargo requires explicit registration

## Implementation Notes
- Per Key Conventions §Testing: integration tests in `tests/api/` hit a real PostgreSQL test database. Follow the `assert_eq!(resp.status(), StatusCode::OK)` pattern established in existing test files.
  Applies: task creates `tests/api/advisory_summary.rs` matching the convention's Rust test file scope.
- Reference `tests/api/sbom.rs` and `tests/api/advisory.rs` for the test setup patterns: database initialization, test data insertion, HTTP client creation, and assertion style.
- Test data setup should create SBOMs with known advisory correlations at each severity level to verify correct counting.
- For deduplication testing, insert multiple `sbom_advisory` join records for the same advisory-SBOM pair and verify the count reflects the unique advisory count.
- For caching tests, issue two requests and verify the second returns within expected cache timing, or verify the `Cache-Control` header.

## Reuse Candidates
- `tests/api/sbom.rs` — existing SBOM endpoint integration tests; reference for test structure, database setup, and HTTP assertion patterns
- `tests/api/advisory.rs` — existing advisory endpoint integration tests; reference for advisory test data creation
- `entity/sbom_advisory.rs` — join table entity needed for setting up test data with advisory-SBOM correlations

## Acceptance Criteria
- [ ] All integration tests pass against a PostgreSQL test database
- [ ] Tests cover: happy path (200 with correct counts), 404 for nonexistent SBOM, advisory deduplication, SBOM with no advisories, threshold parameter variants, invalid threshold returns 400
- [ ] Tests follow established patterns from existing `tests/api/` files
- [ ] Test assertions verify both HTTP status codes and response body content

## Test Requirements
- [ ] Test: valid SBOM with advisories at all severity levels returns correct counts and total
- [ ] Test: nonexistent SBOM ID returns 404
- [ ] Test: SBOM with no linked advisories returns all-zero counts
- [ ] Test: duplicate advisory-SBOM join records do not inflate counts
- [ ] Test: `?threshold=critical` returns only critical count with correct total
- [ ] Test: `?threshold=high` returns critical and high counts
- [ ] Test: invalid threshold value returns 400 Bad Request
- [ ] Test: response includes `Cache-Control` header with `max-age=300`

## Dependencies
- Depends on: Task 1 — Add severity aggregation model and service method
- Depends on: Task 2 — Add advisory-summary endpoint with caching
- Depends on: Task 3 — Add cache invalidation for advisory summaries
- Depends on: Task 4 — Add threshold query parameter support
