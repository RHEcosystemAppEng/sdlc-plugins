# Task 6 — Update integration tests for advisory status enum migration

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory integration tests to reflect the new schema where advisory status is stored as an enum column on the `advisory` table instead of a joined lookup table. Ensure test fixtures, setup code, and assertions all use the new `AdvisoryStatusEnum` type and direct column references. Verify that the advisory list endpoint status filtering works correctly with the enum column.

## Files to Modify
- `tests/api/advisory.rs` — update all advisory integration tests: (1) remove any test setup code that inserts into `advisory_status` table; (2) update test advisory creation to set `status` enum column directly; (3) update assertions that verify status values to expect enum-based responses; (4) add tests for status filtering with enum values; (5) verify response format is unchanged (status is still a string in the JSON response)
- `tests/Cargo.toml` — add dependency on `entity` crate if not already present (needed for `AdvisoryStatusEnum` type in tests)

## Implementation Notes
- Integration tests in `tests/api/` hit a real PostgreSQL test database — the new migration must be applied to the test database before these tests can run
- Follow the existing test pattern: `assert_eq!(resp.status(), StatusCode::OK)` for status code checks
- Test fixtures that previously created `advisory_status` rows must be updated to set the enum value directly on the advisory record
- Verify that the JSON response shape remains identical — the `status` field should still be a string value (e.g., `"Fixed"`, `"New"`), not the enum's Rust representation
- Reference `tests/api/sbom.rs` for the integration test structure and patterns used in this project
- Per docs/constraints.md §5.11: add doc comments to every test function
- Per docs/constraints.md §5.12: add given-when-then inline comments to non-trivial test functions

## Reuse Candidates
- `tests/api/sbom.rs` — reference for SBOM endpoint integration test patterns (setup, request building, assertion style)
- `tests/api/advisory.rs` — existing advisory tests to modify (inspect current test structure before updating)

## Acceptance Criteria
- [ ] All advisory integration tests pass against the new schema
- [ ] No test code references the `advisory_status` table or `status_id` column
- [ ] Tests verify status filtering works with enum values (e.g., filter by "Fixed")
- [ ] Tests verify JSON response still contains status as a string field
- [ ] Test setup code creates advisories with enum status directly

## Test Requirements
- [ ] Test: list advisories filtered by status "Fixed" returns only fixed advisories
- [ ] Test: list advisories filtered by status "New" returns only new advisories
- [ ] Test: get advisory by ID returns correct status enum value as string
- [ ] Test: list advisories without filter returns all advisories with correct statuses
- [ ] All existing advisory test scenarios still pass

## Verification Commands
- `cargo test --test api -- advisory` — all advisory integration tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 2 — Create migration to replace advisory_status table with enum column
- Depends on: Task 4 — Update advisory service and endpoints to use enum column
- Depends on: Task 5 — Update advisory ingestion pipeline to write enum values directly
