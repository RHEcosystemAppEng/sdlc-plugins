## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory integration tests to reflect the new enum-based schema. Tests must verify that advisory CRUD operations, status filtering, and ingestion work correctly with the `advisory_status_enum` column instead of the lookup table. This ensures the migration and code changes are fully validated before merging.

## Files to Modify
- `tests/api/advisory.rs` — update all advisory integration tests: remove setup code that inserts into `advisory_status` table; update assertions to check enum status values; add tests for status filtering with enum values; verify ingestion writes enum values directly
- `tests/Cargo.toml` — update dependencies if the entity crate's public API changed (e.g., new `AdvisoryStatusEnum` type needs to be imported)

## Implementation Notes
In `tests/api/advisory.rs`:
- The existing tests likely set up test data by inserting into the `advisory_status` table and then creating advisories with `status_id`. Replace this with direct advisory creation using `AdvisoryStatusEnum` values.
- Follow the existing test pattern: tests use `assert_eq!(resp.status(), StatusCode::OK)` and hit a real PostgreSQL test database.
- Add test cases for each enum variant (New, Analyzing, Fixed, Rejected) to ensure all values work correctly.
- Test the status filter query parameter with enum values.
- Test that the response shape is unchanged — status should still appear as a string in the JSON response.

Update assertions from checking joined status name to checking the direct enum field:
```rust
// Before: status came from advisory_status join
// After: status comes from advisory.status enum column
assert_eq!(advisory_summary.status, "Fixed");
```

## Acceptance Criteria
- [ ] All existing advisory integration tests pass with the new schema
- [ ] Tests no longer reference or set up `advisory_status` table data
- [ ] Test coverage includes all four enum variants (New, Analyzing, Fixed, Rejected)
- [ ] Status filtering is tested in integration tests
- [ ] Response shape assertions confirm status is still returned as a string

## Test Requirements
- [ ] `cargo test -p tests --test advisory` passes with all tests green
- [ ] No test references `advisory_status` table or entity
- [ ] New test case verifies filtering advisories by each status enum value
- [ ] New test case verifies advisory ingestion with enum status

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005
- Depends on: Task 5 — Update advisory endpoints and ingestion
