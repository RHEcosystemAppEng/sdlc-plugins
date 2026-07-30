## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory integration tests to reflect the new schema where advisory status is an enum column instead of a joined lookup table. All test setup, assertions, and query expectations must be updated to use the `status` enum column directly. Test fixtures that insert into the `advisory_status` table must be removed or replaced with direct enum value insertion.

## Files to Modify
- `tests/api/advisory.rs` — update test setup to insert advisories with enum status values instead of lookup table references; update assertions to check enum status in responses; add test coverage for status filtering with enum values

## Implementation Notes
- Remove any test fixture code that creates `advisory_status` rows or references the lookup table
- Update advisory insertion in test setup to use `AdvisoryStatusEnum` variants directly on the advisory model
- Verify that response JSON still contains status as a string (API shape unchanged)
- Add filter test cases for each enum value to ensure the endpoint correctly handles enum-based filtering

Per CONVENTIONS.md §Testing: integration tests in `tests/api/` must hit a real PostgreSQL test database and use the `assert_eq!(resp.status(), StatusCode::OK)` pattern.
Applies: task modifies `tests/api/advisory.rs` matching the convention's integration test scope.

## Reuse Candidates
- `tests/api/advisory.rs` — existing advisory test patterns to adapt
- `tests/api/sbom.rs` — reference for integration test setup patterns that do not use lookup table joins

## Acceptance Criteria
- [ ] All advisory integration tests pass with the new enum-based schema
- [ ] No test references to `advisory_status` table or `status_id` column
- [ ] Test coverage includes status filtering for all four enum values (New, Analyzing, Fixed, Rejected)
- [ ] Test setup uses direct enum value insertion, not lookup table insertion
- [ ] API response shape assertions confirm status is still returned as a string

## Test Requirements
- [ ] Verify existing advisory list test passes with enum-based status
- [ ] Verify existing advisory get test passes with enum-based status
- [ ] Add test for filtering advisories by status = "New"
- [ ] Add test for filtering advisories by status = "Fixed"
- [ ] Verify test database setup does not reference dropped `advisory_status` table

## Verification Commands
- `cargo test --test advisory` — run advisory integration tests
- `cargo test` — run all integration tests to verify no regressions

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 4 — Update advisory service and endpoints to use status enum
- Depends on: Task 5 — Update advisory ingestion pipeline to write enum values directly
