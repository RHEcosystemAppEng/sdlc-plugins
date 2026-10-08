## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory endpoint integration tests to work with the new enum-based status schema. Tests must verify that the advisory list and detail endpoints correctly return status values from the enum column, and that status filtering works without the `advisory_status` lookup table join. All test fixtures must be updated to insert advisories with enum status values directly.

## Files to Modify
- `tests/api/advisory.rs` -- update test data setup to insert advisories with `AdvisoryStatusEnum` values instead of creating `advisory_status` rows and linking via FK; update assertions to verify status values from the enum column; add test cases for enum-based status filtering

## Implementation Notes
- Update test fixtures: replace advisory_status table inserts and FK linking with direct enum value assignment on advisory rows
- Verify the established assertion pattern is followed: `assert_eq!(resp.status(), StatusCode::OK)` for all endpoint response checks
- Add test cases covering status filtering: `GET /api/v2/advisory?status=Fixed` should return only advisories with the `Fixed` enum status
- Test data setup should use all four enum values (New, Analyzing, Fixed, Rejected) to ensure comprehensive coverage
- Ensure test database migration runs the new migration before test execution

Per CONVENTIONS.md section "Testing": integration tests in `tests/api/` hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern.
Applies: task modifies `tests/api/advisory.rs` matching the convention's Rust file scope.

## Reuse Candidates
- `tests/api/sbom.rs` -- SBOM integration tests showing the established test setup, request building, and assertion patterns without lookup table dependencies
- `tests/api/advisory.rs` -- current advisory tests to understand existing test structure before refactoring

## Acceptance Criteria
- [ ] All existing advisory integration tests pass with the new enum-based schema
- [ ] Test for `GET /api/v2/advisory` verifies status values are returned correctly from enum column
- [ ] Test for `GET /api/v2/advisory/{id}` verifies advisory detail status is correct
- [ ] Test for status filtering (`GET /api/v2/advisory?status=Fixed`) returns correctly filtered results
- [ ] No test code references the `advisory_status` lookup table or `status_id` FK column
- [ ] Test data uses all four enum values: New, Analyzing, Fixed, Rejected

## Test Requirements
- [ ] Integration tests run against a real PostgreSQL test database with the new migration applied
- [ ] Tests cover all four status enum values (New, Analyzing, Fixed, Rejected) in test data
- [ ] Tests verify positive status filtering (matching status returns results)
- [ ] Tests verify negative status filtering (non-matching status returns empty results)
- [ ] Tests verify the API response shape is unchanged (status is a string in the JSON response)

## Verification Commands
- `cargo test --test advisory` -- advisory integration tests pass

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
- Depends on: Task 4 -- Update advisory service and endpoints to use status enum
- Depends on: Task 5 -- Update advisory ingestion pipeline to write enum values
