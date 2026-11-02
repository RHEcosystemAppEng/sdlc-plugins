## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory integration tests to validate the new enum-based status column. Tests must verify that status filtering, advisory detail retrieval, and ingestion all work correctly with the `advisory_status_enum` type instead of the `advisory_status` lookup table join.

## Files to Modify
- `tests/api/advisory.rs` — update existing advisory integration tests to work with the enum-based status column: remove any test setup that inserts into the `advisory_status` table; update status filter test assertions to use enum values; add test cases for each of the four enum values; verify advisory list endpoint returns correct status strings

## Implementation Notes
- Follow the existing integration test pattern in `tests/api/advisory.rs` and `tests/api/sbom.rs`: tests hit a real PostgreSQL test database using `assert_eq!(resp.status(), StatusCode::OK)` pattern
- Remove any test fixture setup that creates `advisory_status` table rows — the enum type is created by the migration and does not need seed data
- Test status filtering by querying `GET /api/v2/advisory?status=Fixed` and verifying the response contains only advisories with the `Fixed` status
- Test advisory detail by querying `GET /api/v2/advisory/{id}` and verifying the `status` field in the response is a valid string
- Per CONVENTIONS.md §Testing: integration tests in `tests/api/` hit a real PostgreSQL test database.
  Applies: task modifies `tests/api/advisory.rs` matching the convention's integration test scope.

## Acceptance Criteria
- [ ] All existing advisory integration tests pass with the new enum-based schema
- [ ] Status filter tests verify filtering by each of the four enum values (New, Analyzing, Fixed, Rejected)
- [ ] Advisory detail test verifies the `status` field is returned as a string
- [ ] No test references the `advisory_status` lookup table
- [ ] Ingestion integration test verifies end-to-end: ingest advisory → query it → status matches

## Test Requirements
- [ ] `GET /api/v2/advisory` returns advisories with status as a string field
- [ ] `GET /api/v2/advisory?status=Fixed` returns only Fixed-status advisories
- [ ] `GET /api/v2/advisory?status=New` returns only New-status advisories
- [ ] `GET /api/v2/advisory/{id}` returns correct status for a specific advisory
- [ ] Advisory ingestion followed by API query returns matching status value

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 4 — Update advisory service and endpoints (tests validate service behavior)
- Depends on: Task 5 — Update ingestion pipeline (tests validate ingestion behavior)
