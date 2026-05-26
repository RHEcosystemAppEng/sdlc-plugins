# Task 5 -- Add integration tests for advisory-summary endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the `GET /api/v2/sbom/{id}/advisory-summary`
endpoint covering the full range of acceptance criteria: correct severity counts,
404 for missing SBOMs, deduplication of advisories, threshold filtering, and cache
behavior. These tests follow the existing integration test patterns in `tests/api/`
and run against a real PostgreSQL test database.

## Files to Modify
- `tests/Cargo.toml` -- add the advisory-summary test module if test modules are registered there

## Files to Create
- `tests/api/advisory_summary.rs` -- integration tests for the advisory-summary endpoint

## Implementation Notes
- Follow the test patterns established in `tests/api/sbom.rs` and `tests/api/advisory.rs`. These tests:
  1. Set up test data (SBOMs, advisories, advisory-SBOM links) using the existing test fixtures or helper functions
  2. Make HTTP requests to the endpoint
  3. Assert on response status codes using `assert_eq!(resp.status(), StatusCode::OK)` pattern
  4. Deserialize and validate response body JSON
- Test scenarios to cover:
  1. **Happy path**: SBOM with advisories at multiple severity levels returns correct counts
  2. **Empty SBOM**: SBOM with no linked advisories returns all zeros
  3. **Deduplication**: Same advisory linked to an SBOM multiple times is counted once
  4. **Not found**: Non-existent SBOM ID returns 404
  5. **Threshold -- critical**: `?threshold=critical` returns only critical count
  6. **Threshold -- high**: `?threshold=high` returns critical and high counts
  7. **Threshold -- invalid**: `?threshold=invalid` returns 400
  8. **Threshold -- absent**: No threshold parameter returns all counts (regression)
- Ensure test data setup creates advisories with known, deterministic severity levels so assertions can be exact (not approximate).
- Use the test database setup/teardown pattern from existing test files.

## Reuse Candidates
- `tests/api/sbom.rs` -- SBOM endpoint integration tests; follow the same test setup, request, and assertion patterns
- `tests/api/advisory.rs` -- advisory endpoint integration tests; reuse test data setup for advisories
- `common/src/model/paginated.rs::PaginatedResults` -- response wrapper used by list endpoints; not directly needed here but demonstrates the deserialization pattern used in tests

## Acceptance Criteria
- [ ] All test scenarios listed above pass against a PostgreSQL test database
- [ ] Tests verify exact severity counts, not just response status
- [ ] Tests cover both the base endpoint and the threshold query parameter
- [ ] Tests follow the established integration test patterns in `tests/api/`

## Test Requirements
- [ ] Integration test for happy path: SBOM with advisories at critical (2), high (3), medium (1), low (0) returns `{ "critical": 2, "high": 3, "medium": 1, "low": 0, "total": 6 }`
- [ ] Integration test for empty SBOM: returns `{ "critical": 0, "high": 0, "medium": 0, "low": 0, "total": 0 }`
- [ ] Integration test for deduplication: advisory linked twice returns count of 1
- [ ] Integration test for 404: non-existent SBOM ID returns 404
- [ ] Integration test for threshold=critical: returns only critical and total
- [ ] Integration test for threshold=high: returns critical, high, and total
- [ ] Integration test for invalid threshold: returns 400
- [ ] Integration test for absent threshold: returns all counts

## Verification Commands
- `cargo test --test api -- advisory_summary` -- run all advisory-summary integration tests

## Dependencies
- Depends on: Task 2 -- Add GET /api/v2/sbom/{id}/advisory-summary endpoint
- Depends on: Task 3 -- Add optional threshold query parameter to advisory-summary endpoint
