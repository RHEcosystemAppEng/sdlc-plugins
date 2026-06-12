# Task 7 — Update advisory integration tests for enum status column

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory integration tests to work with the new enum-based status column. Tests must verify that advisory CRUD operations, status filtering, and the ingestion pipeline all function correctly with the `advisory_status_enum` column instead of the `advisory_status` lookup table join.

## Files to Modify
- `tests/api/advisory.rs` — update all advisory integration tests: remove any test setup that inserts rows into the `advisory_status` table; update test data setup to set `status` as an enum value directly on advisory records; update assertions to verify status as a string from the enum column; add test cases for status filtering with the enum column

## Implementation Notes
- The existing integration tests likely set up test data by inserting into `advisory_status` and using the resulting IDs as `status_id` foreign keys. Replace this with direct `AdvisoryStatusEnum` values on advisory records
- Follow the existing test pattern in `tests/api/sbom.rs` for test structure: use real PostgreSQL test database, `assert_eq!(resp.status(), StatusCode::OK)` pattern
- Test status filtering by sending `GET /api/v2/advisory?status=Fixed` and verifying only Fixed advisories are returned
- Verify that the response JSON still contains `status` as a string field (backward compatibility)
- Remove any test helpers or fixtures that reference the `advisory_status` table

## Reuse Candidates
- `tests/api/sbom.rs` — existing integration test pattern showing test setup, HTTP request construction, and response assertion patterns
- `tests/api/advisory.rs` — the existing advisory tests themselves contain the test infrastructure (database setup, client creation) that should be preserved

## Acceptance Criteria
- [ ] All advisory integration tests pass with the enum-based status column
- [ ] No test code references the `advisory_status` table
- [ ] Tests cover status filtering for at least two different status values
- [ ] Tests verify the API response shape is unchanged (status is a string)

## Test Requirements
- [ ] Test advisory list returns correct status string values
- [ ] Test advisory list with status filter returns only matching advisories
- [ ] Test advisory get by ID returns correct status
- [ ] Test advisory creation via ingestion sets status correctly

## Verification Commands
- `cargo test -p tests --test advisory` — all advisory integration tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 5 — Update advisory endpoints to use enum status filtering
- Depends on: Task 6 — Update advisory ingestion pipeline to write enum status directly
