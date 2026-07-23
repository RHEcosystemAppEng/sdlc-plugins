# Task 6: Update advisory integration tests for status enum

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory endpoint integration tests to work with the new status enum column. The tests in `tests/api/advisory.rs` hit a real PostgreSQL test database and exercise the advisory list and detail endpoints. After the schema migration, these tests must seed data using the new enum column (not the lookup table), verify status filtering works with enum values, and confirm the API response shape is unchanged.

## Files to Modify
- `tests/api/advisory.rs` -- update test data seeding to use the `status` enum column instead of inserting into the `advisory_status` lookup table; update status filter assertions to use enum values; verify response status strings match expected values

## Implementation Notes
- The existing tests likely seed test data by inserting rows into both `advisory` and `advisory_status` tables, then setting `advisory.status_id`. After this change, tests should insert advisory rows with the `status` enum column directly (e.g., `status = 'Fixed'`).
- Remove any test setup code that creates rows in the `advisory_status` table or references `status_id`.
- Per CONVENTIONS.md: integration tests use the `assert_eq!(resp.status(), StatusCode::OK)` pattern.
  Applies: task modifies `tests/api/advisory.rs` matching the convention's integration test scope.
- Per CONVENTIONS.md: integration tests in `tests/api/` hit a real PostgreSQL test database.
  Applies: task modifies `tests/api/advisory.rs` matching the convention's test database scope.
- Follow the existing test patterns in `tests/api/sbom.rs` for test data seeding, endpoint invocation, and response assertion structure.
- Ensure tests cover:
  - Listing advisories returns correct status strings
  - Filtering by each status value returns the correct subset
  - Advisory detail endpoint returns the correct status
  - Empty result sets when filtering by a status that no advisory has

## Reuse Candidates
- `tests/api/sbom.rs` -- existing integration test file demonstrating the project's test patterns: database seeding, HTTP client setup, response assertions, and `StatusCode` checks
- `tests/api/advisory.rs` -- current advisory tests showing the existing patterns that must be adapted

## Acceptance Criteria
- [ ] All advisory integration tests pass with the new schema
- [ ] Test data seeding uses the `status` enum column, not the `advisory_status` lookup table
- [ ] No test code references the `advisory_status` table or `status_id` column
- [ ] Status filtering tests verify each of the four enum values (New, Analyzing, Fixed, Rejected)
- [ ] API response assertions confirm the status field is still a string in the response

## Test Requirements
- [ ] Verify advisory list endpoint test passes with enum-based status values
- [ ] Verify advisory status filter test passes for each status value (New, Analyzing, Fixed, Rejected)
- [ ] Verify advisory detail endpoint test returns the correct status string
- [ ] Verify the full integration test suite passes: `cargo test --test advisory`

## Verification Commands
- `cargo test --test advisory` -- all advisory integration tests pass
- `cargo test --workspace` -- full test suite passes (no regressions in other modules)

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
- Depends on: Task 4 -- Update advisory service layer and endpoints to use status enum column
- Depends on: Task 5 -- Update advisory ingestion pipeline for direct enum writes
