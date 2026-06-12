# Task 5 — Add integration tests for the advisory-summary endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Create comprehensive integration tests for the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint. Tests must cover the core aggregation behavior, deduplication, 404 handling, threshold filtering, empty advisory sets, and cache header verification. These tests hit a real PostgreSQL test database following the established integration test patterns in the repository.

## Files to Create
- `tests/api/advisory_summary.rs` — integration test suite for the advisory-summary endpoint

## Files to Modify
- `tests/Cargo.toml` — add any necessary test dependencies if not already present (likely not needed if existing test infrastructure covers this)

## Implementation Notes
- Follow the integration test pattern established in `tests/api/sbom.rs` and `tests/api/advisory.rs`. These tests:
  - Hit a real PostgreSQL test database
  - Use `assert_eq!(resp.status(), StatusCode::OK)` pattern for status code verification
  - Set up test data (SBOMs, advisories) before making assertions
  - Use the Axum test client to send HTTP requests
- **Test data setup**: Create test fixtures that include:
  - An SBOM with advisories at each severity level (Critical, High, Medium, Low)
  - Duplicate advisory-SBOM links to verify deduplication
  - An SBOM with zero advisories
  - A non-existent SBOM ID
- **Test cases to implement**:
  1. Successful aggregation: SBOM with mixed severity advisories returns correct counts and total
  2. Deduplication: same advisory linked multiple times to an SBOM is counted only once
  3. Non-existent SBOM: returns 404 status
  4. Threshold filtering with `?threshold=critical`: returns only critical count
  5. Threshold filtering with `?threshold=high`: returns critical and high counts
  6. Empty advisories: SBOM with no advisories returns all zeros
  7. Invalid threshold: returns 400 status
  8. Cache headers: response includes `Cache-Control: max-age=300`
- Per constraints (docs/constraints.md):
  - §5.11: Add a doc comment to every test function
  - §5.12: Add given-when-then inline comments to non-trivial test functions
  - §5.13: Skip given-when-then comments for trivial single-assertion tests

## Reuse Candidates
- `tests/api/sbom.rs` — established pattern for SBOM endpoint integration tests; follow its test setup, fixtures, and assertion patterns
- `tests/api/advisory.rs` — established pattern for advisory endpoint integration tests; reuse advisory creation test helpers
- `tests/api/search.rs` — additional reference for endpoint integration test structure

## Acceptance Criteria
- [ ] All test cases pass against a PostgreSQL test database
- [ ] Tests verify correct JSON response shape with expected field names
- [ ] Tests verify deduplication of advisory counts
- [ ] Tests verify 404 for non-existent SBOM
- [ ] Tests verify threshold query parameter filtering
- [ ] Tests verify cache control headers
- [ ] Every test function has a doc comment

## Test Requirements
- [ ] Test: aggregation returns correct counts for each severity level
- [ ] Test: total field equals sum of all severity counts
- [ ] Test: duplicate advisory links do not inflate counts
- [ ] Test: non-existent SBOM ID returns 404
- [ ] Test: `?threshold=critical` returns only critical count (others zero)
- [ ] Test: `?threshold=high` returns critical and high counts (medium and low zero)
- [ ] Test: SBOM with no linked advisories returns `{ critical: 0, high: 0, medium: 0, low: 0, total: 0 }`
- [ ] Test: invalid threshold value returns 400
- [ ] Test: response contains `Cache-Control: max-age=300` header

## Verification Commands
- `cargo test --package tests -- api::advisory_summary` — run the advisory-summary integration test suite
- `cargo test --package tests` — verify no existing tests are broken

## Dependencies
- Depends on: Task 3 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint
