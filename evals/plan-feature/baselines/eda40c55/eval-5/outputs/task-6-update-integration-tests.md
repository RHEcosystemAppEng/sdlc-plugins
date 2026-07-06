## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory integration tests to work with the new `advisory_status_enum` column instead of the `advisory_status` lookup table. Test fixtures and assertions must use the enum column directly. Verify that advisory list filtering by status, single advisory retrieval, and search results all function correctly with the migrated schema.

## Files to Modify
- `tests/api/advisory.rs` — update test fixtures to insert advisories with `status: AdvisoryStatusEnum` instead of inserting into `advisory_status` and using `status_id`; update assertions to verify status enum values; add test cases for filtering by each enum variant

## Implementation Notes
- Update test data setup to use the `advisory_status_enum` column directly. Replace any fixture code that inserts rows into `advisory_status` and references them by ID with direct `AdvisoryStatusEnum` values.
- Ensure all four status values (New, Analyzing, Fixed, Rejected) are covered in test fixtures.
- Verify that the response JSON serializes status as a plain string (e.g., `"status": "Fixed"`) matching the pre-migration format — no API contract change.
- Per CONVENTIONS.md §Testing: integration tests must hit a real PostgreSQL test database and use the `assert_eq!(resp.status(), StatusCode::OK)` pattern.
  Applies: task modifies `tests/api/advisory.rs` matching the convention's `.rs` test file scope.

## Reuse Candidates
- `tests/api/advisory.rs` — existing test structure and patterns to modify in place
- `tests/api/sbom.rs` — reference for integration test patterns (request construction, response assertion, test database setup)

## Acceptance Criteria
- [ ] All existing advisory integration tests pass with the new schema
- [ ] Tests verify status filtering using enum values for all four statuses
- [ ] Tests verify that API response format for status is unchanged (string representation)
- [ ] No test code references `advisory_status` table or entity
- [ ] Test coverage includes advisory list, advisory get, and status filtering

## Test Requirements
- [ ] Run `cargo test -p tests --test advisory` — all tests pass
- [ ] Verify test for `GET /api/v2/advisory?status=Fixed` returns only Fixed advisories
- [ ] Verify test for `GET /api/v2/advisory?status=New` returns only New advisories
- [ ] Verify test for `GET /api/v2/advisory/{id}` includes correct status in response

## Verification Commands
- `cargo test -p tests --test advisory` — all advisory integration tests pass
- `cargo test -p tests` — full integration test suite passes

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 4 — Update advisory service layer and endpoints to use status enum
- Depends on: Task 5 — Update advisory ingestion pipeline for status enum
