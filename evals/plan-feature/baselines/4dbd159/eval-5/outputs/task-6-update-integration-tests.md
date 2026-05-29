# Task 6 — Update advisory integration tests for enum-based status

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory integration tests to reflect the new schema where `advisory.status` is an enum column instead of a foreign key to the `advisory_status` lookup table. Test fixtures, setup code, and assertions must be updated to work with the enum column directly. Add test coverage for status filtering to verify the eliminated join produces correct results.

## Files to Modify
- `tests/api/advisory.rs` — update all advisory integration tests:
  - Remove any test setup code that inserts rows into the `advisory_status` table
  - Update advisory fixture creation to set `status` as an enum value directly instead of `status_id` as a foreign key
  - Update assertions that verify status values in API responses to confirm the string representation matches the enum variant names
  - Add test cases for status-based filtering (e.g., `GET /api/v2/advisory?status=Fixed`) to verify the eliminated join returns correct filtered results

## Implementation Notes
- Follow the existing integration test patterns in `tests/api/advisory.rs` and `tests/api/sbom.rs` — tests hit a real PostgreSQL test database and use `assert_eq!(resp.status(), StatusCode::OK)` pattern
- Test fixture advisory records should be created with the new entity model — set `status: ActiveValue::Set(AdvisoryStatusEnum::Fixed)` instead of `status_id: ActiveValue::Set(1)`
- Verify that the JSON response shape is unchanged: the `status` field in the response should be a plain string (`"Fixed"`, `"New"`, etc.), not a JSON object
- Add at least one test that filters the advisory list by status to confirm the enum-based filtering works correctly without the join
- Remove any test helper functions or fixtures that create or reference `advisory_status` table rows

## Reuse Candidates
- `tests/api/sbom.rs` — reference for integration test patterns, fixture setup, and assertion style
- `tests/api/advisory.rs` — existing advisory tests to adapt (update rather than rewrite from scratch)

## Acceptance Criteria
- [ ] All advisory integration tests pass against the new schema
- [ ] No test code references the `advisory_status` table or `status_id` column
- [ ] Advisory fixture creation uses `AdvisoryStatusEnum` variants directly
- [ ] At least one test verifies status filtering on the list endpoint
- [ ] API response shape in test assertions matches the pre-migration format (status as string)

## Test Requirements
- [ ] `cargo test --test api -- advisory` passes all advisory integration tests
- [ ] Status filter test verifies that `GET /api/v2/advisory?status=Fixed` returns only advisories with status Fixed
- [ ] Verify that creating an advisory via ingestion and then querying it returns the correct status string

## Verification Commands
- `cargo test --test api -- advisory` — all advisory integration tests pass
- `cargo test` — full test suite passes (no regressions in other modules)

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 4 — Update advisory service and endpoints to use enum column
- Depends on: Task 5 — Update advisory ingestion pipeline to write enum values directly
