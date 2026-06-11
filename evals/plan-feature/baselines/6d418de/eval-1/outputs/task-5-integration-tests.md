# Task 5 — Add integration tests for advisory summary endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint. The tests should cover the core scenarios: successful aggregation returning correct severity counts, 404 response for non-existent SBOM IDs, deduplication of advisories (same advisory linked multiple times should count once), and verification of the response JSON shape. These tests follow the existing integration test patterns in `tests/api/` using a real PostgreSQL test database.

## Files to Create
- `tests/api/advisory_summary.rs` — integration tests for the advisory summary endpoint

## Files to Modify
- `tests/Cargo.toml` — add any necessary test dependencies if not already present

## Implementation Notes
- Follow the existing integration test patterns in `tests/api/sbom.rs` and `tests/api/advisory.rs`. Key patterns:
  - Tests hit a real PostgreSQL test database
  - Use `assert_eq!(resp.status(), StatusCode::OK)` pattern for status code assertions
  - Set up test data by inserting SBOMs and advisories into the test database, then linking them via the `sbom_advisory` join table
- Test scenarios to implement:
  1. **Successful aggregation**: create an SBOM, link advisories at each severity level (e.g., 2 critical, 3 high, 1 medium, 0 low), call the endpoint, assert response matches `{ "critical": 2, "high": 3, "medium": 1, "low": 0, "total": 6 }`
  2. **Non-existent SBOM**: call the endpoint with an ID that does not exist, assert 404 response
  3. **Deduplication**: link the same advisory to an SBOM twice (via different paths), call the endpoint, assert the advisory is counted only once
  4. **Empty advisories**: create an SBOM with no linked advisories, assert response is `{ "critical": 0, "high": 0, "medium": 0, "low": 0, "total": 0 }`
  5. **Response shape**: verify all expected fields are present in the JSON response and are integer types
- Per docs/constraints.md Section 5 (Code Change Rules): changes must be scoped to the files listed; code must not be modified without first inspecting it; implementation must follow the patterns referenced in these notes.
- Per docs/constraints.md Section 2 (Commit Rules): every commit must reference TC-9001, follow Conventional Commits, and include the AI assistance trailer.

## Reuse Candidates
- `tests/api/sbom.rs` — SBOM endpoint integration tests demonstrating test setup, data insertion, and assertion patterns
- `tests/api/advisory.rs` — Advisory endpoint integration tests showing how advisory test data is created and linked
- `entity/src/sbom_advisory.rs` — SBOM-Advisory join table entity for creating test linkages

## Acceptance Criteria
- [ ] Integration test file exists at `tests/api/advisory_summary.rs`
- [ ] Test covers successful aggregation with correct severity counts
- [ ] Test covers 404 response for non-existent SBOM ID
- [ ] Test covers advisory deduplication
- [ ] Test covers SBOM with zero advisories
- [ ] All tests pass against the PostgreSQL test database

## Test Requirements
- [ ] All five test scenarios listed in Implementation Notes are implemented as separate test functions
- [ ] Each test function has a doc comment describing what it verifies
- [ ] Tests are independent and do not depend on execution order

## Verification Commands
- `cargo test --test api advisory_summary` — advisory summary integration tests pass
- `cargo test --test api` — all integration tests pass (no regressions)

## Dependencies
- Depends on: Task 3 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint with caching
