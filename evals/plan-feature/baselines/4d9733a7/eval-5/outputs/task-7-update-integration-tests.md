## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory integration tests to reflect the new enum-based status schema. Tests must verify that advisory CRUD operations, status filtering, and ingestion work correctly with the `advisory_status_enum` column instead of the `advisory_status` lookup table join.

## Files to Modify
- `tests/api/advisory.rs` — update all advisory test cases to work with the new enum-based status column: remove any test setup that inserts into the `advisory_status` lookup table; update test data creation to set `status` enum values directly; verify status filtering and response shapes work correctly with enum values

## Implementation Notes
- Remove any test fixture setup that creates rows in the `advisory_status` table — this table no longer exists.
- Update test advisory creation to set the `status` field as an `AdvisoryStatusEnum` variant instead of `status_id` FK.
- Verify that the response shape remains unchanged — the `status` field in API responses should still be a string (e.g., `"Fixed"`), not the enum variant name in any Rust-specific format.
- Per CONVENTIONS.md §Testing: integration tests hit a real PostgreSQL test database using `assert_eq!(resp.status(), StatusCode::OK)` pattern. Follow this pattern for all assertion checks.
  Applies: task modifies `tests/api/advisory.rs` matching the convention's Rust test file scope.
- Reference existing test patterns in `tests/api/sbom.rs` for how integration tests create test data, invoke endpoints, and assert responses.

## Reuse Candidates
- `tests/api/sbom.rs` — SBOM endpoint integration tests; follow the same patterns for test setup, endpoint invocation, and response assertion
- `tests/api/advisory.rs` — existing advisory tests; modify in place to use new enum schema

## Acceptance Criteria
- [ ] All advisory integration tests pass with the new enum-based schema
- [ ] Tests verify status filtering works with each enum variant (New, Analyzing, Fixed, Rejected)
- [ ] Tests verify the API response shape includes status as a plain string
- [ ] No test code references the `advisory_status` lookup table
- [ ] Test coverage includes: advisory list, advisory detail, advisory list with status filter

## Test Requirements
- [ ] Advisory list endpoint test — verify list returns advisories with correct status strings
- [ ] Advisory detail endpoint test — verify detail returns advisory with correct status
- [ ] Advisory status filter test — verify filtering by each enum variant returns correct results
- [ ] Advisory ingestion test — verify ingested advisory has correct enum status value

## Verification Commands
- `cargo test --test api -- advisory` — run advisory integration tests

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 4 — Update advisory service and model layer to use enum status
- Depends on: Task 5 — Update advisory REST endpoints for enum status filtering
- Depends on: Task 6 — Update advisory ingestion pipeline for direct enum writes
