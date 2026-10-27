## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory integration tests to work with the new enum-based status column. The tests currently set up advisory data using the `advisory_status` lookup table and join-based queries. After this change, tests set up advisory data with enum status values directly and verify filtering and retrieval against the enum column.

## Files to Modify
- `tests/api/advisory.rs` — update test setup to create advisories with `AdvisoryStatusEnum` values directly instead of inserting `advisory_status` lookup rows; update assertions to verify status field from enum column; add test cases for each status filter value

## Implementation Notes
In `tests/api/advisory.rs`, update the test data setup:
1. Remove any `advisory_status` table inserts from test fixtures
2. Create advisory records with `status: AdvisoryStatusEnum::New` (etc.) directly
3. Update status filter test assertions to use enum string values ("New", "Analyzing", "Fixed", "Rejected")

Follow the existing test pattern: integration tests hit a real PostgreSQL test database and use `assert_eq!(resp.status(), StatusCode::OK)` for response validation.

Per CONVENTIONS.md §Testing: integration tests in `tests/api/` hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern.
Applies: task modifies `tests/api/advisory.rs` matching the convention's Rust test file scope.

## Acceptance Criteria
- [ ] All advisory integration tests pass with the enum-based status column
- [ ] Tests verify status filtering for all four enum values (New, Analyzing, Fixed, Rejected)
- [ ] Tests verify that advisory list endpoint returns correct status string in response body
- [ ] Tests verify that advisory get endpoint returns correct status
- [ ] No references to `advisory_status` lookup table remain in test code

## Test Requirements
- [ ] Advisory list endpoint returns filtered results by status enum value
- [ ] Advisory get endpoint returns correct status field
- [ ] Test setup creates advisories with all four status values
- [ ] Tests validate response shape is unchanged (status is a string)

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 4 — Update advisory service and endpoints (tests depend on working service layer)
- Depends on: Task 5 — Update ingestion pipeline (tests may use ingestion to create test data)
