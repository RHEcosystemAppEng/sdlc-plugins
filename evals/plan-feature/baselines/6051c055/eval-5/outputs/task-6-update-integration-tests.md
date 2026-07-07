# Task 6 — Update advisory integration tests for status enum migration

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory integration tests to work with the new `advisory_status_enum` column instead of the `advisory_status` lookup table. The existing tests set up advisory data using the lookup table for status assignment and assert on status values retrieved via the join. After the migration, tests must insert advisories with enum status values directly and verify that the API returns the correct status strings.

## Files to Modify
- `tests/api/advisory.rs` — Update all advisory integration tests: replace `advisory_status` table setup with direct enum value insertion; update status filter test cases to use enum values; verify API response status field matches expected enum string values
- `tests/Cargo.toml` — Update dependencies if needed to import the `AdvisoryStatusEnum` type from the entity crate

## Implementation Notes
- Replace test setup code that inserts rows into `advisory_status` and sets `status_id` with code that sets `status: AdvisoryStatusEnum::Fixed` (etc.) directly on advisory entities
- Update assertions that verify status values to match the string representation of enum variants
- Ensure test database migrations run the new migration before tests execute
- Per CONVENTIONS.md §Testing: integration tests must hit a real PostgreSQL test database and use the `assert_eq!(resp.status(), StatusCode::OK)` assertion pattern.
  Applies: task modifies `tests/api/advisory.rs` matching the convention's test file scope.

## Reuse Candidates
- `tests/api/sbom.rs` — Reference for integration test patterns, particularly test setup and assertion style
- `entity/src/advisory.rs::AdvisoryStatusEnum` — The enum type that must be used in test data setup

## Acceptance Criteria
- [ ] All advisory integration tests pass against the new schema
- [ ] Tests verify status filtering by enum value works correctly
- [ ] Tests verify the API response shape is unchanged (status returned as string)
- [ ] No references to `advisory_status` entity or lookup table remain in test code

## Test Requirements
- [ ] Verify GET /api/v2/advisory returns advisories with correct status values from the enum column
- [ ] Verify GET /api/v2/advisory with status filter returns only matching advisories
- [ ] Verify GET /api/v2/advisory/{id} returns the correct status for a specific advisory
- [ ] Verify that status values in API responses match the expected string format (e.g., "Fixed", not "fixed")

## Verification Commands
- `cargo test --test advisory` — all advisory integration tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 4 — Update advisory service and endpoints to use status enum column
- Depends on: Task 5 — Update advisory ingestion pipeline to write enum values directly
