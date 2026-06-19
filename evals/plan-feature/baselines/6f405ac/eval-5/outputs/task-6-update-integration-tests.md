# Task 6 — Update advisory integration tests for enum status column

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory endpoint integration tests to reflect the schema change from a lookup table join to a direct enum column. Tests that set up advisory fixtures must create advisory rows with the `status` enum field directly instead of inserting into the `advisory_status` lookup table. Verify that the advisory list and get endpoints return correct status values, including filtered queries.

## Files to Modify
- `tests/api/advisory.rs` — update test fixtures to use `AdvisoryStatusEnum` values directly instead of `advisory_status` table inserts; update assertions if the setup flow changed; add test for status enum filtering

## Implementation Notes
Follow the existing test patterns in `tests/api/advisory.rs` and `tests/api/sbom.rs` for test structure. Use `assert_eq!(resp.status(), StatusCode::OK)` for response status checks per the testing convention.

Test fixtures should insert advisory rows with `status: AdvisoryStatusEnum::New` (or other variants) directly on the advisory model, without any reference to the now-removed `advisory_status` entity.

Per CONVENTIONS.md §Testing: integration tests in `tests/api/` hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern. Applies: task modifies `tests/api/advisory.rs` matching the convention's test file scope.

## Reuse Candidates
- `tests/api/sbom.rs` — SBOM integration tests; reference for fixture setup patterns and assertion style

## Acceptance Criteria
- [ ] All advisory integration tests pass with the new enum-based schema
- [ ] Test fixtures create advisories with direct enum status values
- [ ] No references to `advisory_status` lookup table remain in test code
- [ ] Status filtering test verifies correct enum-based filtering

## Test Requirements
- [ ] Advisory list endpoint test passes with enum-based status
- [ ] Advisory get endpoint test passes with enum-based status
- [ ] Advisory list with status filter test validates filtering by enum value
- [ ] All existing advisory tests pass without regression

## Verification Commands
- `cargo test --test advisory` — all advisory integration tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
