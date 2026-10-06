## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory integration tests to reflect the new enum-based status column. The tests currently exercise advisory endpoints that join the `advisory_status` lookup table — they must be updated to work with the direct `status` enum column. Add test coverage for status filtering using the enum column to verify the p95 latency improvement from eliminating the join.

## Files to Modify
- `tests/api/advisory.rs` — update existing advisory endpoint tests to work with the enum-based status column; remove any test setup that seeds the `advisory_status` lookup table; add tests for status filtering (`?status=Fixed`, `?status=New`, etc.) using the enum column; verify response shape is unchanged

## Implementation Notes
- Update test database setup: remove any `INSERT INTO advisory_status` seed data. Advisories should now be created with the `status` enum column set directly.
- If tests use SeaORM `ActiveModel` to create test data, update them to set `status: Set(AdvisoryStatusEnum::Fixed)` instead of `status_id: Set(some_id)`.
- Add test cases for each status filter value: `New`, `Analyzing`, `Fixed`, `Rejected`.
- Verify that the response JSON shape has not changed — the `status` field should still be a string value, not the enum variant representation.
- Per CONVENTIONS.md §Testing: integration tests hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern.
  Applies: task modifies `tests/api/advisory.rs` matching the convention's Rust test file scope.

## Reuse Candidates
- `tests/api/advisory.rs` — existing advisory tests show the established test setup, request, and assertion patterns
- `tests/api/sbom.rs` — reference for integration test patterns in the project

## Acceptance Criteria
- [ ] All existing advisory endpoint tests pass with the new enum-based schema
- [ ] Test setup no longer seeds `advisory_status` lookup table
- [ ] Test data creation uses `AdvisoryStatusEnum` variants directly
- [ ] Status filtering tests cover all four enum values (New, Analyzing, Fixed, Rejected)
- [ ] Response shape assertions confirm status is still a string in the JSON response
- [ ] No references to `advisory_status` table or entity remain in test code

## Test Requirements
- [ ] `GET /api/v2/advisory` returns advisories with correct string status values
- [ ] `GET /api/v2/advisory?status=Fixed` returns only advisories with status `Fixed`
- [ ] `GET /api/v2/advisory?status=New` returns only advisories with status `New`
- [ ] `GET /api/v2/advisory/{id}` returns advisory detail with correct status string
- [ ] Response status field is a JSON string (not an object or number)

## Verification Commands
- `cargo test -p tests -- advisory` — all advisory tests pass
- `grep -r "advisory_status" tests/` — returns no matches

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 4 — Update advisory service and endpoints to use status enum column
- Depends on: Task 5 — Update advisory ingestion pipeline for direct enum writes
