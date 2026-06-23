## Summary
Update advisory integration tests for status enum migration

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory integration tests to reflect the new schema where advisory status is stored as a PostgreSQL enum column (`advisory.status`) instead of a foreign key to the `advisory_status` lookup table. Test fixtures that insert advisory rows must use the enum column directly. Assertions on API responses remain unchanged since the response shape is identical (status is still a string). Add test coverage for status filtering using the new enum column.

## Files to Modify
- `tests/api/advisory.rs` -- update test data setup to insert advisories with `status` enum column instead of `status_id` foreign key; remove any test setup code that inserts rows into `advisory_status` table; add test cases for status enum filtering (`GET /api/v2/advisory?status=Fixed`)

## Implementation Notes
The existing integration tests in `tests/api/advisory.rs` likely set up test data by inserting into both `advisory_status` and `advisory` tables. Replace this with direct insertion using the enum column. The test assertions on response bodies should remain the same since the API response shape is unchanged. Follow the existing integration test patterns used in `tests/api/sbom.rs` for setup/teardown and assertion style. Use `assert_eq!(resp.status(), StatusCode::OK)` pattern per repository conventions.

Per CONVENTIONS.md: use `assert_eq!(resp.status(), StatusCode::OK)` pattern for integration tests.
Applies: task modifies `tests/api/advisory.rs` matching the convention's `.rs` test file scope.

## Reuse Candidates
- `tests/api/sbom.rs` -- reference for integration test setup patterns, assertion style, and test database interaction

## Acceptance Criteria
- [ ] All advisory integration tests pass with the new enum-based schema
- [ ] Test data setup no longer references the `advisory_status` lookup table
- [ ] Tests cover advisory list with status filter using enum values
- [ ] Tests verify API response shape is unchanged (status is a string)

## Test Requirements
- [ ] Verify advisory list endpoint returns correct status values from enum column
- [ ] Verify advisory list with `?status=Fixed` filter returns only fixed advisories
- [ ] Verify advisory list with `?status=New` filter returns only new advisories
- [ ] Verify advisory detail endpoint returns correct status from enum column
- [ ] Verify all pre-existing advisory test cases still pass

## Verification Commands
- `cargo test --test advisory` -- all advisory integration tests pass
- `cargo test` -- full test suite passes

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main

[sdlc-workflow] Description digest: sha256-md:19690964a8df2912a1117e7c2a8ef88c8203760ca8da132d225cbfa06125c0ad
