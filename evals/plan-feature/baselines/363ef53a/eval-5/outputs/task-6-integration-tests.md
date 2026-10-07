## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory integration tests to work with the new enum-based status column. Tests must verify that advisory listing with status filtering, advisory detail retrieval, and advisory ingestion all function correctly with the enum schema. The response shape must remain backward compatible (status is still a string in the JSON response).

## Files to Modify
- `tests/api/advisory.rs` -- Update test data setup to use `AdvisoryStatusEnum` values instead of `advisory_status` table inserts; update assertions for status filtering; add test cases for enum-based filtering and ingestion

## Implementation Notes
- Update test fixtures: replace `advisory_status` table inserts with direct `AdvisoryStatusEnum` values in advisory test data setup
- Follow the existing test pattern: tests hit a real PostgreSQL test database and use `assert_eq!(resp.status(), StatusCode::OK)` assertions
- Add or update test cases for:
  - Listing advisories filtered by a specific status enum value (covers UC-1 from the feature)
  - Ingesting an advisory with a direct enum status (covers UC-2 from the feature)
  - Verifying the response shape is unchanged (status is still a string in the JSON response)
- Ensure the test database runs the new enum migration (Task 2) before tests execute

Per CONVENTIONS.md §Testing: integration tests in `tests/api/` hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern.
Applies: task modifies `tests/api/advisory.rs` matching the convention's test file scope.

## Reuse Candidates
- `tests/api/sbom.rs` -- SBOM integration test patterns for reference on test structure, fixture setup, and assertion patterns
- `tests/api/advisory.rs` -- Existing advisory tests to understand current test data setup and assertion patterns

## Acceptance Criteria
- [ ] All existing advisory tests pass with the updated schema
- [ ] Test data setup uses `AdvisoryStatusEnum` values instead of `advisory_status` table inserts
- [ ] Test for advisory list with status filter (e.g., `GET /api/v2/advisory?status=Fixed`) passes and returns correct results
- [ ] Test for advisory detail retrieval confirms status is returned as a string in the response JSON
- [ ] Test for advisory ingestion with enum status passes and stores the correct value
- [ ] No references to the `advisory_status` table remain in the test code

## Test Requirements
- [ ] `cargo test --test advisory` passes -- all advisory integration tests pass
- [ ] Advisory list endpoint returns correct filtered results when filtering by status
- [ ] Advisory response JSON includes status as a string field (backward compatible)
- [ ] Ingestion test creates advisory records with the correct enum status value

## Verification Commands
- `cargo test --test advisory` -- Run advisory integration tests
- `cargo test` -- Run all tests to verify no regressions across the test suite

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
- Depends on: Task 4 -- Update advisory service and endpoints to use status enum
- Depends on: Task 5 -- Update advisory ingestion pipeline for direct enum writes
