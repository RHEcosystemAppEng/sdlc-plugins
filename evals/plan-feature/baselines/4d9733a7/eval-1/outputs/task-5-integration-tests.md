## Repository
trustify-backend

## Target Branch
main

## Description
Add integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint covering all scenarios: valid SBOM with advisories, nonexistent SBOM (404), advisory deduplication, threshold filtering, and caching behavior. These tests follow the existing integration test pattern in `tests/api/` using a real PostgreSQL test database.

## Files to Create
- `tests/api/sbom_advisory_summary.rs` — integration test module for the advisory-summary endpoint

## Files to Modify
- `tests/Cargo.toml` — add any needed test dependencies if not already present

## Implementation Notes
- Follow the integration test pattern in `tests/api/sbom.rs` for test setup, database fixtures, and HTTP request/response assertion style.
- Use the `assert_eq!(resp.status(), StatusCode::OK)` pattern established in the codebase for status code assertions.
- Test fixtures should:
  - Create an SBOM via the ingestion pipeline or direct entity insertion
  - Create advisories at each severity level and link them to the SBOM via `sbom_advisory` records
  - Include duplicate advisory links to verify deduplication
- For the threshold parameter tests, verify the response shape changes correctly when `?threshold=critical`, `?threshold=high`, etc. are supplied.
- For the 404 test, use a nonexistent SBOM ID and verify the response status and error body.
- Per CONVENTIONS.md §Testing: use real PostgreSQL test database and the `assert_eq!(resp.status(), StatusCode::OK)` pattern.
  Applies: task creates `tests/api/sbom_advisory_summary.rs` matching the convention's integration test scope.

## Reuse Candidates
- `tests/api/sbom.rs` — existing SBOM integration tests; follow fixture setup and assertion patterns
- `tests/api/advisory.rs` — existing advisory integration tests; reference for creating advisory test data

## Acceptance Criteria
- [ ] Test suite passes for all advisory-summary endpoint scenarios
- [ ] Deduplication logic is verified with duplicate advisory links
- [ ] 404 behavior is verified for nonexistent SBOM IDs
- [ ] Threshold parameter filtering is verified for each severity level
- [ ] Tests are consistent with the existing test style in `tests/api/`

## Test Requirements
- [ ] Test: valid SBOM with mixed-severity advisories returns correct counts
- [ ] Test: SBOM with no advisories returns all-zero counts
- [ ] Test: nonexistent SBOM ID returns 404
- [ ] Test: duplicate advisory links do not inflate counts
- [ ] Test: threshold=critical returns only critical count
- [ ] Test: threshold=high returns critical and high counts
- [ ] Test: no threshold returns all severity counts
- [ ] Test: invalid threshold value returns 400

## Dependencies
- Depends on: Task 1 — Add AdvisorySeveritySummary model and service method
- Depends on: Task 2 — Add advisory-summary endpoint with caching
- Depends on: Task 3 — Add cache invalidation for advisory summaries
- Depends on: Task 4 — Add threshold query parameter support
