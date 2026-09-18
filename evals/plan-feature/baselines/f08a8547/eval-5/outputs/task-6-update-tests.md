## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update advisory integration tests to work with the new enum-based status column. Tests must no longer reference the `advisory_status` lookup table or use `status_id` foreign key values. Update test data setup to insert advisory rows with `AdvisoryStatusEnum` values directly, update assertions to verify status from the enum column, and update any status filtering tests to use enum string comparisons.

## Files to Modify
- `tests/api/advisory.rs` -- update test data setup to insert advisory rows with enum status values instead of inserting into `advisory_status` lookup table; update response assertions to verify status field sourced from enum column; update status filter test cases to use enum value strings

## Implementation Notes
- Replace any test setup code that follows the pattern: (1) insert into `advisory_status`, (2) get ID, (3) set `status_id` on advisory row -- with direct enum value insertion: set `status` to an `AdvisoryStatusEnum` variant on the advisory `ActiveModel`
- Update response assertions: the response JSON `status` field should contain the same string values as before ("New", "Analyzing", "Fixed", "Rejected") since the API response shape is unchanged -- verify these values are correctly populated from the enum column
- For status filtering tests, update the query parameter to filter by the enum string value (e.g., `?status=Fixed`) and verify the filtered results match
- Per CONVENTIONS.md §Testing: use the established integration test pattern with a real PostgreSQL test database and `assert_eq!(resp.status(), StatusCode::OK)` assertions.
  Applies: task modifies `tests/api/advisory.rs` matching the convention's Rust test file scope.
- Constraint §5.1: changes scoped to files listed in this task
- Constraint §5.11: add doc comments to any new test functions created
- Constraint §5.12: add given-when-then inline comments to non-trivial test functions with distinct setup, action, and assertion phases

## Reuse Candidates
- `tests/api/sbom.rs` -- reference for integration test patterns (test setup, HTTP request construction, response assertion style)
- `tests/api/advisory.rs` -- existing test file to modify in-place; contains current test patterns for advisory endpoints
- `tests/api/search.rs` -- additional reference for integration test conventions

## Acceptance Criteria
- [ ] All advisory integration tests pass with the new enum-based schema
- [ ] No test code references the `advisory_status` lookup table
- [ ] No test code references the `status_id` column
- [ ] Status filtering tests verify correct enum-based filtering behavior
- [ ] Test data setup uses `AdvisoryStatusEnum` values directly
- [ ] `cargo test --test advisory` passes

## Test Requirements
- [ ] Verify advisory list test returns correct status values from the enum column
- [ ] Verify advisory get test returns the correct status value from the enum column
- [ ] Verify status filter test correctly filters by enum values (e.g., filter by "Fixed" returns only fixed advisories)
- [ ] Verify all integration tests compile and pass against the migrated test database schema

## Verification Commands
- `cargo test --test advisory` -- all advisory integration tests pass
- `cargo test` -- full test suite passes with no regressions

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
- Depends on: Task 4 -- Update advisory service and endpoints to use enum column
- Depends on: Task 5 -- Update advisory ingestion pipeline to write enum values directly
