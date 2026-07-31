## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory integration tests to verify the new enum-based status schema. Tests must validate that advisory CRUD operations, status filtering, and ingestion work correctly with the `advisory_status_enum` column instead of the old `advisory_status` lookup table join. Remove any test setup code that inserts rows into the `advisory_status` table and replace it with direct enum value usage.

## Files to Modify
- `tests/api/advisory.rs` -- update advisory endpoint integration tests: remove `advisory_status` table setup/seed data; update test advisory creation to use enum status values; verify status filtering works with enum comparisons; verify response payloads contain correct status strings

## Implementation Notes
- Follow the existing test pattern in `tests/api/sbom.rs` for integration test structure (setup, HTTP request, assertion pattern)
- Tests use `assert_eq!(resp.status(), StatusCode::OK)` per the project convention
- Test setup: when creating test advisory records, use `AdvisoryStatusEnum` values directly instead of inserting into the lookup table
- Remove any `advisory_status` table seed data from test fixtures
- Verify the API response shape is unchanged: the `status` field in JSON responses should still be a plain string (e.g., `"Fixed"`, `"New"`)
- Test the status filter parameter on the list endpoint to ensure it works with enum values

## Reuse Candidates
- `tests/api/sbom.rs` -- reference for integration test patterns (setup, request, assertion)
- `tests/api/advisory.rs` -- existing advisory tests to be modified

## Acceptance Criteria
- [ ] All advisory integration tests pass with the new enum-based schema
- [ ] Test setup code no longer references the `advisory_status` lookup table
- [ ] Tests verify status filtering on the advisory list endpoint works with enum values
- [ ] Tests verify the advisory get endpoint returns the correct status string
- [ ] Tests verify advisory ingestion stores the correct enum status value
- [ ] API response shape is unchanged in test assertions (status is still a string)

## Test Requirements
- [ ] Test advisory list endpoint with no status filter returns all advisories with correct status strings
- [ ] Test advisory list endpoint with status filter `?status=Fixed` returns only "Fixed" advisories
- [ ] Test advisory get endpoint returns the correct status string for a specific advisory
- [ ] Test advisory creation via ingestion stores and returns the correct enum status

## Verification Commands
- `cargo test --test advisory` -- all advisory integration tests pass

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
- Depends on: Task 4 -- Update advisory service layer and endpoints
- Depends on: Task 5 -- Update advisory ingestion pipeline
