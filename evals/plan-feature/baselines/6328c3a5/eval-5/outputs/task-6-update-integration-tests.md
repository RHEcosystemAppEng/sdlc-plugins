## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory integration tests to validate the new enum-based status queries. The existing tests in `tests/api/advisory.rs` reference the old join-based status filtering and need to be updated to test enum column filtering, ingestion with direct enum writes, and correct API response serialization.

## Files to Modify
- `tests/api/advisory.rs` -- update all advisory tests to validate enum-based status filtering; remove any setup that inserts into the `advisory_status` lookup table; add tests for each enum variant

## Implementation Notes
- Update test setup functions to no longer insert into the `advisory_status` table. Advisory rows should be created with the `status` enum value directly.
- Update status filter tests to use the enum column directly (e.g., query with `?status=Fixed` and verify results).
- Add test coverage for each enum variant (New, Analyzing, Fixed, Rejected) to ensure all values round-trip correctly through the API.
- Follow the existing test pattern in `tests/api/advisory.rs`: use a real PostgreSQL test database, assert on HTTP status codes with `assert_eq!(resp.status(), StatusCode::OK)`.
- Verify backward compatibility: the API response shape should be identical to before (status as a plain string in JSON).

Per CONVENTIONS.md §Testing: follow the integration test pattern in `tests/api/` using real PostgreSQL test database.
Applies: task modifies `tests/api/advisory.rs` matching the convention's `.rs` file scope.

## Reuse Candidates
- `tests/api/sbom.rs` -- sibling integration test showing the project's test patterns and database setup

## Acceptance Criteria
- [ ] All existing advisory tests pass with the new enum-based schema
- [ ] Tests validate status filtering with enum values (e.g., `?status=Fixed`)
- [ ] Tests cover all four enum variants: New, Analyzing, Fixed, Rejected
- [ ] Test setup no longer references the `advisory_status` lookup table
- [ ] API response shape validation confirms status is returned as a string

## Test Requirements
- [ ] Integration test for advisory list with status filter returns correct filtered results
- [ ] Integration test for advisory list without filter returns all advisories with correct status strings
- [ ] Integration test for advisory get returns the correct status enum value as a string
- [ ] Integration test for advisory ingestion verifies enum value is stored correctly

## Verification Commands
- `cargo test --test advisory` -- advisory integration tests pass
- `cargo test -p tests` -- all integration tests pass

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
- Depends on: Task 4 -- Update advisory service and endpoints to use status enum column
- Depends on: Task 5 -- Update advisory ingestion pipeline for direct enum writes
