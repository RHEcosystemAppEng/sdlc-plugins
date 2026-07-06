## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory integration tests to verify that the advisory endpoints and ingestion pipeline work correctly with the new `advisory_status_enum` column. The existing tests reference the `advisory_status` lookup table join and must be updated to reflect the new schema.

## Files to Modify
- `tests/api/advisory.rs` -- Update integration tests for advisory endpoints to verify enum-based status filtering and response shape

## Implementation Notes
- Update test fixtures and setup code to create advisories with the new `status` enum column instead of using `advisory_status` table inserts
- Verify that status filtering in the list endpoint works with enum values (`WHERE status = 'Fixed'` etc.)
- Verify the response JSON still contains status as a string (API backward compatibility)
- Follow the existing integration test pattern: use a real PostgreSQL test database and the `assert_eq!(resp.status(), StatusCode::OK)` assertion pattern
- Reference the test patterns in `tests/api/sbom.rs` for the established integration test structure

Per CONVENTIONS.md §Testing: integration tests hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern.
Applies: task modifies `tests/api/advisory.rs` matching the convention's Rust test file scope.

## Reuse Candidates
- `tests/api/sbom.rs` -- SBOM integration test patterns for reference on test structure and assertions

## Acceptance Criteria
- [ ] Integration tests for advisory list endpoint pass with enum-based status
- [ ] Integration tests for advisory detail endpoint pass with enum-based status
- [ ] Status filtering is tested for all four enum values (New, Analyzing, Fixed, Rejected)
- [ ] API response shape is verified to be unchanged (backward compatibility)
- [ ] No test code references the `advisory_status` lookup table

## Test Requirements
- [ ] Test advisory list endpoint returns correct results filtered by each status value
- [ ] Test advisory detail endpoint returns the status as a string in the response
- [ ] Test that creating an advisory with each valid status value works correctly
- [ ] Test error handling for invalid status values (if applicable at the API level)

## Verification Commands
- `cargo test --test advisory` -- advisory integration tests pass
- `cargo test` -- all integration tests pass (no regressions)

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
- Depends on: Task 4 -- Update advisory service, models, and endpoints to use status enum
- Depends on: Task 5 -- Update advisory ingestion pipeline for status enum
