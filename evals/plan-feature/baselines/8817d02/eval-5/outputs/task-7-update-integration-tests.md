# Task 7 — Update advisory integration tests for enum status

## Summary

Update advisory integration tests to reflect enum-based status column and verify end-to-end behavior

## Repository

trustify-backend

## Target Branch

TC-9005

## Description

Update the advisory integration tests to work with the new enum-based status column. Tests must verify that advisory CRUD operations, status filtering, and ingestion all function correctly with the enum column instead of the lookup table join. Test fixtures and setup code that reference the `advisory_status` table must be updated.

## Files to Modify

- `tests/api/advisory.rs` — update test setup code that inserts into the `advisory_status` lookup table to instead use enum values directly; update assertions to verify status comes from the enum column; add tests for status filtering with the enum; remove any test helpers that reference the `advisory_status` table

## Implementation Notes

- In test setup code, replace any direct SQL or entity inserts into `advisory_status` with direct enum value setting on advisory records.
- Verify that status filtering tests cover all four enum values: `New`, `Analyzing`, `Fixed`, `Rejected`.
- Follow the existing integration test pattern in `tests/api/sbom.rs` for test structure and assertion patterns (use `assert_eq!(resp.status(), StatusCode::OK)` pattern).
- Integration tests hit a real PostgreSQL test database per the project convention — ensure the test database has the migration applied.
- Verify backward compatibility: the JSON response shape must be unchanged (status as a string).

## Reuse Candidates

- `tests/api/sbom.rs` — reference for integration test patterns (setup, request building, assertions)
- `tests/api/advisory.rs` — existing test file to modify; inspect current test setup and assertion patterns

## Acceptance Criteria

- [ ] All advisory integration tests pass with the new enum-based schema
- [ ] No test code references the `advisory_status` table or entity
- [ ] Tests verify status filtering works for all four enum values
- [ ] Tests verify the JSON response shape is unchanged (backward compatible)

## Test Requirements

- [ ] Test advisory list endpoint with no status filter returns all advisories with correct status values
- [ ] Test advisory list endpoint with status filter for each enum value returns correct filtered results
- [ ] Test advisory get endpoint returns correct status for a single advisory
- [ ] Test advisory ingestion creates records with correct enum status values

## Verification Commands

- `cargo test -p tests --test advisory` — all advisory integration tests pass

## Dependencies

- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 4 — Update advisory service and models to use enum status
- Depends on: Task 5 — Update advisory ingestion pipeline to write enum values directly
- Depends on: Task 6 — Update advisory endpoints for enum-based status filtering

sha256-md:a476f0ee9cec5c50b0e7b11e3e70f642be7d524ae9e48ceaaa54529d335511a7
