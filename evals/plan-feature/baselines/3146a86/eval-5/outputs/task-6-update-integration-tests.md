# Task 6 — Update advisory integration tests for enum status column

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory integration tests to validate that advisory queries, filtering, and ingestion work correctly with the new `status` enum column. Remove any test setup or assertions that reference the `advisory_status` lookup table or `status_id` foreign key. Add test coverage for enum-specific behavior (valid enum values, filtering by enum).

## Files to Modify
- `tests/api/advisory.rs` — Update all advisory endpoint integration tests: remove test fixtures that seed the `advisory_status` table; update test data setup to use the enum column directly; update assertions to verify status as a string from the enum; add filter-by-status test cases using enum values

## Implementation Notes
- The existing tests likely set up test data by inserting into the `advisory_status` table and then referencing those IDs when creating advisory rows. Replace this with direct insertion of advisory rows with the `status` enum value.
- Follow the existing test pattern in `tests/api/advisory.rs` using `assert_eq!(resp.status(), StatusCode::OK)` and the established test database setup conventions.
- Reference `tests/api/sbom.rs` for the test structure pattern used by sibling integration tests.
- Ensure status filtering tests cover all four enum values: New, Analyzing, Fixed, Rejected.
- Verify the response JSON shape is unchanged — the `status` field should still appear as a plain string in the API response.
- Per constraints doc section 5 (Code Change Rules): inspect existing test files before modifying.
- Per constraints doc section 5.11: add doc comments to every new test function.
- Per constraints doc section 5.12: add given-when-then inline comments to non-trivial test functions.
- Per constraints doc section 2 (Commit Rules): commit message must reference TC-9005 and follow Conventional Commits format.

## Reuse Candidates
- `tests/api/sbom.rs` — Sibling integration test file demonstrating the project's test conventions, database setup patterns, and assertion styles
- `tests/api/advisory.rs` — Existing advisory tests to update (the current test patterns provide the baseline to follow)

## Acceptance Criteria
- [ ] No test references to `advisory_status` table or `status_id` column remain
- [ ] Advisory list endpoint test validates correct status values from the enum column
- [ ] Advisory list endpoint test validates status filtering works with enum values
- [ ] Advisory get endpoint test validates status is returned correctly
- [ ] All tests pass against a database with the new schema (post-migration)
- [ ] API response shape for status field is unchanged (string value, same field name)

## Test Requirements
- [ ] Test advisory list returns advisories with correct status strings (New, Analyzing, Fixed, Rejected)
- [ ] Test advisory list filtered by `status=Fixed` returns only advisories with Fixed status
- [ ] Test advisory list filtered by `status=New` returns only advisories with New status
- [ ] Test advisory get by ID returns the correct status value
- [ ] Test that the response JSON shape has not changed (backward compatibility)

## Verification Commands
- `cargo test -p trustify-tests -- advisory` — all advisory integration tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 4 — Update advisory service and endpoints to use status enum column
- Depends on: Task 5 — Update advisory ingestion pipeline to write enum values directly
