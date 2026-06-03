# Task 5 — Add integration tests for advisory summary endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint in the existing test suite. The tests should cover the core scenarios: successful aggregation with correct counts, 404 for non-existent SBOMs, deduplication of advisories, zero-count responses for SBOMs with no advisories, and correct severity level mapping. These tests follow the existing integration test patterns in `tests/api/`.

## Files to Modify
- `tests/api/sbom.rs` — add integration tests for the advisory summary endpoint (or create a new test module if the file is too large)

## Implementation Notes
- Follow the existing integration test patterns in `tests/api/sbom.rs` and `tests/api/advisory.rs`. Key patterns to follow:
  - Tests hit a real PostgreSQL test database
  - Use `assert_eq!(resp.status(), StatusCode::OK)` pattern for status code assertions
  - Set up test data (SBOMs, advisories, SBOM-advisory links) in the database before making HTTP requests
  - Parse response bodies as JSON and assert field values
- Test data setup should:
  - Create a test SBOM
  - Create advisories at each severity level (Critical, High, Medium, Low)
  - Link advisories to the SBOM via the `sbom_advisory` join table
  - For deduplication testing: link the same advisory to the SBOM multiple times (if the schema allows) or verify that the query handles duplicate links correctly
- Test cases to implement:
  1. **Happy path**: SBOM with advisories at each severity level returns correct counts
  2. **Empty result**: SBOM with no linked advisories returns all zeros
  3. **404**: Non-existent SBOM ID returns 404 status
  4. **Deduplication**: Same advisory linked multiple times is counted only once
  5. **Single severity**: SBOM with advisories only at one severity level returns counts for that level and zeros for others
- Per docs/constraints.md Section 2 (Commit Rules): every commit must reference TC-9001, follow Conventional Commits, and include the AI assistance trailer.
- Per docs/constraints.md Section 5.11: add a doc comment to every test function.
- Per docs/constraints.md Section 5.12: add given-when-then inline comments to non-trivial test functions.

## Reuse Candidates
- `tests/api/sbom.rs` — existing SBOM endpoint integration tests demonstrating test setup, HTTP client usage, and assertion patterns
- `tests/api/advisory.rs` — existing advisory endpoint tests showing how advisory test data is created and queried
- `entity/src/sbom_advisory.rs` — the join table entity for setting up test data linking SBOMs to advisories

## Acceptance Criteria
- [ ] At least 5 integration tests covering the scenarios listed above
- [ ] All tests pass against the test PostgreSQL database
- [ ] Tests follow the existing test patterns in `tests/api/`
- [ ] Each test function has a doc comment describing what it tests
- [ ] Non-trivial tests have given-when-then inline comments

## Test Requirements
- [ ] Integration test: happy path with advisories at all severity levels returns correct counts
- [ ] Integration test: SBOM with no advisories returns `{ critical: 0, high: 0, medium: 0, low: 0, total: 0 }`
- [ ] Integration test: non-existent SBOM returns 404
- [ ] Integration test: duplicate advisory links are deduplicated in the count
- [ ] Integration test: SBOM with advisories at a single severity level returns correct count for that level and zeros for others

## Verification Commands
- `cargo test --test api` — all integration tests pass including the new ones

## Dependencies
- Depends on: Task 3 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint with caching
