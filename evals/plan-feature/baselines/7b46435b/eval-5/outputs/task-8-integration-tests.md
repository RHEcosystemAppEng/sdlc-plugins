# Task 8 — Update advisory integration tests for new schema

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory integration tests to reflect the new database schema where advisory status is stored as a PostgreSQL enum column instead of a lookup table join. Update test fixtures, assertions, and setup code to create advisories with enum status values and verify the correct behavior of list filtering, detail retrieval, and ingestion with the new schema.

## Files to Modify
- `tests/api/advisory.rs` — update test setup to use enum status values instead of `advisory_status` table inserts; update assertions to verify status from enum column; add tests for enum-specific filtering behavior

## Implementation Notes
- Existing tests likely set up advisory records by first inserting into `advisory_status` and then referencing the `status_id` FK — replace with direct enum value assignment on the advisory entity's `ActiveModel`
- Follow the existing test pattern: `assert_eq!(resp.status(), StatusCode::OK)` for HTTP response status assertions per project convention
- Tests hit a real PostgreSQL test database — ensure the test database runs all migrations including the new enum migration from Task 2
- Add test coverage for:
  - Listing advisories filtered by each of the four status enum values (New, Analyzing, Fixed, Rejected)
  - Verifying that the response JSON contains the correct status string (not an integer ID or null)
  - Verifying advisory creation through the ingestion path with enum status values
  - Verifying that invalid status filter values return appropriate error responses
- Follow the test structure and helper patterns in `tests/api/sbom.rs` for reference

## Reuse Candidates
- `tests/api/sbom.rs` — reference test structure, assertion patterns, and test helper usage
- `tests/api/advisory.rs` — existing advisory test setup code to modify in place

## Acceptance Criteria
- [ ] All existing advisory integration tests pass with the new enum schema
- [ ] Tests verify status filtering works correctly with each of the four enum values
- [ ] Tests verify API responses contain correct status strings
- [ ] No test code references the `advisory_status` table or `status_id` column
- [ ] Test setup creates advisories with enum status values directly

## Test Requirements
- [ ] Run full integration test suite: `cargo test -p tests`
- [ ] Verify advisory list with status filter for each value (New, Analyzing, Fixed, Rejected) returns correct results
- [ ] Verify advisory detail response includes correct status string
- [ ] Verify advisory list without filter returns all statuses correctly

## Verification Commands
- `cargo test -p tests` — all integration tests pass
- `cargo test -p tests -- advisory` — advisory-specific tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 5 — Update advisory service to eliminate status table join
- Depends on: Task 6 — Update advisory endpoints for enum status filtering
- Depends on: Task 7 — Update advisory ingestion pipeline for direct enum writes
