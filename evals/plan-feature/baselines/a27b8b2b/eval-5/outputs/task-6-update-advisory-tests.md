## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory integration tests to reflect the new schema where advisory status is an enum column instead of a joined lookup table. Tests must verify that advisory endpoints return correct status values, that status filtering works with the enum column, and that the API response shape is unchanged. This ensures the migration and code changes are validated end-to-end against a real PostgreSQL test database.

## Files to Modify
- `tests/api/advisory.rs` — update advisory endpoint integration tests: remove any test setup that inserts into the `advisory_status` lookup table; update test data insertion to use enum values directly; verify status filtering works with the new enum column; verify response shape is unchanged

## Implementation Notes
- Follow the existing test pattern in `tests/api/advisory.rs`: integration tests hit a real PostgreSQL test database using `assert_eq!(resp.status(), StatusCode::OK)`.
- Update test data setup: instead of inserting rows into `advisory_status` and referencing them via FK, insert advisory rows with the enum status value directly.
- Test all four status values: New, Analyzing, Fixed, Rejected.
- Test status-based filtering: verify that `GET /api/v2/advisory?status=Fixed` returns only advisories with status Fixed.
- Verify response shape: the JSON response should still contain a `status` string field with the same values as before.
- Reference existing SBOM tests in `tests/api/sbom.rs` for test structure and assertion patterns.

## Reuse Candidates
- `tests/api/sbom.rs` — SBOM endpoint integration tests; follow the same test structure and assertion patterns for consistency
- `tests/api/advisory.rs` — existing advisory tests being modified; preserve test structure while updating data setup

## Acceptance Criteria
- [ ] All advisory endpoint tests pass with the new enum-based schema
- [ ] Tests verify all four status enum values (New, Analyzing, Fixed, Rejected)
- [ ] Tests verify status filtering works correctly with enum values
- [ ] Tests verify the API response shape is unchanged (status is still a string in the JSON response)
- [ ] No test code references the `advisory_status` lookup table or `status_id` column

## Test Requirements
- [ ] `cargo test --test advisory` passes against a PostgreSQL test database with the new migration applied
- [ ] Test coverage includes listing advisories with mixed statuses
- [ ] Test coverage includes filtering by a single status value
- [ ] Test coverage includes retrieving a single advisory and verifying the status field

## Verification Commands
- `cargo test --test advisory` — all advisory integration tests pass
- `grep -r "advisory_status\|status_id" tests/` — no remaining references to old schema in tests

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 2 — Create migration for advisory status enum
- Depends on: Task 4 — Update advisory service and endpoints
- Depends on: Task 5 — Update advisory ingestion pipeline
