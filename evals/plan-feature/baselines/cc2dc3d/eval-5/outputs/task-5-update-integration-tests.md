# Task 5 — Update advisory integration tests for enum status schema

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory integration tests to work with the new `advisory_status_enum` column instead of the `advisory_status` lookup table. Test fixtures that seed advisory data must be updated to use the enum values directly. Existing test assertions for status filtering and advisory detail responses must be verified against the new schema.

## Files to Modify
- `tests/api/advisory.rs` — Update advisory endpoint integration tests: remove any test setup that inserts rows into `advisory_status` table; update advisory seeding to set `status` enum column directly; verify status filter tests use enum comparison; verify response assertions still pass with the unchanged response shape

## Implementation Notes
- In `tests/api/advisory.rs`, update test fixture setup that previously inserted rows into `advisory_status` and referenced them via FK. Replace with direct enum value assignment on advisory records (e.g., `status: Set(AdvisoryStatusEnum::New)`).
- Follow the existing test pattern: integration tests hit a real PostgreSQL test database and use `assert_eq!(resp.status(), StatusCode::OK)` for response validation per the project's testing conventions.
- Ensure test coverage for all four enum values: `New`, `Analyzing`, `Fixed`, `Rejected`.
- Add a test case for filtering by enum status to verify the eliminated join does not change query behavior.
- Reference the test patterns in `tests/api/sbom.rs` for the established integration test structure in this project.

## Reuse Candidates
- `tests/api/sbom.rs` — Example integration test file showing the established test pattern (database setup, HTTP request, response assertion) that advisory tests should follow
- `tests/api/search.rs` — Another integration test example for reference

## Acceptance Criteria
- [ ] All advisory integration tests pass against the new schema
- [ ] Test setup no longer references the `advisory_status` table
- [ ] Tests cover filtering by each of the four status enum values
- [ ] Response shape assertions confirm backward compatibility (status returned as string)
- [ ] No references to `advisory_status` table or `status_id` column remain in test code

## Test Requirements
- [ ] Run the full advisory test suite: `cargo test --test advisory` passes
- [ ] Run the full test suite: `cargo test` passes with no regressions in other test files
- [ ] Verify that test database setup correctly creates the enum type via migrations

## Verification Commands
- `cargo test --test advisory` — all advisory tests pass
- `cargo test` — full test suite passes

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
