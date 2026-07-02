# Task 6 — Update advisory integration tests for status enum

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory endpoint integration tests to reflect the new schema where advisory status is stored as a PostgreSQL enum column on the `advisory` table instead of a joined lookup table. Test fixtures must stop seeding the `advisory_status` lookup table and instead use enum values directly. Assertions must verify that status filtering and status fields in API responses work correctly with the enum-based schema.

## Files to Modify
- `tests/api/advisory.rs` — Update test fixtures to use enum-based status values; remove any `advisory_status` table seeding; update assertions for status filtering and response shape

## Implementation Notes
- In `tests/api/advisory.rs`, locate test setup code that inserts rows into the `advisory_status` table and then references them via `status_id`. Replace this with direct advisory inserts that set the `status` enum column.
- Update status filter test cases: verify that `GET /api/v2/advisory?status=Fixed` correctly filters using the enum column instead of the join. The query parameter value should match the enum variant name (e.g., `Fixed`, `New`).
- Follow the existing integration test pattern: tests hit a real PostgreSQL test database and use `assert_eq!(resp.status(), StatusCode::OK)` for response status checks.
- Verify that the API response JSON shape is unchanged — the `status` field in the response should still be a string value (e.g., `"Fixed"`, `"New"`), not a numeric ID.
- Reference the SBOM integration tests in `tests/api/sbom.rs` for the established test structure pattern (setup, request, assertion).
- Per CONVENTIONS.md §Testing: integration tests in `tests/api/` hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern.
  Applies: task modifies `tests/api/advisory.rs` matching the convention's test file scope.

## Reuse Candidates
- `tests/api/sbom.rs` — Reference for integration test structure and assertion patterns
- `tests/api/search.rs` — Reference for test patterns that verify query parameter filtering

## Acceptance Criteria
- [ ] No integration test references the `advisory_status` lookup table
- [ ] Tests seed advisory data with enum status values directly
- [ ] Advisory list endpoint test verifies correct status values in JSON response
- [ ] Advisory list endpoint test with status filter verifies correct filtering behavior
- [ ] Advisory get endpoint test verifies correct status value for a single advisory
- [ ] All advisory integration tests pass

## Test Requirements
- [ ] Test advisory list endpoint returns advisories with correct string status values
- [ ] Test advisory list endpoint with `?status=Fixed` filter returns only advisories with status `Fixed`
- [ ] Test advisory list endpoint with `?status=New` filter returns only advisories with status `New`
- [ ] Test advisory get endpoint returns the correct status for a specific advisory
- [ ] Test that the response shape is unchanged (status is a string, not a numeric ID)

## Verification Commands
- `cargo test --test advisory` — expected: all advisory integration tests pass
- `cargo test` — expected: full test suite passes

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 4 — Update advisory service and model layer to use status enum column
- Depends on: Task 5 — Update advisory ingestion pipeline to write enum values directly

---

[sdlc-workflow] Description digest: sha256-md:43a9155e4da39ed2c77ff58b36ad547332ec773d212650727ec5dd7c30f58a94
