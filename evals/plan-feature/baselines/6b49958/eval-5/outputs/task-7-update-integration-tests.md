## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory integration tests to reflect the new schema: replace any test setup that inserts into the `advisory_status` lookup table with direct enum value usage, update assertions to match the new query behavior, and verify that status filtering works correctly with the enum column.

## Files to Modify
- `tests/api/advisory.rs` — update test setup to create advisories with `status` enum values instead of `status_id` foreign keys; update assertions for status filtering and response shape; add test cases for each enum value

## Implementation Notes
- In `tests/api/advisory.rs`, locate test fixture setup code that inserts rows into `advisory_status` and references them via `status_id`. Replace with direct `AdvisoryStatusEnum` values on the advisory insert.
- Follow the existing integration test pattern: tests hit a real PostgreSQL test database and use `assert_eq!(resp.status(), StatusCode::OK)` for response validation.
- Ensure tests cover all four status enum values (New, Analyzing, Fixed, Rejected) for both insertion and filtering.
- Test that the JSON response shape is unchanged — `status` should still appear as a string in the response body, not as an enum object.
- Reference the test patterns in `tests/api/sbom.rs` for how list endpoint tests are structured with pagination and filtering assertions.
- Remove any test helper functions that create or reference `advisory_status` table rows.

## Reuse Candidates
- `tests/api/sbom.rs` — demonstrates integration test patterns for list endpoints with filtering, pagination, and response shape assertions
- `tests/api/advisory.rs` — the existing test file being modified, containing the current test patterns to adapt

## Acceptance Criteria
- [ ] All advisory integration tests pass with the new enum-based schema
- [ ] No test code references the `advisory_status` entity or table
- [ ] Tests cover listing, filtering by each status value, and single advisory retrieval
- [ ] Response shape assertions confirm backward compatibility (status as string)

## Test Requirements
- [ ] Test `GET /api/v2/advisory` with advisories having all four status values
- [ ] Test `GET /api/v2/advisory?status=Fixed` returns only fixed advisories
- [ ] Test `GET /api/v2/advisory?status=New` returns only new advisories
- [ ] Test `GET /api/v2/advisory/{id}` returns correct status string in response body
- [ ] Test that advisory creation via ingestion with enum status works end-to-end

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main

[sdlc-workflow] Description digest: sha256:cf76997ba90e5f632e48810a2adfda4cca58f360c23ffe793af7ebc0f125b6b8
