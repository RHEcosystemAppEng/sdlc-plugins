## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory endpoint integration tests to reflect the schema change from a lookup table to an enum column. Test fixtures and setup code that insert into the `advisory_status` table must be updated to set the `status` enum value directly on advisory rows. Status filter tests must use enum values instead of joined lookups. Verify that the API response shape remains unchanged (status is still a string).

## Files to Modify
- `tests/api/advisory.rs` — update test setup to insert advisories with `status` enum values instead of `advisory_status` table rows and `status_id` FK; update status filter test assertions; remove any `advisory_status` table setup

## Implementation Notes
The integration tests in `tests/api/advisory.rs` currently set up test data by:
1. Inserting rows into `advisory_status` table
2. Inserting advisory rows with `status_id` FK references

After this change:
1. Insert advisory rows directly with `status: AdvisoryStatusEnum::New` (etc.)
2. Remove all `advisory_status` table setup code

Update test assertions to verify:
- Status filtering works with enum values (e.g., `?status=Fixed`)
- Response JSON contains status as a string (same shape as before)
- All four status values are correctly handled

Per CONVENTIONS.md §Testing: integration tests in `tests/api/` hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern.
Applies: task modifies `tests/api/advisory.rs` matching the convention's test file scope.

## Reuse Candidates
- `tests/api/sbom.rs` — reference for integration test patterns used in this project (setup, assertions, status code checks)
- `tests/api/advisory.rs` — existing test structure to adapt rather than rewrite

## Acceptance Criteria
- [ ] All advisory integration tests pass with the new enum-based schema
- [ ] Test setup no longer references the `advisory_status` table
- [ ] Status filter tests verify filtering by enum values
- [ ] Response shape assertions confirm status is still returned as a string
- [ ] Tests cover all four status values (New, Analyzing, Fixed, Rejected)

## Test Requirements
- [ ] Verify advisory list endpoint returns correct results when filtering by each status value
- [ ] Verify advisory detail endpoint returns the correct status string
- [ ] Verify response shape is unchanged (no breaking changes to API consumers)
- [ ] Verify error handling for invalid status filter values

## Verification Commands
- `cargo test --test api -- advisory` — all advisory integration tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 4 — Update advisory service and endpoint queries to use enum status
- Depends on: Task 5 — Update advisory ingestion pipeline for enum status
