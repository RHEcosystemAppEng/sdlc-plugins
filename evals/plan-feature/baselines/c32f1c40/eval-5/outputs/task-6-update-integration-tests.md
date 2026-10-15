## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory integration tests to work with the new `status` enum column schema. Tests must verify that advisory list and get endpoints return correct status values from the enum column, that status filtering works without the lookup table join, and that the ingestion pipeline correctly writes enum values. Test data setup must create advisories with enum status values instead of inserting into the lookup table.

## Files to Modify
- `tests/api/advisory.rs` -- update test data setup to use `advisory_status_enum` values instead of inserting into the `advisory_status` lookup table; update assertions to verify status is returned correctly from the enum column; add tests for status filtering via the enum column; remove any test utilities that reference the `advisory_status` table

## Implementation Notes
- Per CONVENTIONS.md §Testing: integration tests hit a real PostgreSQL test database. Use the established `assert_eq!(resp.status(), StatusCode::OK)` pattern for response status assertions.
  Applies: task modifies `tests/api/advisory.rs` matching the convention's `tests/api/` scope.
- Update test data factories or setup functions to insert advisory rows with `status` enum values directly, rather than creating `advisory_status` lookup rows and referencing them via FK
- Ensure status filtering tests verify that `GET /api/v2/advisory?status=Fixed` returns only advisories with the matching enum value
- Verify the response JSON shape is identical to the pre-migration shape (status is still a string field)
- Reference existing test patterns in `tests/api/sbom.rs` for the established integration test structure

## Reuse Candidates
- `tests/api/sbom.rs` -- SBOM endpoint integration tests as a reference for the test structure, setup patterns, and assertion style
- `tests/api/search.rs` -- search integration tests for cross-entity search testing patterns

## Acceptance Criteria
- [ ] All advisory integration tests pass against a database with the new enum schema
- [ ] Tests verify advisory list endpoint returns correct status values
- [ ] Tests verify advisory get endpoint returns correct status values
- [ ] Tests verify status filtering works with enum values
- [ ] No test code references the `advisory_status` lookup table
- [ ] `cargo test -p tests` passes without failures

## Test Requirements
- [ ] Test advisory list with no status filter returns all statuses correctly
- [ ] Test advisory list with status filter `?status=Fixed` returns only Fixed advisories
- [ ] Test advisory list with status filter `?status=New` returns only New advisories
- [ ] Test advisory get by ID returns the correct status enum value as a string
- [ ] Test ingestion followed by retrieval returns the correct status

## Verification Commands
- `cargo test -p tests -- advisory` -- all advisory integration tests pass

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
- Depends on: Task 4 -- Update advisory service and endpoints to use status enum
- Depends on: Task 5 -- Update advisory ingestion pipeline for status enum
