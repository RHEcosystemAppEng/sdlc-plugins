## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add comprehensive integration tests for the SBOM comparison endpoint. These tests hit a real PostgreSQL test database to verify the full request/response cycle, including edge cases like large SBOMs and identical SBOMs.

## Files to Modify
- `tests/api/sbom.rs` — add comparison endpoint integration tests

## Implementation Notes
Add test functions to `tests/api/sbom.rs` following the existing test pattern which uses `assert_eq!(resp.status(), StatusCode::OK)`.

Test scenarios:
1. Set up two SBOMs with known package differences (use the test database infrastructure already in place)
2. Call GET /api/v2/sbom/compare?left={id1}&right={id2}
3. Assert response status and body structure

Follow the existing test patterns in `tests/api/sbom.rs` for setting up test data and making requests. Use the same test harness and database setup as existing SBOM tests.

Reference `tests/api/advisory.rs` for advisory-related test data setup patterns, since the comparison includes vulnerability diff.

Ensure tests cover the performance requirement: for SBOMs with up to 2000 packages, the endpoint should respond within a reasonable time (the p95 < 1s requirement is validated in production monitoring, but tests should not timeout).

## Reuse Candidates
- `tests/api/sbom.rs` — existing SBOM test patterns for request/response assertions
- `tests/api/advisory.rs` — advisory test data setup for vulnerability diff testing

## Acceptance Criteria
- [ ] Integration tests cover: valid comparison, missing params, non-existent IDs, identical SBOMs, SBOMs with no overlap
- [ ] Tests follow existing patterns in tests/api/sbom.rs
- [ ] All tests pass against the PostgreSQL test database

## Test Requirements
- [ ] Test: compare two SBOMs with added packages returns correct added_packages array
- [ ] Test: compare two SBOMs with removed packages returns correct removed_packages array
- [ ] Test: compare two SBOMs with version changes returns correct version_changes array
- [ ] Test: compare identical SBOMs returns empty arrays in all categories
- [ ] Test: compare with non-existent SBOM ID returns 404

## Verification Commands
- `cargo test --test api sbom` — expected: all SBOM tests pass including new comparison tests

## Dependencies
- Depends on: Task 4 — Backend comparison endpoint
