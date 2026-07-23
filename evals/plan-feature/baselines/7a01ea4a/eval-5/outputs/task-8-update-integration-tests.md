## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory integration tests to reflect the new schema. Tests should no longer set up `advisory_status` lookup table data or join through it. Instead, tests should create advisories with enum status values directly and verify that filtering, fetching, and ingestion work correctly with the enum column.

## Files to Modify
- `tests/api/advisory.rs` -- update all advisory test cases to: (1) remove any test fixtures that insert into the `advisory_status` table, (2) create advisories with `status: AdvisoryStatusEnum` values directly, (3) verify status filtering via `GET /api/v2/advisory?status=Fixed` works with enum comparison, (4) verify advisory detail responses contain the correct status string

## Implementation Notes
- Follow the existing test pattern in `tests/api/sbom.rs` for reference on integration test structure using `assert_eq!(resp.status(), StatusCode::OK)`.
- The integration tests hit a real PostgreSQL test database -- after the migration runs on the test database, the `advisory_status` table will no longer exist. Any test setup that references it must be removed or updated.
- Verify that the test database migration is applied before tests run (the test harness should run migrations automatically).
- Test cases should cover:
  - Listing advisories without a status filter (returns all)
  - Listing advisories with a status filter (returns only matching)
  - Fetching a single advisory by ID (status field is correct)
  - Ingesting an advisory and verifying its status is stored correctly
- Per docs/constraints.md section 2 (Commit Rules): commit messages must follow Conventional Commits format, reference TC-9005 in the footer, and include the `--trailer="Assisted-by: Claude Code"`.
- Per docs/constraints.md section 5.11: add a doc comment to every test function created or modified.
- Per docs/constraints.md section 5.12: add given-when-then inline comments to non-trivial test functions.

## Reuse Candidates
- `tests/api/sbom.rs` -- reference for integration test patterns (endpoint testing, response assertion, test database setup)

## Acceptance Criteria
- [ ] All advisory integration tests pass with the new enum schema
- [ ] No remaining references to `advisory_status` table setup in test fixtures
- [ ] Tests cover all four status enum values (New, Analyzing, Fixed, Rejected)
- [ ] Tests verify the API response shape is unchanged (status is a string)

## Test Requirements
- [ ] Test advisory list without filter returns all statuses
- [ ] Test advisory list with `?status=Fixed` filter returns only Fixed advisories
- [ ] Test advisory list with `?status=New` filter returns only New advisories
- [ ] Test advisory get by ID returns correct status string
- [ ] Test advisory ingestion stores enum value correctly

## Verification Commands
- `cargo test -p tests --test advisory` -- all advisory integration tests pass
- `cargo test` -- full test suite passes (no regressions)

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
- Depends on: Task 2 -- Create migration for advisory_status_enum
- Depends on: Task 5 -- Update AdvisoryService
- Depends on: Task 6 -- Update advisory endpoints
- Depends on: Task 7 -- Update ingestion pipeline
