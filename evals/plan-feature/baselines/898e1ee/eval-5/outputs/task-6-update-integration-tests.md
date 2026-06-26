## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update advisory integration tests to reflect the schema change from lookup-table-based status to enum-column-based status. Tests that set up advisory fixtures must create advisories with the `status` enum field instead of inserting into the `advisory_status` table and referencing by `status_id`. Tests that assert on response shape should continue to verify that status is returned as a string. Add a test that verifies the advisory list endpoint filters correctly by the new enum status column.

## Files to Modify
- `tests/api/advisory.rs` -- update advisory fixture setup to use enum status values instead of lookup table inserts; update any assertions that reference `status_id`; add a test for status enum filtering

## Implementation Notes
- In `tests/api/advisory.rs`, find any test setup code that inserts rows into the `advisory_status` table or sets `status_id` on advisory rows. Replace with setting `status: AdvisoryStatusEnum::New` (or other variants) directly on the advisory ActiveModel.
- The test pattern uses a real PostgreSQL test database (per Key Conventions) and asserts `assert_eq!(resp.status(), StatusCode::OK)`.
- Verify that the response body still contains `"status": "New"` (or similar) as a string -- the API contract is unchanged.
- Add a test that filters advisories by status (e.g., `GET /api/v2/advisory?status=Fixed`) and verifies only matching advisories are returned.
- Import `AdvisoryStatusEnum` from `entity::advisory`.
- Remove any `use entity::advisory_status` imports.
- Per CONVENTIONS.md §Testing Conventions (inferred from Key Conventions): use `assert_eq!(resp.status(), StatusCode::OK)` pattern and real PostgreSQL test database. Applies: task modifies `tests/api/advisory.rs` matching the convention's `.rs` test file scope.

## Acceptance Criteria
- [ ] All existing advisory integration tests pass with the updated fixture setup
- [ ] No test references `advisory_status` entity or lookup table
- [ ] A test exists that verifies advisory list filtering by enum status
- [ ] Response shape assertions confirm status is returned as a string

## Test Requirements
- [ ] `cargo test -p trustify-tests` passes all advisory tests
- [ ] Status filter test verifies correct filtering by at least two different status values
- [ ] Tests verify the API response shape is unchanged (status as string, not as object)

## Verification Commands
- `cargo test -p trustify-tests -- advisory` -- all advisory tests pass

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main

[sdlc-workflow] Description digest: sha256-md:fd6bba6589b59384bba27c135c91a352beae16ec256d12edc169cee6df66be45
