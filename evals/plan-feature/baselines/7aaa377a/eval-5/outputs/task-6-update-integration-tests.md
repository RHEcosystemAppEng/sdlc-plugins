## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory integration tests to work with the new enum-based status schema. The existing tests in `tests/api/advisory.rs` set up test data using the `advisory_status` lookup table and join-based queries. These must be updated to use the `AdvisoryStatusEnum` values directly, remove any test setup that populates the lookup table, and verify that status filtering works via enum comparison.

## Files to Modify
- `tests/api/advisory.rs` — update test data setup to use enum status values instead of lookup table inserts; update assertions for status filtering; remove any `advisory_status` table setup from test fixtures

## Implementation Notes
- Test data setup currently inserts rows into `advisory_status` and references them via FK. After this change, test data setup should set the `status` enum column directly on advisory rows.
- Status filter tests should verify `?status=Fixed` returns only advisories with that enum value.
- The response shape should remain identical — status is still a string in the JSON response. Existing response assertions should not need changes for the status field value format.
- Per CONVENTIONS.md §Testing: integration tests hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern.
  Applies: task modifies `tests/api/advisory.rs` matching the convention's test file scope.

## Reuse Candidates
- `tests/api/sbom.rs` — SBOM integration tests as a reference for test patterns without lookup table dependencies
- `tests/api/advisory.rs` — existing advisory tests showing the project's test setup and assertion patterns

## Acceptance Criteria
- [ ] All advisory integration tests pass with the new enum-based schema
- [ ] No test setup code references the `advisory_status` lookup table
- [ ] Status filtering tests verify enum-based filtering works correctly
- [ ] Test assertions confirm the API response shape is unchanged

## Test Requirements
- [ ] Advisory list endpoint test with status filter returns correct results
- [ ] Advisory detail endpoint test returns the correct status string
- [ ] Advisory creation/ingestion test verifies enum status is set correctly
- [ ] All existing advisory test scenarios continue to pass

## Verification Commands
- `cargo test --test advisory` — all advisory integration tests pass
- `cargo test` — full test suite passes

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 4 — Update advisory service and model to use enum column
- Depends on: Task 5 — Update advisory ingestion pipeline for enum status
