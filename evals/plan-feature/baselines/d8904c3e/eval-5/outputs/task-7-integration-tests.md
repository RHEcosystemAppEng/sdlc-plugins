## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory endpoint integration tests to reflect the new schema where status is an enum column on the `advisory` table instead of a join to the `advisory_status` lookup table. Tests must verify that advisory queries, status filtering, and the ingestion pipeline all work correctly with the enum column.

## Files to Modify
- `tests/api/advisory.rs` — update test data setup to use enum status values instead of inserting into `advisory_status` table; update assertions to verify status field from enum column; add tests for status filtering with enum values

## Implementation Notes
- Per CONVENTIONS.md §Testing: integration tests in `tests/api/` hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern.
  Applies: task modifies `tests/api/advisory.rs` matching the convention's test file scope.
- See `tests/api/sbom.rs` for the standard integration test pattern (SBOM tests follow the same test database setup and assertion structure)
- Update test data setup: instead of inserting rows into `advisory_status` table and referencing via FK, set the `status` enum column directly on advisory entities using `AdvisoryStatusEnum` values
- Test status filter: verify that `GET /api/v2/advisory?status=Fixed` returns only matching advisories
- Test all four status values: New, Analyzing, Fixed, Rejected
- Verify response shape is unchanged — status appears as a string in the JSON response, matching the pre-migration format
- Remove any test helper code that inserts into the `advisory_status` table

## Reuse Candidates
- `tests/api/sbom.rs` — reference integration test implementation following the standard test pattern with database setup and HTTP assertions
- `tests/api/advisory.rs` (existing) — existing advisory tests provide the baseline test structure and helpers to update

## Acceptance Criteria
- [ ] All existing advisory integration tests pass with the enum-based schema
- [ ] New tests cover status filtering with each enum value (New, Analyzing, Fixed, Rejected)
- [ ] Test data setup uses enum values directly (no advisory_status table inserts)
- [ ] Response shape assertions confirm backward compatibility (status as string in JSON)

## Test Requirements
- [ ] Test suite passes against a PostgreSQL database with the new schema (`cargo test -p tests -- advisory`)
- [ ] Each status filter value returns correct results
- [ ] Edge case: empty result set when filtering by a status with no matching advisories

## Verification Commands
- `cargo test -p tests -- advisory` — advisory integration tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 5 — Update advisory endpoints (tests verify endpoint behavior)
- Depends on: Task 6 — Update advisory ingestion pipeline (tests may verify ingestion behavior)
